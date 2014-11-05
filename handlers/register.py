import json
from binascii import b2a_base64 as e64
import threading
# import ipdb
import tornado
from tornado.web import asynchronous
from logger import Logger
from db.helpers.login import LoginDBHelper
from db.helpers.company import CompanyDBHelper
from .manage_pass import make_verifier
from .admin_mailer import admin_signup


class RegisterHandler(tornado.web.RequestHandler):

    def options(self):
        self.add_header('Access-Control-Allow-Methods',
                        'GET,POST, PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        self.add_header('Access-Control-Allow-Origin', '*')

    @asynchronous
    def post(self):
        self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        RegisterWorkerThread(request=self, callback=self.on_complete).start()

    def on_complete(self):
        self.finish()


class RegisterWorkerThread(threading.Thread):

    def __init__(self, request=None, callback=None):
        threading.Thread.__init__(self)
        self.request = request
        self.callback = callback

    def run(self):
        # log = Logger('RegisterWorkerThread')
        # TAG = 'run'
        print 'RegisterWorkerThread'
        final_dict = {}

        company = CompanyDBHelper()
        admin = LoginDBHelper()

        request_data = json.loads(self.request.request.body)

        company_name = request_data.get('company_name')
        company_email = request_data.get('company_email')
        company_address = request_data.get('company_address')
        company_contact = request_data.get('company_contact')
        admin_name = request_data.get('admin_name')
        admin_email = request_data.get('admin_email')
        admin_password = request_data.get('admin_password')

        company_id, duplicate_company = company.add_company(
            {'name': company_name, 'email': company_email,
             'contact': company_contact, 'address': company_address})

        # if company_id and duplicate_company:
        # Send mail to admin registered for this company
        #     pass

        if company_id:

            temp_hash = make_verifier(str(admin_password))
            final_hash = e64(temp_hash).strip()
            pass_id = admin.set_login_password(final_hash)

            if pass_id:
                admin_id, duplicate_admin = admin.add_admin(
                    {'email': admin_email, 'name': admin_name,
                     'login_id': pass_id, 'company_id': company_id})

                if admin_id and duplicate_admin:
                    # Admin already registered, set pass false
                    final_dict['admin'] = True
                    final_dict['pass'] = False

                elif admin_id and not duplicate_admin:
                    final_dict['pass'] = True
                    final_dict['admin'] = False

                    # send verification mail to this admin
                    admin_signup(admin_id, company_id, admin_email,
                                 company_email)
                else:
                    final_dict['pass'] = False
                    final_dict['admin'] = False

            else:
                final_dict['pass'] = False
                final_dict['admin'] = False
        else:
            final_dict['pass'] = False
            final_dict['admin'] = False

        self.request.write(json.dumps(final_dict))
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
