'''
This script will handle the activation link sent to admin and make corresponding change in the database to make user activated.
'''
import json
from os import environ
import threading
#import ipdb
import tornado
from tornado.web import asynchronous
from logger import Logger
from db.helpers.login import LoginDBHelper
from itsdangerous import (TimedJSONWebSignatureSerializer, BadSignature,
                          SignatureExpired)
from tornado.template import Template
from tornado.template import Loader

class ActivationLinkHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self, hash_url):
        ActivationWorkerThread(request=self, hash_url=hash_url,
                      callback=self.on_complete).start()

    def on_complete(self):
        self.finish()

class ActivationWorkerThread(threading.Thread):
    def __init__(self, request =None, hash_url=None, callback=None):
        threading.Thread.__init__(self)
        self.request = request
        self.callback = callback
        self.hash_url = hash_url

    def run(self):
        log = Logger('ActivationWorkerThread')
        TAG = 'run'
        print 'ActivationWorkerThread'

        ### load html file for rendering ####
        loader = Loader("/opt/toppatch/mv/media/app/")
        t_status = 'alert-danger'

        if self.hash_url:

            salt_key = environ.get('salt_key')
            json_url_key = environ.get('json_url_key')

            danger_signer = TimedJSONWebSignatureSerializer(json_url_key)

            try:
                data_dict = danger_signer.loads(self.hash_url, salt=salt_key)

                company_data = data_dict.get('cmd_hash')
                admin_data = data_dict.get('adm_hash')

                if company_data and admin_data:

                    admin = LoginDBHelper()

                    company_id = company_data
                    admin_id = admin_data
                    status = admin.set_login(admin_id, company_id)

                    if status:
                        message = '''Success! Please visit \
                    https://demo-mdm.toppatch.com and login using your admin \
                    email as username and password used at the time of \
                    Registration.
                        '''
                        message = message.replace('  ', '')
                        t_status = 'alert-success'
                    else:
                        message = "Mr. Intruder U r failed in this attemps.!!!"
                else:
                    message = "Mr. Intruder U r failed in this attemps.!!!"

            except SignatureExpired:
                message = 'Sorry! This link was already expired'

            except BadSignature:
                message = '''Thanks for visiting . Please try agian after \
                          some time to activate the link sent to you.'''

        else:
            message = 'Sorry! This link was already expired'

        self.request.write(loader.load("error_invalid.html").generate(
                message=message, status=t_status))
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
