import json
import threading
import tornado.ioloop as ioloop

import tornado.web
from tornado.web import asynchronous

from db.constants import Constants as c
from db.helpers.device import DeviceDBHelper
from db.helpers.violations import ViolationsDBHelper
from db.helpers.enrollment import EnrollmentDBHelper
from db.helpers.samsung_command import SamsungCommandsDBHelper
from logger import Logger
from handlers.admin_mailer import admin_mailer


class SamsungCommandResultHandler(tornado.web.RequestHandler):
    json_dict = {}

    def callback(self):
        self.finish()

    @asynchronous
    def put(self):
        SamsungCommandResult(request=self, callback=self.callback).start()


class SamsungCommandResult(threading.Thread):

    def __init__(self, callback, request=None, *args, **kwargs):
        super(SamsungCommandResult, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.log = Logger('SamsungCommandResult')
        self.callback = callback

    def run(self):
        TAG = 'run'

        print ' In SamsungCommandResult\'s PUT'
        command = SamsungCommandsDBHelper()

        print "here is the response \n", self.request.request.body
        json_dict = json.loads(self.request.request.body)

        special_result = False
        checkout_result = False
        result_updated = False

        special_uuid = '1717171717-17171717-1717117-1717'
        checkout_uuid = '1919191919-19191919-191919-1919'

        command_uuid = str(json_dict.get('command_uuid'))
        gcm_id = json_dict.get('gcm_id')
        imei = json_dict.get('imei')

        if special_uuid in command_uuid:
            special_result = True

        if checkout_uuid in command_uuid:
            checkout_result = True

        device = DeviceDBHelper()
        device_list = device.get_device_with_udid(str(imei))

        print "\n device list here \n", device_list
        command_result = json_dict.get('result')

        if checkout_result:

            violation = ViolationsDBHelper()
            enrollment = EnrollmentDBHelper()
            if device_list is None:
                self.log.e(TAG, 'No User ID Associated with Device gcm_id = '
                           + gcm_id)
            else:
                device_id = device_list[0][c.DEVICE_TABLE_ID]
                violation_id = violation.add_violation(str(device_id))
                if violation_id is None:
                    self.log.e(TAG, 'Not able to insert in Violation Table.\
                               DeviceID = ' + str(device_id))
                else:
                    device.delete_device(device_id)
                    enrollment_list = enrollment.get_enrollments({
                        'device_id': device_id})
                    for enroll in enrollment_list:
                        enrollment_id = enroll.get('id')
                        enrollment.update_enrollment(
                            str(enrollment_id), {
                                'device_id': "null", 'is_enrolled': False})
                    self.log.i(TAG, 'Violation added for device id = ' +
                               str(device_id))
                    admin_mailer(device_id, violation_id)

            result_updated = True

        elif special_result:
            os_version = command_result.get('device_platform')
            os_version = os_version.replace('Android', '').strip()

            if device_list is None:
                device_list = []

            for unique_device in device_list:
                device_id = unique_device.get(c.DEVICE_TABLE_ID)
                is_updated = device.update_device(
                    str(device_id), {
                        c.DEVICE_TABLE_OS_VERSION: str(os_version)})
                if not is_updated:
                    self.log.e(TAG, 'Not able to set the version of the \
device gcm_id = ' + str(gcm_id) + " Device id = " + str(device_id))

                else:
                    self.log.i(
                        TAG,
                        'Version Set for the device gcm_id = ' +
                        str(gcm_id) +
                        " Device id = " +
                        str(device_id))

                result_updated = command.update_result(
                    str(command_uuid),
                    str(device_id),
                    command_result)
        else:
            if device_list is None:
                device_list = []

            for unique_device in device_list:
                device_id = unique_device.get(c.DEVICE_TABLE_ID)
                result_updated = command.update_result(
                    str(command_uuid),
                    str(device_id),
                    command_result)

        if not result_updated:
            self.log.e(TAG, 'Result Not updated for uuid = ' +
                       str(command_uuid) + 'gcm_id = ' + str(gcm_id))

            self.request.set_status(404)
            self.request.write("Not OK")
            ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            self.log.i(TAG, 'Result send in DB for uuid = ' +
                       str(command_uuid) + 'gcm_id = ' + str(gcm_id))
            self.request.set_status(200)
            self.request.write("OK")
            ioloop.IOLoop.instance().add_callback(self.callback)
