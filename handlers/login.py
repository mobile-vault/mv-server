import json
import threading
import ipdb
import tornado
from tornado.web import asynchronous
from logger import Logger
from db.constants import Constants as c
from db.helpers.login import LoginDBHelper
from db.helpers.company import CompanyDBHelper
from db.helpers.session import SessionDBHelper
from .manage_pass import verify_password
from binascii import a2b_base64 as d64


# from toppatch_db.helpers.login import *
# from toppatch_db.constants import Constants as c

class LoginHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self,arg):
        self.render('login.html')

    @asynchronous
    def post(self,arg):
        LoginWorkerThread(request=self,callback=self.on_complete).start()

    def on_complete(self,res):
        self.finish(res)

class LoginWorkerThread(threading.Thread):
    def __init__(self,request =None,callback=None):
        threading.Thread.__init__(self)
        self.request = request
        self.callback = callback

    def run(self):
        log = Logger('LoginWorkerThread')
        TAG = 'run'
        print 'LoginWorkerThread'

        user_name = self.request.get_argument('name', None)
        password = self.request.get_argument('password', None)
        #ipdb.set_trace()

        login = LoginDBHelper()
        admin_detail = login.get_login(user_name)

        #print admin_detail
        if admin_detail is None:
            result = dict()
            result['pass']= False
            result['message']='Authentication failed'
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.redirect('/login.html?err=Invalid+Username+Password+Combination')

        elif admin_detail:
            ## Verify Mr. annonymous

            login_success = verify_password(str(password),
                                  d64(admin_detail.get('password')))

            if login_success:

                ### Session table entry will go here ###
                session = SessionDBHelper()
                session_dict = {}
                session_dict[c.SESSION_TABLE_USER] = admin_detail.get(c.LOGIN_TABLE_ID)
                session_dict[c.SESSION_TABLE_IP] = self.request.request.remote_ip
                session_dict[c.SESSION_TABLE_USER_AGENT] = self.request.request.headers.get(
                                                            'User-Agent')
                session.add_session(session_dict)

                company_helper = CompanyDBHelper()
                company_details = company_helper.get_company(str
                    (admin_detail[c.LOGIN_TABLE_COMPANY]))
                company_name = company_details[c.COMPANY_TABLE_NAME]
                self.request.set_secure_cookie("user",
                                self.request.get_argument("name"))
                self.request.set_secure_cookie("company",
                             str(admin_detail[c.LOGIN_TABLE_COMPANY]))
                self.request.set_secure_cookie("company_name", company_name)
                result = dict()
                result['pass'] = True
                result['message'] = 'Welcome'

                #self.request.write(json.dumps(result))
                if self.request.get_argument('next', None):
                    self.request.redirect('/index.html')
                    #tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    self.request.redirect('/index.html')
                    #tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                print'else'
                result = dict()
                result['pass']= False
                result['message']='Authentication failed'
                #self.request.add_header('Access-Control-Allow-Origin', '*')
                self.request.set_header ('Content-Type', 'application/json')
                self.request.redirect('/login.html?err=Invalid+Username+Password+Combination')

