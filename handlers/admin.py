import json
from binascii import b2a_base64 as e64
from binascii import a2b_base64 as d64
import threading
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import ipdb
from logger import Logger
from handlers.super import SuperHandler
from db.helpers.login import LoginDBHelper
from .manage_pass import verify_password, make_verifier

class AdminRequestHandler(SuperHandler):

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods', 'GET,POST, PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self):
        AdminGetHandlerThread(self, current_user=self.get_current_user(),
                    company_id=self.get_current_company(), callback=self.finish).start()

    @tornado.web.authenticated
    @asynchronous
    def post(self):
        AdminPostHandlerThread(request=self, current_user=self.get_current_user(),
                    company_id=self.get_current_company(), callback=self.finish).start()


class AdminGetHandlerThread(threading.Thread):
    final_dict = {}
    def __init__(self, request = None, callback=None, current_user=None,
                                        company_id=None, *args, **kwargs):
        super(AdminGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.current_user = current_user
        self.company_id = company_id

    def run(self):
        log = Logger('AdminGetHandlerThread')
        self.final_dict['message'] = ''
        self.final_dict['pass'] = True

        data_dict = {}
        customer_dict = {}

        data_dict['username'] = self.current_user
        data_dict['company_id'] = self.company_id

        #customer_dict['name'] = 'Toppatch Inc.'
        #data_dict['current_customer'] = customer_dict
        #ipdb.set_trace()


        # data_dict['groups'] = []
        # data_dict['enabled'] = True
        # data_dict['customers'] = []
        # data_dict['full_name'] = 'Toppatch Admin Account'

        # default_customer_dict = {}
        # default_customer_dict['name'] = 'default'

        # data_dict['default_customer'] = default_customer_dict

        # data_dict['user_name'] = 'admin'
        # data_dict['email'] = 'admin@toppatch.com'

        permissions = []
        permissions.append('admin')
        permissions.append('install')

        data_dict['permissions'] = permissions

        self.final_dict['data'] = data_dict

        opJson = json.dumps(self.final_dict)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header ('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class AdminPostHandlerThread(threading.Thread):

    def __init__(self, request=None, callback=None, current_user=None,
                                        company_id=None, *args, **kwargs):
        super(AdminPostHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.current_user = current_user
        self.company_id = company_id


    def run(self):
        log = Logger('AdminPostHandlerThread')
        request_data = json.loads(self.request.request.body)
        print request_data
        login = LoginDBHelper()
        update_status = False

        final_dict = {}

        admin_detail = login.get_login(self.current_user, update_flag=True)

        if admin_detail is None:
            final_dict['pass'] = False
            final_dict['message'] = "Wrong username password combination"

        else:
            current_password = request_data.get('current_password')
            login_success = verify_password(str(current_password),
                                        d64(admin_detail.get('password')))


            if login_success:
                login_id = admin_detail.get('login_id')
                new_password = request_data.get('new_password')
                temp_passwd = make_verifier(str(new_password))
                new_password_hash = e64(temp_passwd).strip()
                update_status = login.update_login_password(login_id,
                                new_password_hash)

            if update_status:

                final_dict['pass'] = True
                final_dict['message'] = "Password changed successfully"

            else:

                final_dict['pass'] = False
                final_dict['message'] = "Wrong username password combination"

        opJson = json.dumps(final_dict)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header ('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
