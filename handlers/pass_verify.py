import os
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from create_profile import *
from logger import Logger
from db.constants import Constants as c
from db.helpers.enrollment import EnrollmentDBHelper
from tornado.template import Template
from tornado.template import Loader

class PassVerifyRequestHandler(tornado.web.RequestHandler):

    @asynchronous
    def post(self):
        PassVerifyerThread(self,callback=self.onComplete).start()

    def onComplete(self):
        self.finish()

class PassVerifyerThread(threading.Thread):
    def __init__(self, request = None, callback=None, *args, **kwargs):
        super(PassVerifyerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback

    def run(self):
        log = Logger('PassVerifyerThread')
        tag = 'run'
        print 'In PassVerify\'s POST'

        loader = Loader("/opt/toppatch/mv/media/app/")
        passwd = str(self.request.get_argument('password',None))
        enrollment_id = self.request.get_argument('hidden', None)
        log.e(tag, 'enrollment id : '+enrollment_id)

        ### check type of enrollment id ###
        try:
            enrollment_id = int(enrollment_id)
            invalid_enrollment_id = False
            enrollment_id = str(enrollment_id)
        except ValueError:
            invalid_enrollment_id = True

        #No enrollment ID sent
        if enrollment_id is None or invalid_enrollment_id:
            #print 'Some Error in enrollID not present corresponding\
            #     to the password or of invalid format'
            log.e(tag, 'Some Error in program deviceID not present \
                    corresponding to the password or of invalid format')
            self.request.write(loader.load("error_invalid.html").generate(
                    message='Invalid link, Mr. intruder. :D ;)',
                    status='alert-danger'))
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        #Password not found
        elif passwd is None:
            redirect_url = '''/enroll/{0}?err=Try+again+with+correct+password'''.format(enrollment_id)
            self.request.redirect(redirect_url)
            log.i(tag,'password is incorrect')
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        #Enrollent ID and Password found
        else:

            enrollment = EnrollmentDBHelper()
            ret_dict = enrollment.get_enrollment(enrollment_id)
            #print ret_dict
            ret = None
            if ret_dict is not None:
                ret = str(ret_dict[c.ENROLLMENT_TABLE_PASSWORD])

            else:
                log.e(tag,'Enrollment password cannot be reterived')

            if ret is None:
                log.e(tag,'DB did not sent the password from Enrollment table')
                self.request.write(loader.load("error_invalid.html").generate(
                    message='Invalid link, Mr. intruder. :D ;)',
                     status='alert-danger'))

                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                #Password matched
                if ret == passwd:
                    print 'download the profile'

                    #Now find out the browser details
                    # Create the profile to download
                    thread = CreateProfileThread(enrollment_id)
                    thread.start()
                    thread.join()

                    filename = enrollment_id +'.mobileconfig'
                    signed_filename = 'mdm_'+ enrollment_id + '.mobileconfig'

                    log.i(tag,'Downloading the iOS profile')
                    log.i(tag, 'Signing the iOS profile')
                    sign_command = """
                           openssl smime \
                          -sign \
                         -signer /etc/ssl/star_toppatch_com.pem \
                          -inkey /etc/ssl/star_toppatch_com.key \
                  -certfile /opt/toppatch/assets/ios/DigiCertPersonal_chain.pem \
                            -nodetach \
                            -outform der \
                            -in {0} \
                            -out {1}
                            """.format(filename, signed_filename)

                    os.system(sign_command)
                    f = file(signed_filename,'rb')
                    self.request.set_header ('Content-Type',
                        'application/x-apple-aspen-config; chatset=utf-8')
                    self.request.set_header ('Content-Disposition',
                             'attachment; filename='+filename+'')
                    self.request.write(f.read())
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)

                    ## Delete the file from server after download 'Delay can be introduced'.
                    os.remove(filename)
                    os.remove(signed_filename)
                else:
                    redirect_url = '''/enroll/{0}?err=Try+again+with+correct+password'''.format(enrollment_id)
                    self.request.redirect(redirect_url)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                    log.i(tag,'Incorrect Password for enrollment')
