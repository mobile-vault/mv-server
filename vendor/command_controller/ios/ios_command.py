import json
import time
import datetime
import uuid
# import ipdb
from APNSWrapper import *
from vendor.command_controller.engine import Engine
from vendor.command_controller.ios.ios_policy_mapper import get_mapped_policy
from db.constants import Constants as c
from db.helpers.device_details import DeviceDetailsDBHelper
from db.helpers.ioscommand import IOSCommandDBHelper
from logger import Logger
from db.helpers.logs import *


class IosCommand(Engine):

    def execute(self, policy_dict, device_id, device_udid, *args, **kwargs):

        self.log = Logger('CommandHandler')
        command = IOSCommandDBHelper()

        broadcast_message = None

        '''
        Send Commands to iOS
        '''
        self.TAG = 'commandToIOS'
        '''
        mapped policy will give dict('policy', 'erase_device',
        'install_application', 'remove_application')
        '''

        if 'action_command' in policy_dict:
            ios_mapped_policy = {policy_dict.get('action_command'): True}

        elif 'broadcast_command' in policy_dict:
            broadcast_message = policy_dict.get('broadcast_command')

        else:
            ios_mapped_policy = get_mapped_policy(policy_dict)

        action = {}

        print 'Sending Payload for Polling'
        self.device_id = device_id
        device_details = DeviceDetailsDBHelper()
        self.udid = device_udid

        print 'device_id ' + str(device_id)
        print 'getting device details'
        device_details_list = device_details.get_device_details(device_id)
        # print device_details_list
        json_extras = device_details_list.get(c.DEVICE_DETAILS_TABLE_EXTRAS)

        '''
        self.push_magic = 'push_magic'
        self.device_token = 'token'
        self.message_token = 'message_token'
        '''

        self.push_magic = str(json_extras.get('push_magic'))
        self.device_token = str(json_extras.get('token'))
        self.message_token = str(json_extras.get('message_token'))

        if broadcast_message and self.udid and self.message_token != 'None':
            # create wrapper
            wrapper = APNSNotificationWrapper(
                '/opt/toppatch/assets/ios/ckProd.pem',
                True)

            # create message
            message = APNSNotification()
            message.tokenHex(self.message_token)

            message_text = str(broadcast_message)
            # just add alert text
            message.alert(message_text)

            # enable sound (default sound if no argument)
            message.sound()

            # add message to tuple and send it to APNS server
            wrapper.append(message)
            wrapper.notify()
            print '\nios Broadcast message sent\n'

            return

        elif broadcast_message and self.message_token == 'None':
            return

        elif all(x != 'None' for x in (self.push_magic, self.device_token,
                                       self.udid)):
            for ios_action in ios_mapped_policy.keys():
                action[ios_action] = ios_mapped_policy.get(ios_action)

            if action.get('install_application'):
                print "date time is \n ", datetime.datetime.now()
                current_time = datetime.datetime.utcnow()
                special_uuid = '77777777-7777-7777-7777-777777777777' + \
                    self.device_id
                installed_apps_query = command.get_result(special_uuid)
                installed_apps = None

                if installed_apps_query:
                    installed_apps_query = installed_apps_query[0]
                    executed_time = installed_apps_query.get('executed_on')

                if (installed_apps_query and
                    installed_apps_query.get('result')
                    and (current_time - executed_time) < datetime.timedelta(
                        minutes=15)):

                    installed_apps = installed_apps_query.get('result')

                if installed_apps:
                    policy_app_list = action.get('install_application')

                    if isinstance(installed_apps, str):
                        installed_apps = json.loads(installed_apps)
                    print '\n\n print install app here ...\n\n', installed_apps
                    pre_install_apps = [
                        x.get('Identifier') for x in installed_apps]
                    to_install_apps = [
                        x.get('app_identifier') for x in policy_app_list]
                    final_apps = list(set(to_install_apps).difference(
                        set(pre_install_apps)))

                    if len(final_apps) > 0:
                        send_install = True
                    else:
                        send_install = False

                    if send_install:
                        final_apps_list = []

                        for identifier in policy_app_list:
                            if identifier.get('app_identifier') in final_apps:
                                final_apps_list.append(identifier)

                        for apps in iter(final_apps_list):
                            command_list = []
                            attribute = [{'app_id': apps.get('id')}]
                            command_list.append('install_application')
                            command_list.append(json.dumps(attribute))
                            command_list.append(device_id)
                            status = self.save_ios_command(command_list)
                            print 'status of pooling to device: ', status
                            time.sleep(31)

                else:
                    command_list = []
                    attribute = [{'message': 'installed_application_list'}]
                    command_list.append('installed_application_list')
                    command_list.append(json.dumps(attribute))
                    command_list.append(device_id)
                    command_list.append(special_uuid)
                    status = self.save_ios_command(command_list)
                    print 'status of pooling to device: ', status

            if action.get('remove_application'):
                for apps in iter(action.get('remove_application')):
                    command_list = []
                    attribute = [{'app_identifier': str(apps)}]
                    command_list.append('remove_application')
                    command_list.append(json.dumps(attribute))
                    command_list.append(device_id)
                    status = self.save_ios_command(command_list)
                    print 'status of pooling to device: ', status
                    # time.sleep(32)

            if action.get('erase_device'):
                command_list = []
                special_uuid = '2929292929-29292929-292929-292929-292929' +\
                    self.device_id
                attribute = [{'message': 'erasing your device'}]
                command_list.append('erase_device')
                command_list.append(json.dumps(attribute))
                command_list.append(device_id)
                command_list.append(special_uuid)
                status = self.save_ios_command(command_list)

                print 'status of pooling to device: ', status
                # time.sleep(31)

            if action.get('device_information'):
                special_uuid = '55555555-5555-5555-5555-555555555555' +\
                    self.device_id
                command_list = []
                attribute = [{'message': 'device_information'}]
                command_list.append('device_information')
                command_list.append(json.dumps(attribute))
                command_list.append(device_id)
                command_list.append(special_uuid)
                status = self.save_ios_command(command_list)
                print 'status of pooling to device: ', status
                # time.sleep(31)

            if action.get('clear_passcode'):
                command_list = []
                attribute = [{'message': 'clear passcode of the device'}]
                command_list.append('clear_passcode')
                command_list.append(json.dumps(attribute))
                command_list.append(device_id)
                status = self.save_ios_command(command_list)
                print 'status of pooling to device: ', status
                # time.sleep(31)

            if action.get('device_lock'):
                command_list = []
                attribute = [{'message': 'locking the device'}]
                command_list.append('device_lock')
                command_list.append(json.dumps(attribute))
                command_list.append(device_id)
                status = self.save_ios_command(command_list)
                print 'status of pooling to device: ', status
                # time.sleep(31)

            if action.get('installed_application_list'):
                special_uuid = '77777777-7777-7777-7777-777777777777' + \
                    self.device_id
                command_list = []
                attribute = [{'message': 'installed_application_list'}]
                command_list.append('installed_application_list')
                command_list.append(json.dumps(attribute))
                command_list.append(device_id)
                command_list.append(special_uuid)
                status = self.save_ios_command(command_list)
                print 'status of pooling to device: ', status
                # time.sleep(131)

            if action.get('policy'):
                policy = {}
                for key in action['policy'].keys():
                    policy[key] = action['policy'][key]

                if policy.get('restriction'):
                    command_list = []
                    attribute = [{'type': 'restrictions',
                                  'data': policy.get('restriction')}]
                    command_list.append('policy')
                    command_list.append(json.dumps(attribute))
                    command_list.append(device_id)
                    status = self.save_ios_command(command_list)
                    print 'status of pooling to device: ', status
                    # time.sleep(31)

                if policy.get('wifi'):
                    # for wifi_set in policy.get('wifi'):
                    command_list = []
                    attribute = [{'type': 'wifi', 'data': policy.get('wifi')}]
                    command_list.append('policy')
                    command_list.append(json.dumps(attribute))
                    command_list.append(device_id)
                    status = self.save_ios_command(command_list)
                    print 'status of pooling to device: ', status
                    # time.sleep(31)

                if policy.get('vpn'):
                    # for vpn_set in policy.get('vpn'):
                    command_list = []
                    attribute = [{'type': 'vpn', 'data': policy.get('vpn')}]
                    command_list.append('policy')
                    command_list.append(json.dumps(attribute))
                    command_list.append(device_id)
                    status = self.save_ios_command(command_list)
                    print 'status of pooling to device: ', status
                    # time.sleep(31)

        else:
            self.log.e(self.TAG, 'Either Push Magic or Device Token not found \
                                can\'t send command')
            return
            # ipdb.set_trace()

    def save_ios_command(self, command_list):

        command = IOSCommandDBHelper()
        ## Save the command in Commad table with UUID##############
        ##### This may get changed ##################
        command_zip = (c.COMMAND_TABLE_ACTION, c.COMMAND_TABLE_ATTRIBUTE,
                       c.COMMAND_TABLE_DEVICE, c.COMMAND_TABLE_COMMAND_UUID)

        if len(command_list) == 3:
            command_list.append(str(uuid.uuid4()))

        command_dict = dict(zip(command_zip, command_list))
        print command_dict

        device_id = command_dict.get(c.COMMAND_TABLE_DEVICE)
        special_uuid = command_dict.get('command_uuid')

        special_uuid_list = [
            '55555555-5555-5555-5555-555555555555' +
            device_id,
            '77777777-7777-7777-7777-777777777777' +
            device_id,
            '2929292929-29292929-292929-292929-292929' +
            device_id]

        if special_uuid in special_uuid_list:
            uuid_results = command.get_command_attributes(special_uuid)

            if uuid_results:
                command.toggle_executed(str(special_uuid), str(device_id),
                                        False)
                command_id = True
            else:
                command_id = command.add_command(command_dict)

        else:
            command_id = command.add_command(command_dict)

        if command_id is None:
            self.log.e(self.TAG, 'Can\'t insert in command table')
            return None
        else:
            self.insert = False
            wrapper = APNSNotificationWrapper(
                '/opt/toppatch/assets/ios/PushCert.pem', False)
            message = APNSNotification()
            message.appendProperty(APNSProperty("mdm", self.push_magic))
            message.tokenBase64(str(self.device_token))
            # print "Push Magic : {0}".format(self.push_magic)
            # print "device token : {0}".format(self.device_token)
            wrapper.append(message)
            wrapper.notify()
            print 'Payload Sent'
            return True
