# from random import randint
import tornado.ioloop
import tornado.ioloop as ioloop
import tornado.web
from tornado.web import asynchronous
import threading
import cgi
# import time
from logger import Logger
from db.helpers.base import DBHelper
from db.helpers.violations import ViolationsDBHelper
from db.helpers.device import DeviceDBHelper
from db.helpers.device_details import DeviceDetailsDBHelper
from db.helpers.enrollment import EnrollmentDBHelper
from db.helpers.user import UserDBHelper
from db.constants import Constants as c
from tasks import create_command_handler_task
from APNSWrapper import *
from lxml import etree
# from tornado.template import Template
from tornado.template import Loader
from .admin_mailer import admin_mailer

'''
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
'''


class CheckInRequestHandler(tornado.web.RequestHandler):

    def callback(self):
        self.finish()

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                        'GET,POST, PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
# self.add_header('Access-Control-Allow-Origin', '*')

    @asynchronous
    def put(self, data):
        CheckinPerformerThread(request=self, data=data,
                               callback=self.callback).start()

    def get(self, data):
        log = Logger('CheckInHandler Get')
        tag = 'Profile get method'
        user_agent = self.request.headers['User-Agent']

        if 'iPad' in user_agent or 'iPhone OS' in user_agent:

            loader = Loader("/opt/toppatch/mv/media/app/")
            self.write(
                loader.load("enroll_form.html").generate(
                    temp_enroll=data))
        elif 'Android' in user_agent:
            self.redirect('/android_profile.apk')
            log.i(tag, 'Downloading the Android APK')

        else:
            log.i(tag, 'Incorrect browser used in passverify')
            loader = Loader("/opt/toppatch/mv/media/app/")
            self.write(loader.load("error_invalid.html").generate(
                message='Please use Android or iOS device to open this link',
                status='alert-danger'))


class CheckinPerformerThread(threading.Thread):
    push_magic = 'push_magic'
    device_token = 'device_token'
    unlock_token = 'unlock_token'
    udid = 'UDID'
    do_entry = False

    def __init__(
            self,
            data=None,
            callback=None,
            request=None,
            *args,
            **kwargs):
        super(CheckinPerformerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.data = data
        database_con = DBHelper()
        self.cursor = database_con.cursor

    def run(self):
        log = Logger('CheckInHandler PUT')
        TAG = 'run'
        # print ' In deviceCheckin PUT Handler\n\n\n'

        # parse the body of PUT
        # First extract the XML
        arguments = cgi.parse_qsl(self.request.request.body)
        intermediate = arguments[0]
        currentxml = intermediate[1]
        final = currentxml[25:-1]
        enrollment_id = str(self.data)
#         print final

        # Actual Parsing
        #tree = ET.ElementTree(ET.fromstring(final))
# tree = ET.parse('temp.xml')   ### For testing only
        node = etree.fromstring(final)
        device_data = []
        for text_of_child in node.itertext():
            if len(text_of_child.strip()) > 0:
                device_data.append(text_of_child.strip())
        device_data = dict(zip(device_data[::2], device_data[1::2]))

        if device_data.get('PushMagic'):
            self.push_magic = str(device_data.get('PushMagic'))

        if device_data.get('Token'):
            self.device_token = str(device_data.get('Token'))
            self.device_token = self.device_token.replace(' ', '+')
            self.device_token = self.device_token.replace('\n', '')
            self.device_token = self.device_token.replace('\t', '')
            # print len(self.device_token)
            # print self.device_token
        if device_data.get('MessageType'):
            message = device_data.get('MessageType')
            if message == 'TokenUpdate':
                self.do_entry = True
            elif message == 'Authenticate':
                self.do_initial_entry = True

        if device_data.get('UnlockToken'):
            self.unlock_token = device_data.get('UnlockToken')
            self.unlock_token = self.unlock_token.replace(' ', '+')
            self.unlock_token = self.unlock_token.replace('\n', '')
            self.unlock_token = self.unlock_token.replace('\t', '')

        if device_data.get('UDID'):
            self.udid = device_data.get('UDID')

        ### Initial Device DB Entries ###
        if self.do_entry:
            enrolled_success = False
            device_id = None
            # fetch info from enrollment table
            enrollment = EnrollmentDBHelper()

            enrollment_dict = enrollment.get_enrollment(enrollment_id)
            # print 'enrollment_dict = ' + str(enrollment_dict)
            if enrollment_dict is None:
                log.e(TAG,
                      'No user ID in Enrollment table. Enrollment ID = '
                      + str(enrollment_id))
                reply = """
                    <html>
                        <body>401</body>
                    </html>
                    """
                self.request.set_status(401)
                self.request.write(reply)
                ioloop.IOLoop.instance().add_callback(self.callback)

            else:

                reply = """
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
                         "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                        <plist version="1.0">
                        <dict>
                        </dict>
                        </plist>
                """
                print 'inner write'
                self.request.write(reply)
                ioloop.IOLoop.instance().add_callback(self.callback)

                device = DeviceDBHelper()
                violation = ViolationsDBHelper()
                user_id = str(enrollment_dict[c.ENROLLMENT_TABLE_USER])
                device_id = enrollment_dict.get(c.ENROLLMENT_TABLE_DEVICE)
                devices = device.get_device_with_udid(
                    str(self.udid), status=True)
                # print "\n print devices list if available \n\n",devices
                device_detail = DeviceDetailsDBHelper()
                device_details_dict = {
                    'token': self.device_token,
                    'push_magic': self.push_magic,
                    'unlock_token': self.unlock_token
                }

                if device_id:

                    enrolled_success = True
                    device.update_device(str(device_id),
                                         {c.DEVICE_TABLE_DELETED: False,
                                          c.DEVICE_TABLE_UDID: str(self.udid)})
                    device_detail.update_device_details(str(device_id),
                                                        device_details_dict)
                    print "Device details table updated."

                elif devices:
                    device_id = devices[0][c.DEVICE_TABLE_ID]
                    device.update_device(str(device_id),
                                         {c.DEVICE_TABLE_DELETED: False})
                    device_detail.update_device_details(str(device_id),
                                                        device_details_dict)
                    enrollment.update_enrollment(
                        enrollment_id, {
                            c.ENROLLMENT_TABLE_DEVICE: str(device_id)})
                    enrollment.set_enrolled(enrollment_id)
                    enrolled_success = True

                else:
                    # print 'user_id = ' + user_id
                    device_dict = {c.DEVICE_TABLE_USER: user_id,
                                   c.DEVICE_TABLE_OS: 'ios',
                                   c.DEVICE_TABLE_UDID: str(self.udid),
                                   c.DEVICE_TABLE_DELETED: False}
                    device_id = device.add_device(device_dict)
                    if device_id is None:
                        log.e(TAG,
                              'Not Able to insert in Device table UDID = '
                              + str(self.udid) + 'userID = ' + str(user_id))
                    else:
                        device_details_dict_new = {}
                        device_details_dict_new[
                            c.DEVICE_DETAILS_TABLE_DEVICE] = device_id
                        device_details_dict_new[
                            c.DEVICE_DETAILS_TABLE_EXTRAS] = device_details_dict
                        device_details_id = device_detail.add_device_detail(
                            device_details_dict_new)

                        # print 'device_details_id = ' + str(device_details_id)
                        if device_details_id is None:
                            log.e(TAG, 'Not Able to insert in Device Details \
                                  table UDID = ' +
                                  str(self.udid) +
                                  'userID = ' +
                                  str(user_id) +
                                  'DeviceID = ' +
                                  str(device_id))
                        else:

                            success = enrollment.update_enrollment(
                                enrollment_id,
                                {c.ENROLLMENT_TABLE_DEVICE: str(device_id)})
                            if not success:
                                log.e(TAG,
                                      'enrollment device table not linked')
                            else:
                                success1 = enrollment.set_enrolled(
                                    enrollment_id)

                                if success1:
                                    enrolled_success = True
                                else:
                                    log.e(
                                        TAG,
                                        'EnrolledOn time is not updated in \
the Enrollment Table')

                if device_id and enrolled_success:

                    violation_status = violation.update_violations(
                        str(device_id))
                    user = UserDBHelper()
                    user_info = user.get_user(user_id)
                    if violation_status:
                        log.i(TAG,
                              "Violation table updated for device_id" + str(
                                  device_id))
                    else:
                        log.e(
                            TAG,
                            "Violation table not updated for device_id" +
                            str(device_id))

                    ### Add task to Queue for celery Worker. ###
                    json_data = {'to': 'user', 'action': 'device_information',
                                 'id': user_id}
                    json_data['company_id'] = user_info.get('company_id')

                    create_command_handler_task.delay(json_data)

                    ### Now send polling Signal to device ###
                    wrapper = APNSNotificationWrapper(
                        '/opt/toppatch/assets/ios/PushCert.pem', False)
                    message = APNSNotification()
                    message.appendProperty(APNSProperty("mdm",
                                                        str(self.push_magic)))
                    message.tokenBase64(str(self.device_token))
                    wrapper.append(message)
                    wrapper.notify()

                    print 'Payload Sent'

        elif device_data.get('MessageType') == 'CheckOut':
            reply = """
                    <html>
                        <body>401</body>
                    </html>
                    """
            self.request.set_status(401)
            self.request.write(reply)
            ioloop.IOLoop.instance().add_callback(self.callback)

            violation = ViolationsDBHelper()
            device = DeviceDBHelper()
            enrollment = EnrollmentDBHelper()
            devices = device.get_device_with_udid(self.udid)
            if devices is None:
                log.e(TAG, 'No User ID Associated with Device UDID = '
                           + self.udid)
            else:
                device_id = devices[0][c.DEVICE_TABLE_ID]
                violation_id = violation.add_violation(str(device_id))
                if violation_id is None:
                    log.e(TAG, 'Not able to insert in Violation Table.\
                               DeviceID = ' + str(device_id))
                else:
                    device.delete_device(device_id)
                    enrollment.update_enrollment(
                        str(enrollment_id), {
                            'device_id': "null", 'is_enrolled': False})
                    log.i(TAG, 'Violation added for device id = ' +
                               str(device_id))
                    admin_mailer(device_id, violation_id)

        else:
            reply = """
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
             "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                                <plist version="1.0">
                                <dict>
                                </dict>
                                </plist>
            """
            print 'outer write'
            self.request.write(reply)
            ioloop.IOLoop.instance().add_callback(self.callback)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/checkin", CheckInRequestHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
