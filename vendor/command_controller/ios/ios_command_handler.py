'''
This program will get the commands from ios_command table and Sends to the
device.
https://demo-mdm.toppatch.com/command/ios
'''

import base64
import cgi
import threading

import tornado.ioloop
import tornado.ioloop as ioloop

import tornado.web
from tornado.web import asynchronous
from APNSWrapper import *
from vendor.command_controller.ios.ios_command_creator import IOSCommandCreatorThread
from db.constants import Constants as c
from db.helpers.device import DeviceDBHelper
from db.helpers.device_details import DeviceDetailsDBHelper
from db.helpers.ioscommand import IOSCommandDBHelper
from logger import Logger
from db.helpers.user import UserDBHelper
from db.helpers.violations import ViolationsDBHelper
from db.helpers.enrollment import EnrollmentDBHelper
from tasks import create_command_handler_task
from lxml import etree
from lxml import objectify
'''
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
'''


class IOSCommandHandler(tornado.web.RequestHandler):
    json_dict = {}

    def callback(self):
        self.finish("Finished happened in main IOSCommandHandler")

    @asynchronous
    def put(self):
        IOSCommandPerformer(request=self, callback=self.callback).start()


class IOSCommandPerformer(threading.Thread):
    def __init__(self, callback, request=None, *args, **kwargs):
        super(IOSCommandPerformer, self).__init__(*args, **kwargs)
        self.request = request
        self.callback  = callback
        self.log = Logger('IOSCommandPerformer')
        self.callback =callback

    def run(self):
        TAG = 'run'

        print ' In IOSCommandPerformer\'s PUT'
        command = IOSCommandDBHelper()
        invoke_flag = False
        arguments = cgi.parse_qsl(self.request.request.body)
        intermediate = arguments[0]
        currentxml = intermediate[1]
        final = currentxml[25:-1]   ###Original Line
#         final = currentxml[20:]  ### For testing only
        #print '\n\n\n here is final xml \n\n', final
        ##temp Parsing
        #tree = ET.ElementTree(ET.fromstring(final))  ##Original Line
#       tree = ET.parse('temp.xml')   ### For testing only
        initial_list = []
        initial_dict = {}

        check_out_requested = False
        send_command = False
        store_result = False
        store_error = False
        registered = True
        special_result = False
        acknowledged = False
        update_token = False

        object_root = objectify.fromstring(final)

        begin = object_root.dict

        for child in begin.iterchildren():
            initial_list.append(child.text)

        initial_dict = dict(zip(initial_list[::2], initial_list[1::2]))
        #print '\n\n print here initial dict\n', initial_dict


        if initial_dict.has_key('UDID'):
            udid = initial_dict.get('UDID')
            device = DeviceDBHelper()
            registered = device.is_udid_registered(str(udid))



        if initial_dict.has_key('Status'):
            status = initial_dict.get('Status')
            if status == 'Idle':
                send_command = True
            elif status == 'Acknowledged':
                acknowledged = True
            elif status == 'Error':
                store_error = True
                uuid = initial_dict.get('CommandUUID')

        if initial_dict.has_key('MessageType'):
            message = initial_dict.get('MessageType')
            if message == 'TokenUpdate':
                update_token = True
            elif message == 'CheckOut':
                check_out_requested = True
        push_magic = 'push_magic'
        token = 'Token'
        unlock_token = 'UnlockToken'


        if registered is False:
            reply = """

                    """
            self.request.set_status(401)
            self.request.write(reply)
            ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            device_id = str(device.get_device_with_udid(udid)[0]['id'])
            print  'reached here '
        if acknowledged:
            if initial_dict.has_key('CommandUUID'):
                uuid = initial_dict.get('CommandUUID')
                # special uuid for device information
                if uuid == '55555555-5555-5555-5555-555555555555'+ device_id:
                    info_list = [el.text if el.text else el.tag for el in object_root.iterdescendants()]
                    info_list.pop(0)
                    final = dict(zip(info_list[::2], info_list[1::2]))
                    store_result = True
                    special_result = True
                # special uuid for installed application list
                elif uuid == '77777777-7777-7777-7777-777777777777'+ device_id:
                    begin = object_root.dict.array
                    apps_list = []
                    for outer_child in begin.iterchildren():
                        temp_list = []
                        for inner_child in outer_child.iterchildren():
                            temp_list.append(inner_child.text)
                        apps_list.append(dict(zip(temp_list[::2],
                             temp_list[1::2])))
                    final = apps_list
                    store_result = True
                    invoke_flag = True
                else:
                    store_result=True


        if send_command:
            if udid is None:
                self.log.e(TAG, 'No UDID is supplied from the device')
            else:

                command_list = command.get_not_executed(str(device_id))
                if command_list is None or len(command_list) == 0:
                    self.log.e(TAG, 'No command to execute fot the device \
                               having ID = ' + str(device_id))
                    reply = " "
                    print 'outer write'
                    self.request.set_status(500)
                    self.request.write(reply)
                    ioloop.IOLoop.instance().add_callback(self.callback)

                else:

                    device_details = DeviceDetailsDBHelper()
                    violate_device = False
                    special_uuid = '2929292929-29292929-292929-292929-292929'+\
                                    str(device_id)

                    commands = command_list[0]
                    action = str(commands[c.COMMAND_TABLE_ACTION])
                    command_attributes = commands[c.COMMAND_TABLE_ATTRIBUTE]
                    command_uuid = str(commands[c.COMMAND_TABLE_COMMAND_UUID])

                    if command_uuid == special_uuid:
                        violate_device = True


                    if action is not None and not violate_device:
                        command_xml_thread = IOSCommandCreatorThread(action,
                        command_attributes, command_uuid, device_id)
                        command_xml_thread.start()
                        command_xml_thread.join()
                        final_output = command_xml_thread.command_profile
                        if final_output is not None:
                            self.request.write(final_output)
                        ioloop.IOLoop.instance().add_callback(self.callback)
                        ## send polling signal to device for next command
                        device_details_list = device_details.get_device_details(device_id)
                        json_extras = device_details_list.get(c.DEVICE_DETAILS_TABLE_EXTRAS)

                        self.push_magic = str(json_extras.get('push_magic'))
                        self.device_token = str(json_extras.get('token'))
                        wrapper = APNSNotificationWrapper(
                            '/opt/toppatch/assets/ios/PushCert.pem', False)
                        message = APNSNotification()
                        message.appendProperty(APNSProperty("mdm", self.push_magic))
                        message.tokenBase64(str(self.device_token))
                        wrapper.append(message)
                        wrapper.notify()
                        print 'Payload Sent'

                    elif violate_device:
                        ### Wiping device to Factory Reset ###
                        command_xml_thread = IOSCommandCreatorThread(action,
                        command_attributes, command_uuid, device_id)
                        command_xml_thread.start()
                        command_xml_thread.join()
                        final_output = command_xml_thread.command_profile
                        if final_output is not None:
                            self.request.write(final_output)
                        ioloop.IOLoop.instance().add_callback(self.callback)

                        violation = ViolationsDBHelper()
                        enrollment = EnrollmentDBHelper()
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
                                enrollment.update_enrollment(str(enrollment_id),
                                {'device_id': "null", 'is_enrolled': False})
                            self.log.i(TAG, 'Violation added for device id = ' + \
                                str(device_id)+ 'due to remote wipe command')
                    else:
                        reply = " "
                        print 'outer write'
                        self.request.set_status(500)
                        self.request.write(reply)
                        ioloop.IOLoop.instance().add_callback(self.callback)


        elif check_out_requested:
            violation = ViolationsDBHelper()
            device = DeviceDBHelper()

            devices = device.get_device_with_udid(udid)
            if devices is None:
                self.log.e(TAG, 'No User ID Associated with Device UDID = '\
                           + udid)
            else:
                device_id = str(devices[0][c.DEVICE_TABLE_ID])
                violation_id = violation.add_violation(device_id)
                if violation_id == None:
                    self.log.e(TAG, 'Not able to insert in Violation Table.\
                               DeviceID = ' + str(device_id))
                else:
                    self.log.i(TAG, 'Violation added for device id = ' + \
                               str(device_id))

            reply = """

                    """
            self.request.set_status(401)
            self.request.write(reply)
            ioloop.IOLoop.instance().add_callback(self.callback)

        elif store_result or store_error:
            if special_result:
                is_updated = device.update_device(str(device_id),
                        {c.DEVICE_TABLE_OS_VERSION: str(
                            final.get('OSVersion'))})
                if not is_updated:
                    self.log.e(TAG, 'Not able to set the version of the device\
                    udid = ' + str(udid) + " Device id = " + str(device_id))
                else:
                    self.log.i(TAG, 'Version Set for the device udid = '\
                               + str(udid) + " Device id = " + str(device_id))

            if store_error:
                self.log.e(TAG, 'Error in Response for uuid = ' + \
                           str(uuid) + ' device_id = ' + str(device_id))
            #print '\n\nfinal dict to be stored as json is \n\n', final
            result_updated = command.update_result(str(uuid),
                                                   str(device_id), final)
            reply = """
                                <?xml version="1.0" encoding="UTF-8"?>
                                <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
                                 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                                <plist version="1.0">
                                <dict>
                                </dict>
                                </plist>
                    """
            self.request.write(reply)
            ioloop.IOLoop.instance().add_callback(self.callback)
            if not result_updated:
                self.log.e(TAG, 'Result Not updated for uuid = ' +  \
                           str(uuid) + ' udid = ' + str(udid))
            else:
                executed = command.toggle_executed(str(uuid), str(device_id),
                                                   True)
                if executed is False:
                    self.log.e(TAG, 'IOSCommand Table executed \
                            field is not updated CommandUUID = '+ \
                        str(uuid) + 'Device id = ' + str(device_id))

                self.log.i(TAG, 'Result send in DB for uuid = ' + \
                           str(uuid) + ' udid = ' + str(udid))

                if invoke_flag:
                    ### Queue task to send command to user of app installation
                    user = UserDBHelper()
                    user_id = device.get_device_with_udid(str(
                                                udid))[0]['user_id']
                    user_info = user.get_user(str(user_id))
                    json_data = {'to': 'user', 'id': user_id}
                    json_data['company_id'] = user_info.get('company_id')
                    create_command_handler_task.delay(json_data)



        elif update_token == True:
            device = DeviceDBHelper()
            device_list = device.get_device_with_udid(udid)

            device_id = 'device_id'
            if device_list is not None and len(device_list) != 0:
                for devices in device_list:
                    device_id = devices[c.DEVICE_TABLE_ID]
                    if device_id is None:
                        self.log.e(TAG, 'Device id is not found corresponding \
                                   the udid = ' + str(udid))
                    else:
                        device_details = DeviceDetailsDBHelper()
                        device_details_dict = {
                                c.DEVICE_DETAILS_TABLE_DEVICE_TOKEN: token,
                                c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: push_magic,
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: unlock_token
                                    }
                        is_updated = device_details.update_device_details(
                            str(device_id), device_details_dict)
                        if is_updated == False:
                            self.log.e(TAG, 'Not able to update the device \
                                    details of device_id = ' + str(device_id))
                        else:
                            self.log.i(TAG, 'Device Details successfully \
                                       updated device id = ' + str(device_id))

                        reply = """
                                <?xml version="1.0" encoding="UTF-8"?>
                                <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
                                 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                                <plist version="1.0">
                                <dict>
                                </dict>
                                </plist>
                                """
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
            print 'outer write'
            self.request.write(reply)
            ioloop.IOLoop.instance().add_callback(self.callback)
