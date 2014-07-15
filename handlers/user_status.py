import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from logger import Logger
from db.constants import Constants as c
from db.helpers.device import *
from db.helpers.enrollment import *
from db.helpers.role import *
from db.helpers.team import *
from db.helpers.user import *
from db.helpers.violations import *

## This class won't have any POST method because user will be added through enroll API

class UserSentStatusRequestHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self,data):
        if data is None or len(data) == 0:
            UsersSentStatusGetHandlerThread(self).start()
#         else:
#             UserSentStatusGetHandlerThread(self,data).start()


class UsersSentStatusGetHandlerThread(threading.Thread):
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = None
    user_role = 'user_role'
    user_team = 'user_team'
    user_device_os = None
    enrollment_id = 'enrollment_id'
    sent_on = 'sent_on'
    final_dict = {}
    def __init__(self, request = None, callback=None,*args, **kwargs):
        super(UsersSentStatusGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback =callback


    def run(self):
        #Return All the users in the User table
        log = Logger('UsersSentStatusGetHandlerThread')
        TAG = 'run'

        page = self.request.get_argument('page', None)
        count = self.request.get_argument('count', None)

        enrollment = EnrollmentDBHelper()
        enrollment_list = enrollment.get_not_enrolled(int(page), int(count))
        device_id = ''

        if enrollment_list is None:
            log.i(TAG, 'No enrollment in the table')
            opJson = json.dumps({'pass': True, 'users': []})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            inner_array = []
            for enrollments in enrollment_list:
                self.user_id = enrollments[c.ENROLLMENT_TABLE_USER]
                self.sent_on = enrollments[c.ENROLLMENT_TABLE_SENT_ON]
                self.enrollment_id = enrollments[c.ENROLLMENT_TABLE_ID]
                device_id = enrollments[c.ENROLLMENT_TABLE_DEVICE]

                print 'deice_id ' + str(device_id)

                user = UserDBHelper()
                user_dict = user.get_user(str(self.user_id))

                if user_dict is None:
                    log.i(TAG, 'No user corresponding to the enrollment id = ' + str(self.enrollment_id))
                    opJson = json.dumps({'pass': False, 'message': 'No user corresponding to the enrollment id = ' + str(self.enrollment_id)})
                    #self.request.add_header('Access-Control-Allow-Origin', '*')
                    self.request.set_header ('Content-Type', 'application/json')
                    self.request.write(opJson)
#                     tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    self.user_name = str(user_dict[c.USER_TABLE_NAME])
                    self.user_email = str(user_dict[c.USER_TABLE_EMAIL])
                    self.user_team_id = str(user_dict[c.USER_TABLE_TEAM])
                    self.user_role_id = str(user_dict[c.USER_TABLE_ROLE])


                    #Find out devices attached
                    device = DeviceDBHelper()

                    device_list = []
                    device_dict = device.get_device(str(device_id))
                    print device_dict
                    device_list.append(device_dict)
                    if device_list is None:
                        self.user_device = None
                    else:
                        for devices in device_list:
                            print 'devices = ' + str(devices)
                            self.user_device_os = str(devices[c.DEVICE_TABLE_OS])

                    ## Find out the User Role
                    role = RoleDBHelper()
                    role_list = role.get_role(self.user_role_id, [c.ROLE_TABLE_NAME])
                    if role_list is None:
                        self.user_role = None
                    else:
                        self.user_role = str(role_list[c.ROLE_TABLE_NAME])

                    ## Find out User Team
                    team = TeamDBHelper()
                    team_list = team.get_team(self.user_team_id, [c.TEAM_TABLE_NAME])
                    if team_list is None:
                        self.user_team = None
                    else:
                        self.user_team = str(team_list[c.TEAM_TABLE_NAME])

                    violation = ViolationsDBHelper()
                    violation_count = violation.get_violation_count(str(self.user_id))

                    inner_dict = {}
                    inner_dict = {
                                  'user_id': self.user_id,
                                  'user_name': self.user_name,
                                  'user_role': self.user_role,
                                  'user_team': self.user_team,
                                  'user_device': device_id,
                                  'user_violation': violation_count,
                                  'user_device_os' : self.user_device_os,
                                  'sent_on': str(self.sent_on)
                                  }
                    inner_array.append(inner_dict)

            self.final_dict['pass'] = True
            self.final_dict['users'] = inner_array

            opJson = json.dumps(self.final_dict)
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)







class UserEnrollStatusRequestHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self,data):
        if data is None or len(data) == 0:
            UsersEnrollStatusGetHandlerThread(self).start()
#         else:
#             UserEnrollStatusGetHandlerThread(self,data).start()



class UsersEnrollStatusGetHandlerThread(threading.Thread):
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = None
    user_role = 'user_role'
    user_team = 'user_team'
    user_device_os = None
    enrollment_id = 'enrollment_id'
    sent_on = 'sent_on'
    enrolled_on = 'enrolled_on'
    final_dict = {}
    def __init__(self, request = None,callback=None ,*args, **kwargs):
        super(UsersEnrollStatusGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback


    def run(self):
        #Return All the users in the User table
        log = Logger('UsersEnrollStatusGetHandlerThread')
        TAG = 'run'

        page = self.request.get_argument('page', None)
        count = self.request.get_argument('count', None)

        device_id = ''
        enrollment = EnrollmentDBHelper()
        enrollment_list = enrollment.get_enrolled(int(page), int(count))

        if enrollment_list is None:
            log.i(TAG, 'No enrollment in the table')
            opJson = json.dumps({'pass': True, 'users': []})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            inner_array = []
            for enrollments in enrollment_list:

                self.user_id = enrollments[c.ENROLLMENT_TABLE_USER]
                self.sent_on = enrollments[c.ENROLLMENT_TABLE_SENT_ON]
                self.enrollment_id = enrollments[c.ENROLLMENT_TABLE_ID]
                self.enrolled_on = enrollments[c.ENROLLMENT_TABLE_ENROLLED_ON]
                device_id = enrollments[c.ENROLLMENT_TABLE_DEVICE]



                user = UserDBHelper()
                user_dict = user.get_user(str(self.user_id))

                if user_dict is None:
                    log.i(TAG, 'No user corresponding to the enrollment id = ' + str(self.enrollment_id))
                    opJson = json.dumps({'pass': False, 'message': 'No user corresponding to the enrollment id = ' + str(self.enrollment_id)})
                    #self.request.add_header('Access-Control-Allow-Origin', '*')
                    self.request.set_header ('Content-Type', 'application/json')
                    self.request.write(opJson)
#                     tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    self.user_name = str(user_dict[c.USER_TABLE_NAME])
                    self.user_email = str(user_dict[c.USER_TABLE_EMAIL])
                    self.user_team_id = str(user_dict[c.USER_TABLE_TEAM])
                    self.user_role_id = str(user_dict[c.USER_TABLE_ROLE])

                    print 'device_id ' + str(device_id)
                    #Find out devices attached
                    device = DeviceDBHelper()
#                     device_dict = {
#                                    c.DEVICE_TABLE_USER: self.user_id
#                                   }
#                     device_list = device.get_devices_of_user(self.user_id)
                    device_list = []
                    device_dict = device.get_device(str(device_id))
                    device_list.append(device_dict)
                    print 'device list  = ' + str(device_list)
                    if device_list is None:
                        self.user_device = None
                    else:
                        for devices in device_list:
                            print 'devices = ' + str(devices)
                            self.user_device = str(devices[c.DEVICE_TABLE_UDID])
                            self.user_device_os = str(devices[c.DEVICE_TABLE_OS])

                    ## Find out the User Role
                    role = RoleDBHelper()
                    role_list = role.get_role(self.user_role_id, [c.ROLE_TABLE_NAME])
                    if role_list is None:
                        self.user_role = None
                    else:
                        self.user_role = str(role_list[c.ROLE_TABLE_NAME])

                    ## Find out User Team
                    team = TeamDBHelper()
                    team_list = team.get_team(self.user_team_id, [c.TEAM_TABLE_NAME])
                    if team_list is None:
                        self.user_team = None
                    else:
                        self.user_team = str(team_list[c.TEAM_TABLE_NAME])

                    violation = ViolationsDBHelper()
                    violation_count = violation.get_violation_count(str(self.user_id))

                    inner_dict = {}
                    inner_dict = {
                             'user_id': self.user_id,
                             'user_name': self.user_name,
                             'user_role': self.user_role,
                             'user_team': self.user_team,
                             'user_device': device_id,
                             'user_violation': violation_count,
                             'user_device_os' : self.user_device_os,
                             'sent_on': self.sent_on,
                             'enrolled_on': self.enrolled_on
                            }
                    inner_array.append(inner_dict)

            self.final_dict['pass'] = True
            self.final_dict['users'] = inner_array

            opJson = json.dumps(self.final_dict)
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)



class UserViolationStatusRequestHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self,data):
        if data is None or len(data) == 0:
            UsersViolationStatusGetHandlerThread(self,callback=self.finish).start()
#         else:
#             UserViolationStatusGetHandlerThread(self,data).start()
#

class UsersViolationStatusGetHandlerThread(threading.Thread):
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_device = None
    user_role = 'user_role'
    user_team = 'user_team'
    user_device_os = None
    enrollment_id = 'enrollment_id'
    sent_on = 'sent_on'
    time_stamp = 'time_stamp'
    final_dict = {}
    def __init__(self, request = None, callback=None,*args, **kwargs):
        super(UsersViolationStatusGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback

    def run(self):
        #Return All the users in the User table
        log = Logger('UsersViolationStatusGetHandlerThread')
        TAG = 'run'

        page = self.request.get_argument('page', None)
        count = self.request.get_argument('count', None)
#         sort_by = self.request.get_argument('sort_by', None)
        print page
        print count
#         print sort_by

        violation = ViolationsDBHelper()
#         violation_list = violation.get_violations()
        violation_list = violation.get_violations_with_pages(None, int(page), int(count), None)
        if violation_list is None:
            opJson = json.dumps({'pass': True, 'violations' : []})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            array = []
            for violations in violation_list:
                self.user_id = str(violations[c.VIOLATION_TABLE_USER])
                self.time_stamp = str(violations[c.VIOLATION_TABLE_TIMESTAMP])

                device = DeviceDBHelper()
                team = TeamDBHelper()
                role = RoleDBHelper()
#                 violation = ViolationsDBHelper()

                user = UserDBHelper()
                user_dict = user.get_user(self.user_id)

                if user_dict is None:
                    log.e(TAG,'No user id corresponding to the violation id')
                    opJson = json.dumps({'pass': False, 'message': 'No user id corresponding to the violation id'})
                    #self.request.add_header('Access-Control-Allow-Origin', '*')
                    self.request.set_header ('Content-Type', 'application/json')
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    ## Find out user details for each user

                    inner_dict = {}
                    self.user_name = str(user_dict[c.USER_TABLE_NAME])
                    self.user_email = str(user_dict[c.USER_TABLE_EMAIL])
                    self.user_team_id = str(user_dict[c.USER_TABLE_TEAM])
                    self.user_role_id = str(user_dict[c.USER_TABLE_ROLE])
                    self.user_device = 'user_device'
                    self.user_role = 'user_role'
                    self.user_team = 'user_team'

                    #Find out devices attached
                    device_dict = {
                                   c.DEVICE_TABLE_USER: self.user_id
                                   }
                    device_list = device.get_devices_of_user(self.user_id)
                    print 'device list  = ' + str(device_list)
                    if device_list is None:
                        self.user_device = None
                    else:
                        for devices in device_list:
                            print 'devices = ' + str(devices)
                            self.user_device = str(devices[c.DEVICE_TABLE_UDID])
                            self.user_device_os = str(devices[c.DEVICE_TABLE_OS])

                    ## Find out the User Role
                    role_list = role.get_role(self.user_role_id, [c.ROLE_TABLE_NAME])
                    if role_list is None:
                        self.user_role = None
                    else:
                        self.user_role = str(role_list[c.ROLE_TABLE_NAME])

                    ## Find out User Team
                    team_list = team.get_team(self.user_team_id, [c.TEAM_TABLE_NAME])
                    if team_list is None:
                        self.user_team = None
                    else:
                        self.user_team = str(team_list[c.TEAM_TABLE_NAME])


                    ## Create the Output Dictionary

                    inner_dict = {
                                  'user_id': self.user_id,
                                  'user_name': self.user_name,
                                  'user_role': self.user_role,
                                  'user_team': self.user_team,
                                  'user_device': self.user_device,
#                                   'user_violation': self.user_violation,
                                  'user_device_os' : self.user_device_os,
                                  'time_stamp': self.time_stamp
                                  }
                    array.append(inner_dict)

            ## add all the data into dictionary and create output json
            self.final_dict['pass'] = True
            self.final_dict['violations'] = array
            opJson = json.dumps(self.final_dict)
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
