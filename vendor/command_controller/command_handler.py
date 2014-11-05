import json
'''
from os.path import abspath, dirname
from sys import path
ROOT = dirname(dirname(dirname(abspath(__file__))))
path.append(ROOT)
'''

from APNSWrapper import *
from vendor.command_controller.command_merger import Merger
from db.constants import Constants as c
from db.helpers.company import CompanyDBHelper
from db.helpers.device import DeviceDBHelper
# from db.helpers.device_details import DeviceDetailsDBHelper
from db.helpers.ioscommand import *
from db.helpers.logs import *
from db.helpers.role import RoleDBHelper
from db.helpers.team import TeamDBHelper
from db.helpers.user import UserDBHelper
from vendor.command_controller.android import android_command
from vendor.command_controller.ios import ios_command


# iOSCommandURL = 'https://mdm.toppatch.com/command/ios'
# samsungCommandURL = 'https://mdm.toppatch.com/command/samsung'


class CommandPerformer():
    insert = True

    def __init__(self, json_data, callback=None, *args, **kwargs):
        self.callback = callback
        self.log = Logger('CommandHandler')
        self.data = json_data

    def perform(self):
        TAG = 'run'
        print 'In RuN'
        self.insert = True
        json_data = self.data
        print json_data['to']
        # Find out the category of the Device on the basis of 'to' field
        # Case 1 : Command is sent to the USER
        if str(json_data['to']) == 'user':
            to_id = str(json_data['id'])
            company_id = json_data.get('company_id')
            user = UserDBHelper()
            user_dict = user.get_user(str(to_id), company_id=company_id,
                                      pluck=[c.USER_TABLE_NAME])
            if user_dict is not None:
                user_name = str(user_dict[c.USER_TABLE_NAME])
                message = "Command sent to " + user_name +\
                    "  having ID = " + str(json_data['id'])
                logs = LogsDBHelper()
                logs_id = logs.add_log(to_id,
                                       str(json_data['to']),
                                       'info',
                                       None,
                                       message,
                                       raw=None,
                                       company=str(company_id))
                if logs_id is None:
                    self.log.e(TAG, 'Not able to insert the logs')
                self.command_to_user(json_data)
            else:
                self.log.e(TAG, 'No details corresponding to user found')

        # Case 2: Command is sent to the Teams
        elif str(json_data['to']) == 'team':
            print 'sending to teams'
            team_id = str(json_data['id'])
            company_id = json_data.get('company_id')
            team = TeamDBHelper()
            team_dict = team.get_team(str(team_id), company_id=company_id,
                                      pluck=[c.TEAM_TABLE_NAME])
            if team_dict is not None:
                team_name = str(team_dict[c.TEAM_TABLE_NAME])

                message = "Command sent to " + team_name +\
                    "  having ID = " + str(json_data['id'])
                logs = LogsDBHelper()
                logs_id = logs.add_log(team_id,
                                       str(json_data['to']),
                                       'info',
                                       None,
                                       message,
                                       raw=None,
                                       company=str(company_id))
                if logs_id is None:
                    self.log.e(TAG, 'Not able to insert the logs')
                self.command_to_team(json_data)
            else:
                self.log.e(TAG, "No details corresponding to team_id found. ")

        # Case 3: Command is sent to the Role
        elif str(json_data['to']) == 'role':
            role_id = str(json_data['id'])
            company_id = json_data.get('company_id')
            role = RoleDBHelper()
            role_dict = role.get_role(str(role_id), company_id=company_id,
                                      pluck=[c.ROLE_TABLE_NAME])
            if role_dict is not None:
                role_name = str(role_dict[c.ROLE_TABLE_NAME])

                message = "Command sent to " + role_name +\
                    "  having ID = " + str(json_data['id'])
                logs = LogsDBHelper()
                logs_id = logs.add_log(role_id,
                                       str(json_data['to']),
                                       'info',
                                       None,
                                       message,
                                       raw=None,
                                       company=str(company_id))
                if logs_id is None:
                    self.log.e(TAG, 'Not able to insert the logs')
                self.command_to_role(json_data)
            else:
                self.log.e(TAG, 'No role corresponding to given role_id found')

        elif str(json_data['to']) == 'company':
            company_id = str(json_data['id'])
            company = CompanyDBHelper()
            company_dict = company.get_company(str(company_id))
            if company_dict is not None:
                company_name = str(company_dict[c.COMPANY_TABLE_NAME])

                message = "Command sent to " + company_name\
                    + "  having ID = " + str(json_data['id'])
                logs = LogsDBHelper()
                logs_id = logs.add_log(company_id,
                                       str(json_data['to']),
                                       'info',
                                       None,
                                       message,
                                       raw=None,
                                       company=company_id)
                if logs_id is None:
                    self.log.e(TAG, 'Not able to insert the logs')

                self.command_to_company(json_data)
            else:
                self.log.e(TAG, 'No data corresponding to team id given found')

        # Case 5: Some other parameter sent in 'to' field
        else:
            self.log.e(TAG, 'Somthing wrong with \'to\' field of POST data')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False, 'error': 'Correct TO field'})
            self.log.e(TAG, str(opJson))

#################### Handles Commands sent to User    #####################
    def command_to_user(self, json_data):
        TAG = 'command_to_user'
        print 'In command_to_user'
        user_table_id = ''
        try:
            user_table_id = str(json_data['id'])
            print user_table_id
        except:
            self.log.e(
                TAG,
                'There is something wrong in the POST parametes sent')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False,
                                 'error': 'UserID not found in request'})
            self.log.e(TAG, str(opJson))
            return
        device = DeviceDBHelper()
        merger = Merger()
        print 'find device List'
        print user_table_id
        device_list = device.get_devices_of_user(user_table_id)

        print 'find device List found'
        if device_list is None:
            self.log.e(TAG, 'Device List is Empty')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False, 'error': 'Device list empty'})
            self.log.e(TAG, str(opJson))
            return

        print device_list
        for device_item in device_list:
            device_os = str(device_item[c.DEVICE_TABLE_OS])
            device_id = str(device_item[c.DEVICE_TABLE_ID])
            device_udid = str(device_item[c.DEVICE_TABLE_UDID])

            if 'action' in json_data:
                policy_dict = {'action_command': json_data.get('action'),
                               'passcode': json_data.get('passcode')}
            elif 'broadcast' in json_data:
                policy_dict = {'broadcast_command': json_data.get('broadcast')}
            else:
                policy_dict = merger.merge(device_id)
            # Now Send the parameters to the Corresponding engine
            # Send the command to iOS Engine
            if str(device_os) == 'ios':
                print 'Now command sending to ios. Add to queue. Device id= '\
                    + device_id
                command_instance = ios_command.IosCommand()
                command_instance.execute(policy_dict, device_id, device_udid)
                #create_ios_task.delay(policy_dict, device_id, device_udid)
                opJson = json.dumps({'pass': True,
                                     'message': 'Message sent from server'})
                self.log.i(TAG, str(opJson))

            # Send the command to Samsung Engine
            elif device_os == 'samsung':
                print 'Now command sending to samsung'
                command_instance = android_command.AndroidCommand()
                command_instance.execute(policy_dict, device_id)
                #create_android_task.delay(json_data, device_id)
                opJson = json.dumps({'pass': True,
                                     'message': 'Message sent from server'})
                self.log.i(TAG, str(opJson))

            # Wrong device_os
            else:
                self.log.e(TAG, 'Wrong Device OS in the Device Table')
                # Create the O/P JSON
                opJson = json.dumps(
                    {'pass': False,
                        'error': 'Wrong Device OS for this device'})
                self.log.e(TAG, str(opJson))

################# Handles Commands sent to Team #################
    def command_to_team(self, json_data):
        TAG = 'command_to_team'
        print 'In ' + str(TAG)
        team_table_id = 'team_table_id'
        try:
            team_table_id = str(json_data['id'])
        except Exception as err:
            self.log.e(
                TAG,
                'There is something wrong in the POST parametes sent' +
                repr(err))
            # Create the O/P JSON
            opJson = json.dumps({'pass': False,
                                 'error': 'TeamID not found in request'})
            self.log.e(TAG, str(opJson))
            return

        print 'team_table_id ' + team_table_id
        # Finding the team_table_id from TeamTable using TeamName
#         team = TeamDBHelper()
        device = DeviceDBHelper()
        merger = Merger()
        device_list = device.get_devices_of_team(team_table_id)
        print device_list
        if device_list is None:
            self.log.e(TAG, 'Device List is Empty')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False, 'error': 'Device list empty'})
            self.log.e(TAG, str(opJson))
            return

        for device_item in device_list:
            device_os = str(device_item[c.DEVICE_TABLE_OS])
            device_id = str(device_item[c.DEVICE_TABLE_ID])
            device_udid = str(device_item[c.DEVICE_TABLE_UDID])

            if 'action' in json_data:
                policy_dict = {'action_command': json_data.get('action'),
                               'passcode': json_data.get('passcode')}
            elif 'broadcast' in json_data:
                policy_dict = {'broadcast_command': json_data.get('broadcast')}
            else:
                policy_dict = merger.merge(device_id)

            # Now Send the parametes to the Corresponding the engine
            # Send the command to iOS Engine
            print device_os
            if device_os == 'ios':
                command_instance = ios_command.IosCommand()
                command_instance.execute(policy_dict, device_id, device_udid)
                #create_ios_task.delay(policy_dict, device_id, device_udid)
                opJson = json.dumps({'pass': True, 'message': 'Message sent\
                                     from server'})
                self.log.e(TAG, str(opJson))

            # Send the command to Samsung Engine
            elif device_os == 'samsung':
                command_instance = android_command.AndroidCommand()
                command_instance.execute(policy_dict, device_id)
                #create_android_task.delay(json_data, device_id)
                opJson = json.dumps(
                    {'pass': True, 'message': 'Message sent from server'})
                self.log.e(TAG, str(opJson))

            # Wrong device_os
            else:
                self.log.e(TAG, 'Wrong Device OS in the Device Table')
                # Create the O/P JSON
                opJson = json.dumps(
                    {'pass': False,
                        'error': 'Wrong Device OS for this device'})
                self.log.e(TAG, str(opJson))

################# Handles Commands sent to Roles #################
    def command_to_role(self, json_data):
        TAG = 'command_to_role'
        print 'In command_to_role'
        role_table_id = 'role_table_id'
        try:
            role_table_id = str(json_data['id'])
        except:
            self.log.e(
                TAG,
                'There is something wrong in the POST parametes sent')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False,
                                 'error': 'RoleID not found in request'})
            self.log.e(TAG, str(opJson))
            return

        # Finding the role_table_id from RoleTable using RoleName
        # role = RoleDBHelper()
        device = DeviceDBHelper()
        merger = Merger()

        print 'role_table_id = ' + role_table_id
        device_list = device.get_devices_of_role(role_table_id)

        print device_list

        if device_list is None:
            self.log.e(TAG, 'Device List is Empty')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False, 'error': 'Device list empty'})
            self.log.e(TAG, str(opJson))
            return

        for device_item in device_list:
            device_os = str(device_item[c.DEVICE_TABLE_OS])
            device_id = str(device_item[c.DEVICE_TABLE_ID])
            device_udid = str(device_item[c.DEVICE_TABLE_UDID])

            if 'action' in json_data:
                policy_dict = {'action_command': json_data.get('action'),
                               'passcode': json_data.get('passcode')}
            elif 'broadcast' in json_data:
                policy_dict = {'broadcast_command': json_data.get('broadcast')}
            else:
                policy_dict = merger.merge(device_id)

            print device_os

            # Now Send the parametes to the Corresponding the engine
            # Send the command to iOS Engine
            if device_os == 'ios':
                print 'sending command Role ios'
                command_instance = ios_command.IosCommand()
                command_instance.execute(policy_dict, device_id, device_udid)
                #create_ios_task.delay(policy_dict, device_id, device_udid)
                opJson = json.dumps({'pass': True, 'message': 'Message sent\
                                     from server'})
                self.log.e(TAG, str(opJson))

            # Send the command to Samsung Engine
            elif device_os == 'samsung':
                command_instance = android_command.AndroidCommand()
                command_instance.execute(policy_dict, device_id)
                #create_android_task.delay(json_data, device_id)
                opJson = json.dumps({'pass': True, 'message': 'Message sent\
                                     from server'})
                self.log.e(TAG, str(opJson))

            # Wrong device_os
            else:
                self.log.e(TAG, 'Wrong Device OS in the Device Table')
                # Create the O/P JSON
                opJson = json.dumps(
                    {'pass': False,
                        'error': 'Wrong Device OS for this device'})
                self.log.e(TAG, str(opJson))

################# Handles Commands sent to Company #################
    def command_to_company(self, json_data):
        TAG = 'command_to_company'
        print 'In command_to_company'
        company_table_id = 'company_table_id'
        try:
            company_table_id = str(json_data['id'])
        except:
            self.log.e(
                TAG,
                'There is something wrong in the POST parametes sent')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False,
                                 'error': 'Company ID not found in request'})
            self.log.e(TAG, str(opJson))
            return

        # Finding the role_table_id from RoleTable using RoleName
        device = DeviceDBHelper()
        merger = Merger()

        device_list = device.get_devices(company_id=company_table_id)

        print device_list

        if device_list is None:
            self.log.e(TAG, 'Device List is Empty')
            # Create the O/P JSON
            opJson = json.dumps({'pass': False, 'error': 'Device list empty'})
            self.log.e(TAG, str(opJson))
            return

        for device_item in device_list:
            device_os = str(device_item[c.DEVICE_TABLE_OS])
            device_id = str(device_item[c.DEVICE_TABLE_ID])
            device_udid = str(device_item[c.DEVICE_TABLE_UDID])

            if 'action' in json_data:
                policy_dict = {'action_command': json_data.get('action'),
                               'passcode': json_data.get('passcode')}
            elif 'broadcast' in json_data:
                policy_dict = {'broadcast_command': json_data.get('broadcast')}
            else:
                policy_dict = merger.merge(device_id)

            print device_os

            # Now Send the parametes to the Corresponding the engine
            # Send the command to iOS Engine
            if device_os == 'ios':
                print 'sending command Role ios'
                command_instance = ios_command.IosCommand()
                command_instance.execute(policy_dict, device_id, device_udid)
                #create_ios_task.delay(policy_dict, device_id, device_udid)
                opJson = json.dumps({'pass': True, 'message': 'Message sent\
                                     from server'})
                self.log.e(TAG, str(opJson))

            # Send the command to Samsung Engine
            elif device_os == 'samsung':
                command_instance = android_command.AndroidCommand()
                command_instance.execute(policy_dict, device_id)
                #create_android_task.delay(json_data, device_id)
                opJson = json.dumps({'pass': True, 'message': 'Message sent\
                                     from server'})
                self.log.e(TAG, str(opJson))

            # Wrong device_os
            else:
                self.log.e(TAG, 'Wrong Device OS in the Device Table')
                # Create the O/P JSON
                opJson = json.dumps(
                    {'pass': False,
                        'error': 'Wrong Device OS for this device'})
                self.log.e(TAG, str(opJson))


if __name__ == '__main__':
    data = {
        'to': 'team',
        'id': '1',
        'company_id': 1,
        'action': 'device_details'}
    CommandPerformer(json_data=data).perform()
