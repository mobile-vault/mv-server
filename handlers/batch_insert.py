import tornado.web
from tornado.web import asynchronous
import threading
import time
import functools
import json
from boto import ses
from os import environ
from handlers.super import SuperHandler
from tornado.template import Loader

class BatchInsertRequestHandler(SuperHandler):

    def initialize(self):
        self.thread=None

    def perform_post(self,callback):
        output = dict()
        try:

            company = self.get_current_company()
            company_name = self.get_current_company_name()
            excel_file = self.request.files['data'][0]
            #print excel_file
            if excel_file['filename'][-4:]=='xlsx':
                output['pass']= True
                filename = '/tmp/'+str(time.time())+'.xlsx'
                fp = open(filename,'w')
                fp.write(excel_file['body'])
                fp.close()
                #When done, Let the parser do it's work in a seperate thread.
                from excel import ExcelParser
                parser = ExcelParser(path=filename, company=company)
                output['data']=parser.parse(excel_path=filename, company=company, company_name=company_name,
                    callback=self.users_added_callback)
            else:
                output['pass']=False
        except Exception,err:
            output['pass']=False
            output['message']=repr(err)
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(callback,output))

    def users_added_callback(self,users):
        '''
        Server url will be dynamic to work same code on different servers
        in case on user enrollment and iOS profile generation also.
        '''
        loader = Loader("/opt/toppatch/mv/media/app/")
        server_url = environ.get('SERVER_CNAME')
        ses_conn = ses.connect_to_region('us-east-1',
                    aws_access_key_id=environ.get('AWS_SES_ACCESS_KEY_ID'),
                    aws_secret_access_key=environ.get(
                        'AWS_SES_SECRET_ACCESS_KEY'))
        for user in users:

            link = str(server_url) + '/enroll/'+str(user.get('enrollment_id'))
            message = loader.load('user_enroll_mail.html').generate(
                        company_name=user.get('company_name'),
                    user_passwd=user.get('passcode'), activation_link=link)
            # message  = 'Your verification \
            #             link is : {0} and enrollment password is {1} . To ensure \
            #             your device os please open this link in your device \
            #             browser only. :)'.format(
            #                 str(server_url) + '/enroll/'+str(user['enrollment_id']), user['passcode'])
            #message  = message.replace('  ', '')

            try:
                ses_conn.send_email('mv@toppatch.com',
                        'MDM Enrollment verification', message,
                         [user['email']], format='html')
            except Exception,err:
                print repr(err)
    def send_users_email(self,users):
        pass

    @tornado.web.authenticated
    @asynchronous
    def post(self):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header ('Content-Type', 'application/json')
        self.thread = threading.Thread(target=self.perform_post,args=(self.callback_post,))
        self.thread.start()

    def options(self):
        self.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.add_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    def callback_post(self,output):
        self.finish(json.dumps(output))


if __name__ =="__main__":
    application = tornado.web.Application([(r"/", BatchInsertRequestHandler)])
    application.listen(8099)
    tornado.ioloop.IOLoop.instance().start()
