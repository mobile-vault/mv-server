'''
This class won't have any POST method because user will be added through
enroll API.
'''

import cgi
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
from db.helpers.enrollment import EnrollmentDBHelper
from handlers.super import SuperHandler


class UserRequestHandler(SuperHandler):

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                                 'GET,POST, PUT,OPTIONS, DELETE')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self, data):

        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header ('Content-Type', 'application/json')
        if data is None or len(data) == 0:
            UsersGetHandlerThreadWithPage(request=self,
                    callback=self.finish,
                    company_id=self.get_current_company()).start()
        else:
            UserGetHandlerThread(request=self, data=data,
                        company_id=self.get_current_company(),
                        callback=self.finish).start()

    @tornado.web.authenticated
    @asynchronous
    def delete(self, data):

        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header ('Content-Type', 'application/json')
        UserDeleteHandlerThread(request=self, data=data,
                        company_id=self.get_current_company(),
                             callback=self.finish).start()

    @tornado.web.authenticated
    @asynchronous
    def put(self, data):

        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header ('Content-Type', 'application/json')
        UserPutHandlerThread(request=self, data=data,
                        company_id=self.get_current_company(),
                                     callback=self.finish).start()



class UsersGetHandlerThreadWithPage(threading.Thread):
    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = 'user_device'
    user_role = 'user_role'
    user_team = 'user_team'
    user_device_os = 'user_device_os'
    user_violation = 0
    '''

    def __init__(self, request = None, callback=None,
                company_id=None, *args, **kwargs):
        super(UsersGetHandlerThreadWithPage, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        #Return All the users in the User table
        log = Logger('UsersGetHandlerThreadWithPage')
        tag = 'run'

        company_id = self.company_id

        final_dict = {}

        user = UserDBHelper()
        team = TeamDBHelper()
        role = RoleDBHelper()
        violation = ViolationsDBHelper()
        device = DeviceDBHelper()

        offset = self.request.get_argument('offset', None)
        count = self.request.get_argument('count', None)
        name_query = self.request.get_argument('name', None)
        team_query = self.request.get_argument('team', None)
        role_query = self.request.get_argument('role', None)
        device_query = self.request.get_argument('device_id', None)
        sort_by = self.request.get_argument('sort_by', True)#Intentionally done
        sort_order = self.request.get_argument('sort', None)
        filter_key = self.request.get_argument('filter_key', None)
        filter_value = self.request.get_argument('filter_value', None)

        if filter_key == 'role':
            role_name = filter_value
            role_id = role.get_role_by_name(str(role_name), company_id)
        else:
            role_name = None
            role_id = None

        if filter_key == 'team':
            team_name = filter_value
            team_id = team.get_team_by_name(str(team_name), company_id)
        else:
            team_name = None
            team_id = None

        if filter_key == 'os':
            os_mapper = {'Android': 'samsung', 'iOS': 'ios'}
            os_type = os_mapper.get(str(filter_value))
        else:
            os_type = None

        if name_query:
            query  = name_query
            query_type = 'name'
        elif role_query:
            query = role_query
            query_type = 'role'
        elif device_query:
            query = device_query
            query_type = 'device'
        elif team_query:
            query = team_query
            query_type = 'team'
        else:
            query = None
            query_type = None

        if offset:
            result_list, total_count = user.get_users_for_user(
                        company_id=company_id, offset=offset, count=count,
                        role_id=role_id, team_id=team_id, query=query,
                        query_type=query_type, os_type=os_type,
                        sort_by=sort_by, sort_order=sort_order,
                        filter_key=filter_key, filter_value=filter_value)

        else:
            result_list, total_count = user.get_users(
                                    {c.USER_TABLE_COMPANY: company_id})

        if result_list:
            for user_dict in result_list:
                device_deleted = False
                device_info = device.get_device_with_udid(user_dict.get(
                                    'user_device'))
                if not device_info:
                    device_info = device.get_device_with_udid(user_dict.get(
                                    'user_device'), status=True)
                    device_deleted = True
                if device_info:
                    device_id = device_info[0].get(c.DEVICE_TABLE_ID)
                else:
                    device_id = None

                if device_deleted:
                    user_dict['user_device'] = None
                    user_dict['user_device_os'] = None

                if device_id:
                    print "printing \n device id", device_id
                    violation_count = violation.get_violation_count(
                          company_id=company_id, device_id=str(device_id))
                else:
                    violation_count = 0
                user_dict['user_violation'] = violation_count

            final_dict['data'] = result_list
            final_dict['count'] = total_count
            final_dict['pass'] = True
            final_dict['message'] = 'Seems like things are working ...'

        else:
            final_dict['pass'] = True
            log.e(tag,'No User in User Table')
            final_dict['message'] = 'Seems like things are not working ...'
            final_dict['count'] = 0

        ## add all the data into dictionary and create output json
        opJson = json.dumps(final_dict)
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)



class UserGetHandlerThread(threading.Thread):
    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = 'user_device'
    user_role = 'user_role'
    user_team = 'user_team'
    user_violations = 0
    '''
    final_dict = {}
    def __init__(self, request=None, data=None, callback=None,
                                company_id=None, *args, **kwargs):
        super(UserGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data.replace('/', '')
        self.callback = callback
        self.company_id = company_id

    def run(self):
        #Return All the users in the User table
        log = Logger('UserGetHandlerThread')
        tag = 'get'
        print self.data

        company_id = self.company_id

        final_dict = {}

        user = UserDBHelper()
        team = TeamDBHelper()
        role = RoleDBHelper()
        violation = ViolationsDBHelper()
        device = DeviceDBHelper()


        offset = self.request.get_argument('offset', '0')
        count = self.request.get_argument('count', None)
        name_query = self.request.get_argument('name', None)
        team_query = self.request.get_argument('team', None)
        role_query = self.request.get_argument('role', None)
        device_query = self.request.get_argument('device_id', None)
        sort_by = self.request.get_argument('sort_by', True)#Intentionally done
        sort_order = self.request.get_argument('sort', None)
        filter_key = str(self.request.get_argument('filter_key', None))
        filter_value = self.request.get_argument('filter_value', None)

        if filter_key == 'role':
            role_name = filter_value
            role_id = role.get_role_by_name(str(role_name), company_id)
        else:
            role_name = None
            role_id = None

        if filter_key == 'team':
            team_name = filter_value
            team_id = team.get_team_by_name(str(team_name), company_id)
        else:
            team_name = None
            team_id = None

        if filter_key == 'os':
            os_mapper = {'Android': 'samsung', 'iOS': 'ios'}
            os_type = os_mapper.get(str(filter_value))
        else:
            os_type = None

        if name_query:
            query  = name_query
            query_type = 'name'
        elif role_query:
            query = role_query
            query_type = 'role'
        elif device_query:
            query = device_query
            query_type = 'device'
        elif team_query:
            query = team_query
            query_type = 'team'
        else:
            query = None
            query_type = None

        if offset:
            if self.data in ('enrolled', 'pending'):
                result_list, total_count = user.get_users_for_user_status(
                                company_id=company_id, offset=offset,
                                count=count, data=self.data, query=query,
                                query_type=query_type, role_id=role_id,
                                team_id=team_id, os_type=os_type,
                                sort_by=sort_by, sort_order=sort_order,
                                filter_key=filter_key,
                                filter_value=filter_value)
            else:
                result_list, total_count = user.get_users_for_user_violation(
                                company_id=company_id, offset=offset,
                                count=count, query=query,
                                query_type=query_type, role_id=role_id,
                                team_id=team_id, os_type=os_type,
                                sort_by=sort_by, sort_order=sort_order,
                                filter_key=filter_key,
                                filter_value=filter_value)

        if result_list:
            for user_dict in result_list:
                device_deleted = False
                device_info = device.get_device_with_udid(user_dict.get(
                                                    'user_device'))
                if not device_info:
                    device_info = device.get_device_with_udid(user_dict.get(
                                        'user_device'), status=True)
                    device_deleted = True

                if device_info:
                    device_id = device_info[0].get(c.DEVICE_TABLE_ID)
                else:
                    device_id = None

                if device_deleted:
                    user_dict['user_device'] = None
                    user_dict['user_device_os'] = None

                if device_id:
                    violation_count = violation.get_violation_count(
                              company_id=company_id, device_id=str(device_id))
                else:
                    violation_count = 0

                user_dict['user_violation'] = violation_count

            final_dict['data'] = result_list
            final_dict['count'] = total_count
            final_dict['pass'] = True
            final_dict['message'] = 'Seems like things are working ...'

        else:
            final_dict['pass'] = True
            log.e(tag,'No User in User Table')
            final_dict['message'] = 'Seems like things are not working ...'
            final_dict['count'] = 0

        opJson = json.dumps(final_dict)
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class UserDeleteHandlerThread(threading.Thread):
    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = 'user_device'
    user_role = 'user_role'
    user_team = 'user_team'
    user_violations = 0
    '''
    final_dict = {}
    def __init__(self, request=None, data=None,
                company_id=None, callback=None, *args, **kwargs):
        super(UserDeleteHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data.replace('/', '')
        self.callback =callback
        self.company_id = company_id

    def run(self):
        #Return All the users in the User table
        log = Logger('UserDeleteHandlerThread')
        tag = 'DELETE'

        if self.data is None:
            log.e(tag,'No user registered in table for this user_id')
            opJson = json.dumps({'pass': False,
                    'message': 'No user registered in table for this user_id'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        user = UserDBHelper()
        device = DeviceDBHelper()
        enrollment = EnrollmentDBHelper()
        print 'print data here \n ... \n ', self.data

        user_list = user.get_user(str(self.data), company_id=self.company_id)
        if user_list is None:
            log.e(tag,'No user registered in table for this user_id')
            opJson = json.dumps({'pass': False,
                 'message': 'No user registered in table for this user_id'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            user_deleted = user.delete_user(str(user_list.get('id')))
            if user_deleted == False:
                log.e(tag,'Not able to delete from user table')
                opJson = json.dumps({'pass': False,
                     'message': 'Not able to delete from user table'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:

                devices = device.get_devices_of_user(str(self.data))
                if devices is not None and len(devices) > 0:
                    for each_device in devices:
                        device_id = each_device.get('id')
                        device.delete_device(str(device_id))
                        enrollment_list = enrollment.get_enrollments({
                            'device_id': device_id})
                        for enroll in enrollment_list:
                            enrollment_id = enroll.get('id')
                            enrollment.update_enrollment(str(enrollment_id),
                                {'device_id': "null", 'is_enrolled': False})
                log.i(tag,'User delelted')
                opJson = json.dumps({'pass': True,
                         'message': 'User Successfully deleted'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class UserPutHandlerThread(threading.Thread):
    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_policy_id = 'user_policy_id'
    '''
    final_dict = {}
    def __init__(self, request=None, data=None, callback=None,
                company_id=None, *args, **kwargs):
        super(UserPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data.replace('/', '')
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('UserPutHandlerThread')
        TAG = 'PUT'

        input_dict = json.loads(self.request.request.body)
        print input_dict

        self.user_id = input_dict.get('user_id')
        if self.user_id is None:
            log.e(TAG, 'No user id sent aborting update')
            opJson = json.dumps({'pass': False, 'message': 'No user id sent'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:

            user = UserDBHelper()
            user_dict = {c.USER_TABLE_NAME: str(input_dict.get('user_name')),
                        c.USER_TABLE_TEAM: str(input_dict.get('user_team')),
                        c.USER_TABLE_ROLE: str(input_dict.get('user_role'))}
            result = user.update_user(str(self.user_id), user_dict)
            if result is False:
                log.e(TAG, 'Not able to update the Users details')
                opJson = json.dumps({'pass': False,
                    'message': 'Not able to update the Email at DB'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                log.i(TAG, 'Users details Update successfully')
                opJson = json.dumps({'pass': True,
                     'message': 'Email updated for user.'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
