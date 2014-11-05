import threading
import json
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from logger import Logger
from db.constants import Constants as C
from db.helpers.device_details import DeviceDetailsDBHelper
from db.helpers.enrollment import EnrollmentDBHelper
from db.helpers.user import UserDBHelper
from db.helpers.company import CompanyDBHelper


class UpdateTokenRequestHandler(tornado.web.RequestHandler):

    @asynchronous
    def post(self):
        UpdateTokenThread(self, callback=self.onComplete).start()

    def onComplete(self):
        self.finish()


class UpdateTokenThread(threading.Thread):
    log = 'log'

    def __init__(self, request=None, callback=None, *args, **kwargs):
        super(UpdateTokenThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback

    def run(self):
        self.log = Logger('UpdateTokenThread')
        TAG = 'run'
        print 'In UpdateTokenThread\'s POST'

        # Get the parameters which are to be used
        password = str(self.request.get_argument('password', None))
        user_email = str(self.request.get_argument('email', None))
        token = str(self.request.get_argument('token', None))
        print password
        print user_email
        print token

        token = token.replace('<', '')
        token = token.replace('>', '')
        token = token.replace(' ', '')
        result_dict = {}

        user = UserDBHelper()

        user_detail_dict = user.get_user_with_email(user_email)
        print 'user_dict = ' + str(user_detail_dict)
        if user_detail_dict is None:
            self.log.e(
                TAG,
                'No user corresponding to the email = ' +
                str(user_email))
            result_dict['pass'] = False
            result_dict['is_enrolled'] = False
            opJson = json.dumps(result_dict)
            self.request.set_header('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:

            company = CompanyDBHelper()

            user_id = str(user_detail_dict[C.USER_TABLE_ID])
            user_name = str(user_detail_dict[C.USER_TABLE_NAME])
            company_id = str(user_detail_dict[C.USER_TABLE_COMPANY])

            company_detail_dict = company.get_company(company_id)
            company_name = str(company_detail_dict[C.COMPANY_TABLE_NAME])

            enrollment = EnrollmentDBHelper()
            filter_dict = {
                C.ENROLLMENT_TABLE_USER: str(user_id),
                C.ENROLLMENT_TABLE_PASSWORD: str(password)
            }
            enrollment_list = enrollment.get_enrollments(filter_dict)
            print 'enrollment_list = ' + str(enrollment_list)
            if enrollment_list is None:
                self.log.e(
                    TAG,
                    'No enrollment corresponding to the email = ' +
                    str(user_email) +
                    ' and password = ' +
                    str(password))
                result_dict['pass'] = False
                result_dict['is_enrolled'] = False
                opJson = json.dumps(result_dict)
                self.request.set_header('Content-Type', 'application/json')
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:

                device_id = enrollment_list[0][C.ENROLLMENT_TABLE_DEVICE]
                user_data = {'name': user_name, 'company': company_name}
                result_dict['data'] = user_data

                if device_id is None:
                    self.log.e(TAG, 'No device ID in enrollment table\
                             corresponding to the email = ' +
                               str(user_email) + ' and password = ' +
                               str(password))
                    result_dict['pass'] = True
                    result_dict['is_enrolled'] = False
                    opJson = json.dumps(result_dict)
                    self.request.set_header('Content-Type', 'application/json')
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
                else:

                    device_detail = DeviceDetailsDBHelper()
                    updated = device_detail.update_device_details(
                        str(device_id), {
                            C.DEVICE_DETAILS_TABLE_MESSAGE_TOKEN: str(token)})

                    if not updated:
                        self.log.e(
                            TAG,
                            'Not able to update Message Token in \
Device Details Table DeviceID = ' + str(device_id))
                        result_dict['pass'] = False
                        result_dict['is_enrolled'] = True
                        opJson = json.dumps(result_dict)
                        self.request.set_header(
                            'Content-Type',
                            'application/json')
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                    else:
                        self.log.i(
                            TAG,
                            'Device Messge Token updated successfully \
DeviceID = ' + str(device_id))
                        result_dict['pass'] = True
                        result_dict['is_enrolled'] = True
                        opJson = json.dumps(result_dict)
                        self.request.set_header(
                            'Content-Type',
                            'application/json')
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
