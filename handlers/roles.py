'''
Async class to get the enroll request by using the POST method
'''

import json
import threading
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
from logger import Logger
from db.constants import Constants as c
from db.helpers.device import DeviceDBHelper
from db.helpers.role import RoleDBHelper
from db.helpers.team import TeamDBHelper
from db.helpers.user import UserDBHelper
from db.helpers.violations import ViolationsDBHelper
from handlers.super import SuperHandler


class RolesRequestHandler(SuperHandler):

    # Get all the roles info
    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                        'GET,POST,PUT,OPTIONS,DELETE')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        if data is None or len(data) == 0:
            RolesGetHandlerThread(
                request=self,
                callback=self.finish,
                company_id=self.get_current_company()).start()
        else:
            RoleGetHandlerThread(request=self, data=data,
                                 company_id=self.get_current_company(),
                                 callback=self.finish).start()

    # Insert a role in the table
    @tornado.web.authenticated
    @asynchronous
    def post(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        RolesPostHandlerThread(request=self, callback=self.finish,
                               company_id=self.get_current_company()).start()

    # Delete a role in the table
    @tornado.web.authenticated
    @asynchronous
    def delete(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        RolesDeleteHandlerThread(request=self, data=data,
                                 company_id=self.get_current_company(),
                                 callback=self.finish).start()

    # Update a role in the table
    @tornado.web.authenticated
    @asynchronous
    def put(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        RolesPutHandlerThread(request=self, data=data,
                              company_id=self.get_current_company(),
                              callback=self.finish).start()


class RolesGetHandlerThread(threading.Thread):

    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = 'user_device'
    user_device_os = 'user_device_os'
    user_role = 'user_role'
    user_team = 'user_team'
    user_violations = 0
    '''

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(RolesGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table
        log = Logger('RolesGetHandler')
        tag = 'run'

        final_dict = {}
        role = RoleDBHelper()
        team = TeamDBHelper()
        user = UserDBHelper()

        role_name = self.request.get_argument('role', None)
        offset = self.request.get_argument('offset', None)
        count = self.request.get_argument('count', None)
        name_query = self.request.get_argument('name', None)
        team_query = self.request.get_argument('team', None)
        device_query = self.request.get_argument('device_id', None)
        sort_by = self.request.get_argument(
            'sort_by',
            True)  # Intentionally done
        sort_order = self.request.get_argument('sort', None)
        filter_key = str(self.request.get_argument('filter_key', None))
        filter_value = self.request.get_argument('filter_value', None)

        print role_name
        print "\nUI sorting order \n", sort_order
        # Find all the roles in the Roles Table
#        outer_array = []

        if name_query:
            query = name_query
            query_type = 'name'
        elif team_query:
            query = team_query
            query_type = 'team'
        elif device_query:
            query = device_query
            query_type = 'device'
        else:
            query = None
            query_type = None

        if filter_key == 'team':
            team_name = filter_value
            team_id = team.get_team_by_name(str(team_name), self.company_id)
        else:
            team_name = None
            team_id = None

        print "printing team id here ..", team_id
        if role_name:
            role_id = role.get_role_by_name(str(role_name), self.company_id)
        else:
            roles_list = role.get_roles(self.company_id, [c.ROLE_TABLE_NAME,
                                                          c.ROLE_TABLE_ID])
            role_id = None

        if role_id:
            result_list, total_count = user.get_users_for_role(
                role_name=role_name, role_id=role_id,
                team_name=team_name, team_id=team_id, offset=offset,
                count=count, sort_by=sort_by, query=query,
                query_type=query_type, sort_order=sort_order)

        elif roles_list:
            for _role in roles_list:
                _role['role_type'] = _role.get('name')
                _role['role_name'] = _role.get('name')
                _role['role_id'] = _role.get('id')
                del _role['name']
                del _role['id']
            result_list = roles_list
            total_count = len(result_list)
        else:
            result_list = None

        if result_list:
            final_dict['data'] = result_list
            final_dict['count'] = total_count
            final_dict['pass'] = True
            final_dict['message'] = 'Seems like things are working ...'
        else:
            final_dict['data'] = []
            final_dict['pass'] = True
            log.e(tag, 'No Role in Role Table')
            final_dict['message'] = 'Seems like things are not working ...'
            final_dict['count'] = 0

        opJson = json.dumps(final_dict)
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class RolesPostHandlerThread(threading.Thread):

    '''
    user_role_id = 'user_role_id'
    user_role = 'user_role'
    '''

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(RolesPostHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table

        company_id = self.company_id

        log = Logger('RolesPostHandler')
        tag = 'run'
        request_body = json.loads(self.request.request.body)

        self.user_role = request_body.get('name')

        if self.user_role is None or self.user_role == '':
            log.e(tag, 'sent Role is either None or blank')
            opJson = json.dumps({'pass': False,
                                 'error': 'sent Role is either None or blank'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        role = RoleDBHelper()
        insert_dict = {
            c.ROLE_TABLE_NAME: self.user_role,
            c.ROLE_TABLE_COMPANY: company_id,
            c.ROLE_TABLE_DELETED: False
        }

        self.user_role_id = role.add_role(insert_dict)

        if self.user_role_id is None:
            log.e(tag, 'Role not inserted in table')
            opJson = json.dumps({'pass': False,
                                 'error': 'Role not inserted in table'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            opJson = json.dumps({'pass': True, 'role_id': self.user_role_id})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class RoleGetHandlerThread(threading.Thread):

    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_policy_id = 'user_policy_id'
    role_name = 'role_name'
    user_violations = 'user_violations'
    '''

    final_dict = {}

    def __init__(self, request=None, data=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(RoleGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('RoleGetHandlerThread')
        TAG = 'GET'

        page = self.request.get_argument('offset', None)
        count = self.request.get_argument('count', None)
        sort_by = self.request.get_argument('sort_by', None)
        print page
        print count
        print sort_by

        if self.data and self.company_id:
            role = RoleDBHelper()
            roles = role.get_role(str(self.data), company_id=self.company_id)
            outer_dict = {}
            outer_array = []
            if roles is None:
                log.e(TAG, 'No role found corresponding to the role id ' +
                      str(self.data))
                opJson = json.dumps({'pass': False, 'message': 'No role found \
                            corresponding to the role id ' + str(self.data)})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                self.role_name = roles[c.ROLE_TABLE_NAME]

                user = UserDBHelper()
                filter_dict = {
                    c.USER_TABLE_ROLE: str(roles.get('id'))
                }
                user_list = user.get_users_with_pages(
                    filter_dict,
                    int(page),
                    int(count),
                    str(sort_by))

                inner_array = []
                if user_list is not None:
                    for users in user_list:
                        inner_dict = {}
                        self.user_id = str(users[c.USER_TABLE_ID])
                        self.user_name = str(users[c.USER_TABLE_NAME])
                        self.user_email = str(users[c.USER_TABLE_EMAIL])
                        self.user_team_id = str(users[c.USER_TABLE_TEAM])

                        # Find out the team for user
                        team = TeamDBHelper()
                        teams = team.get_team(self.user_team_id,
                                              [c.TEAM_TABLE_NAME])
                        if teams is None:
                            self.user_team = None
                        else:
                            self.user_team = str(teams[c.TEAM_TABLE_NAME])

                        # Find out the device for user
                        device = DeviceDBHelper()
                        device_list = device.get_devices_of_user(self.user_id)
                        if device_list is None:
                            self.user_device = None
                        else:
                            devices = device_list[0]
                            self.user_device = str(
                                devices[c.DEVICE_TABLE_UDID])
                            self.user_device_os = str(
                                devices[c.DEVICE_TABLE_OS])

                            # Find out user violations
                            violation = ViolationsDBHelper()
                            violation_count = violation.get_violation_count(
                                str(devices.get('id')))
                        inner_dict = {
                            'user_id': self.user_id,
                            'user_name': self.user_name,
                            'user_role': self.role_name,
                            'user_team': self.user_team,
                            'user_device': self.user_device,
                            'user_violations': violation_count,
                            'user_device_os': self.user_device_os
                        }
                        inner_array.append(inner_dict)

                outer_dict['name'] = self.role_name
                outer_dict['users'] = inner_array
                outer_dict['roleID'] = self.data
                outer_array.append(outer_dict)

            self.final_dict['pass'] = True
            self.final_dict['roles'] = outer_array

            opJson = json.dumps(self.final_dict)
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for Roles')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class RolesPutHandlerThread(threading.Thread):

    '''
    role_id = 'role_id'
    role_name = 'role_name'
    role_policy_id = 'role_policy_id'
    '''
    final_dict = {}

    def __init__(self, request=None, data=None,
                 company_id=None, callback=None, *args, **kwargs):
        super(RolesPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('RolesPutHandlerThread')
        TAG = 'PUT'

        input_dict = json.loads(self.request.request.body)

        self.role_id = input_dict.get('role_id')
        if self.role_id is None:
            log.e(TAG, 'No role_id sent aborting update')
            opJson = json.dumps({'pass': False, 'message': 'No role_id sent'})
            self.request.set_status(401)
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            if 'name' in input_dict:
                print 'Name found'
                self.role_name = input_dict['name']
                if self.role_name is None:
                    log.e(TAG, 'No role_name sent aborting update')
                    opJson = json.dumps(
                        {'pass': False, 'message': 'No role_name sent'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
                else:
                    role = RoleDBHelper()
                    update_dict = {
                        c.ROLE_TABLE_NAME: self.role_name
                    }
                    result = role.update_role(str(self.role_id),
                                              self.company_id, update_dict)
                    if not result:
                        log.e(TAG, 'Not able to update the role_name at DB')
                        opJson = json.dumps(
                            {'pass': False,
                                'message': 'Not able to update the \
role_name at DB'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                    else:
                        log.i(TAG, 'role_name Updated successfully')
                        opJson = json.dumps(
                            {'pass': True,
                                'message': 'role_name updated for role.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)

            elif 'policy_id' in input_dict:
                print 'Policy found'
                self.role_policy_id = input_dict['policy_id']
                if self.role_policy_id is None:
                    log.e(TAG, 'No Policy ID sent aborting update')
                    opJson = json.dumps(
                        {'pass': False, 'message': 'No policy_id sent'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
                else:
                    role = RoleDBHelper()
                    update_dict = {
                        c.ROLE_TABLE_POLICY: self.role_policy_id
                    }
                    result = role.update_role(str(self.role_id),
                                              self.company_id, update_dict)
                    if not result:
                        log.e(TAG, 'Not able to update the policy_id at DB')
                        opJson = json.dumps(
                            {'pass': False,
                                'message': 'Not able to update the \
policy_id at DB'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                    else:
                        log.i(TAG, 'policy_id Updated successfully')
                        opJson = json.dumps(
                            {'pass': True,
                                'message': 'policy_id updated for role.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)


class RolesDeleteHandlerThread(threading.Thread):
    role_id = 'role_id'
    role_name = 'role_name'
    role_policy_id = 'role_policy_id'
    final_dict = {}

    def __init__(self, request=None, data=None,
                 company_id=None, callback=None, *args, **kwargs):
        super(RolesDeleteHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data.replace('/', '')
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('RolesDeleteHandlerThread')
        TAG = 'DELETE'

        if self.data is None:
            log.e(TAG, 'No Role ID in Request')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            role = RoleDBHelper()
            is_deleted = role.delete_role(str(self.data), self.company_id)
            if is_deleted:
                log.i(TAG, 'Role Successfully deleted')
                opJson = json.dumps({'pass': True,
                                     'message': 'Role Successfully deleted'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                log.e(TAG, 'Role Not Deleted')
                opJson = json.dumps({'pass': False,
                                     'message': 'Role Not Deleted'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
