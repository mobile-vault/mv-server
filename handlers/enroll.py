## Request will come like http://www.example.com/enroll
## with POST data


import json
import threading
from random import randint
from os import environ
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
from boto import ses
from logger import Logger
#from send_enroll_mail import *
from db.constants import Constants as c
from db.helpers.enrollment import EnrollmentDBHelper
from db.helpers.user import UserDBHelper
from db.helpers.company import CompanyDBHelper
from handlers.super import SuperHandler
from .markov_passwords import generate_password
from tornado.template import Loader
# import time
ses_conn = ses.connect_to_region('us-east-1',
                    aws_access_key_id=environ.get('AWS_SES_ACCESS_KEY_ID'),
                    aws_secret_access_key=environ.get(
                        'AWS_SES_SECRET_ACCESS_KEY'))


## Async class to get the enroll request by using the POST method
class EnrollDeviceRequestHandler(SuperHandler):

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                        'GET,POST,PUT,OPTIONS, DELETE')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def post(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        DeviceEnrollerThread(request=self, callback=self.finish,
                 company_id=self.get_current_company(),
                 company_name=self.get_current_company_name()).start()

class DeviceEnrollerThread(threading.Thread):
    '''
    user_email = 'email'
    team_id = 'team'
    user_name = 'user_name'
    role_id = 'role'
    password = 'pass'
    company = 'company'
    os = 'iOS'
    device_name = 'iPhone'
    link = 'http://localhost:8888/enroll/'
    '''

    '''
    Server url will be dynamic to work same code on different servers
    in case on user enrollment and iOS profile generation also.
    '''
    server_url = environ.get('SERVER_CNAME')
    link = str(server_url) + '/enroll/'

    def __init__(self, request=None, callback=None, company_id=None,
                    company_name=None, *args, **kwargs):
        super(DeviceEnrollerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_name = company_name
        self.company_id = company_id

    def run(self):
        #Find all the POST arguments required

        company_id = self.company_id
        company_name = str(self.company_name)

        loader = Loader("/opt/toppatch/mv/media/app/")

        thread1 = {}

        log = Logger('EnrollDevice')
        tag = 'POST'
        request_body = json.loads(self.request.request.body)


        try:
            self.user_email = str(request_body.get('user_email', None))
            self.user_name = str(request_body.get('user_name', None))
            self.team_id = str(request_body.get('team_id', None))
            self.role_id = str(request_body.get('role_id', None))
            self.company_id = str(company_id)
        except:
            self.request.write('Some arguments are not supplied')
            opJson = json.dumps({'pass':False, 'user_name': None,
                                 'link' : None, 'password':None,
                                  'error':'Some argument not supplied'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            log.e(tag, 'Some arguments not sent in POST request for enrollment')
            return

        if self.user_email is None or self.user_name is None or\
                         self.company_id is None:
            log.e(tag, 'Email or user_name is NULL')
            opJson = json.dumps({'pass':False, 'user_name': None,
                        'link' : None, 'password':None,
                         'error':'user_name or Email or Company is None'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


        if self.user_name == '' or self.user_email == '':
            log.e(tag, 'Email or user_name is empty')
            opJson = json.dumps({'pass':False, 'user_name': None,
                             'link' : None, 'password':None,
                        'error':'email or user_name or company is empty'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


        password = generate_password()

        user = UserDBHelper()
        user_dict = {
                    c.USER_TABLE_NAME: str(self.user_name),
                    c.USER_TABLE_TEAM : str(self.team_id),
                    c.USER_TABLE_ROLE: str(self.role_id),
                    c.USER_TABLE_EMAIL: str(self.user_email),
                    c.USER_TABLE_COMPANY: str(self.company_id)
                   }
        user_id, duplicate = user.add_user_if_not_exists(user_dict)

        if duplicate:
            log.e(tag,'No id from primary key ')
            opJson = json.dumps({'pass':False, 'user_name': self.user_name,
                         'link' : None, 'password':None, 'duplicate': True,
                        'error':'DB has problem'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            enrollment_dict = {
                              c.ENROLLMENT_TABLE_USER: user_id,
                              c.ENROLLMENT_TABLE_PASSWORD: password,
                              c.ENROLLMENT_TABLE_IS_ENROLLED: False
                              }
            enrollment = EnrollmentDBHelper()
            enrollment_id = str(enrollment.add_enrollment(enrollment_dict))

            enrollment_dict = enrollment.get_enrollment(enrollment_id)

            if enrollment_id is not None:
                self.link += enrollment_id

                try:
                    message = loader.load('user_enroll_mail.html').generate(
                           company_name=self.company_name,
                           user_passwd=password, activation_link=self.link)

                    ses_conn.send_email('mv@toppatch.com',
                                'MDM Enrollment verification', message,
                                 [self.user_email], format='html')
                    print 'No error found'
                    log.i(tag, 'Enrollment request successful')
                    opJson = json.dumps({'pass':True, 'user_name': self.user_name,
                     'link' : 'link', 'password':'password', 'error':None})

                except Exception, err:
                    print 'Mail Sending error exception is :', repr(err)

                    log.e(tag, 'Incorrect EmailID sent')
                    opJson = json.dumps({'pass':False, 'user_name': self.user_name,
                      'link' : None, 'password':None, 'error':'Wrong emailID'})

            else:
                log.e(tag,
                      'Entry is not done in Enrollment table for UserID = '\
                         +  str(user_id))
                opJson = json.dumps({'pass':False, 'user_name': self.user_name,
                      'link' : None, 'password':None, 'error':'Wrong emailID'})

            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)



if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/enroll", EnrollDeviceRequestHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
