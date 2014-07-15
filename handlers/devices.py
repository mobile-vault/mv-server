'''
No POST method here devices will be added by the enrollment process
No PUT method because can't update the device details
'''

import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from logger import Logger
from db.constants import Constants as c
from db.helpers.device import *
from db.helpers.role import *
from db.helpers.team import *
from db.helpers.user import *
from db.helpers.violations import *


class DevicesRequestHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self,data):
        if data is None or len(data) == 0:
            DevicesGetHandlerThread(self,callback=self.finish).start()
        else:
            DeviceGetHandlerThread(self,data,callback=self.finish).start()


    @asynchronous
    def delete(self,data):
        DeviceDeleteHandlerThread(self,data,callback=self.finish).start()


class DeviceDeleteHandlerThread(threading.Thread):
    def __init__(self, request = None, data = None,callback=None, *args, **kwargs):
        super(DeviceDeleteHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback


    def run(self):
        #Return All the users in the User table
        log = Logger('DeviceGetHandlerThread')
        TAG = 'run'

        if self.data is None:
            log.e(TAG, 'No Device ID in the request')
            opJson = json.dumps({'pass': False, 'message': 'No Device ID in the request'})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            device = DeviceDBHelper()
            is_deleted = device.delete_device(str(self.data))
            if is_deleted == False:
                log.e(TAG, 'Not able to deleted the device id = ' + str(self.data))
                opJson = json.dumps({'pass': False, 'message': 'Not able to deleted the device id = ' + str(self.data)})
                #self.request.add_header('Access-Control-Allow-Origin', '*')
                self.request.set_header ('Content-Type', 'application/json')
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                log.i(TAG, 'Device Deleted Successfully')
                opJson = json.dumps({'pass': True, 'message': 'Device Deleted Successfully'})
                #self.request.add_header('Access-Control-Allow-Origin', '*')
                self.request.set_header ('Content-Type', 'application/json')
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)





class DeviceGetHandlerThread(threading.Thread):
    final_dict = {}
    user_id = 'user_id'
    user_team = 'user_team'
    user_role = 'user_role'
    device_id = 'device_id'
    user_name = 'user_name'
    user_email = 'user_email'
    device_os = 'device_os'
    def __init__(self, request = None, data = None,callback=None, *args, **kwargs):
        super(DeviceGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback


    def run(self):
        #Return All the users in the User table
        log = Logger('DeviceGetHandlerThread')
        TAG = 'run'

        device = DeviceDBHelper()
        device_dict = device.get_device(str(self.data),[c.DEVICE_TABLE_OS, c.DEVICE_TABLE_USER])
        if device_dict is None:
            log.e(TAG, 'No device data corresponding to this device Id = ' + str(self.data))
            opJson = json.dumps({'pass': False, 'message': 'No device data corresponding to this device Id = ' + str(self.data)})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            self.device_os = device_dict[c.DEVICE_TABLE_OS]
            self.user_id = device_dict[c.DEVICE_TABLE_USER]

            if self.device_os is None or self.device_os is None:
                log.e(TAG, 'Either device os or User id is nOne for device id = ' + str(self.data))
                opJson = json.dumps({'pass': False, 'message': 'Either device os or User id is nOne for device id = ' + str(self.data)})
                #self.request.add_header('Access-Control-Allow-Origin', '*')
                self.request.set_header ('Content-Type', 'application/json')
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                user = UserDBHelper()
                user_dict = user.get_user(str(self.user_id), [c.USER_TABLE_EMAIL, c.USER_TABLE_NAME, c.USER_TABLE_ROLE, c.USER_TABLE_TEAM])

                if user_dict is None:
                    log.e(TAG, 'No user info for the user id = ' + self.user_id)
                    opJson = json.dumps({'pass': False, 'message': 'No user info for the user id = ' + self.user_id})
                    #self.request.add_header('Access-Control-Allow-Origin', '*')
                    self.request.set_header ('Content-Type', 'application/json')
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    self.user_email = user_dict[c.USER_TABLE_EMAIL]
                    self.user_name = user_dict[c.USER_TABLE_NAME]
                    user_role_id = user_dict[c.USER_TABLE_ROLE]
                    user_team_id = user_dict[c.USER_TABLE_TEAM]

                    if user_role_id is not None:
                        role = RoleDBHelper()
                        role_dict = role.get_role(str(user_role_id), [c.ROLE_TABLE_NAME])

                        if role_dict is None:
                            log.e(TAG, 'No role in role table corresponding to the role_id = ' + str(user_role_id))
                            opJson = json.dumps({'pass': False, 'message' : 'No role in role table corresponding to the role_id = ' + str(user_role_id)})
                            #self.request.add_header('Access-Control-Allow-Origin', '*')
                            self.request.set_header ('Content-Type', 'application/json')
                            self.request.write(opJson)
                            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                        else:
                            self.user_role = role_dict[c.ROLE_TABLE_NAME]

                    if user_team_id is not None:
                        team = TeamDBHelper()
                        team_dict = team.get_team(str(user_team_id), [c.TEAM_TABLE_NAME])

                        if team_dict is None:
                            log.e(TAG, 'No team in team table corresponding to the team_id = ' + str(user_team_id))
                            opJson = json.dumps({'pass': False, 'message' : 'No team in team table corresponding to the team_id = ' + str(user_team_id)})
                            #self.request.add_header('Access-Control-Allow-Origin', '*')
                            self.request.set_header ('Content-Type', 'application/json')
                            self.request.write(opJson)
                            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                        else:
                            self.user_team = role_dict[c.TEAM_TABLE_NAME]

                    inner_dict = {}
                    inner_array = []
                    inner_dict['user_name'] = self.user_name
                    inner_dict['email_id'] = self.user_email
                    inner_dict['user_team'] = self.user_team
                    inner_dict['user_role'] = self.user_role
                    inner_dict['device_os'] = self.device_os
                    inner_dict['device_id'] = self.data
                    inner_array.append(inner_dict)

                    self.final_dict['devices'] = inner_array
                    self.final_dict['pass'] = True
                    opJson = json.dumps(self.final_dict)
                    #self.request.add_header('Access-Control-Allow-Origin', '*')
                    self.request.set_header ('Content-Type', 'application/json')
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)




class DevicesGetHandlerThread(threading.Thread):
    final_dict = {}
    user_id = 'user_id'
    user_team = 'user_team'
    user_role = 'user_role'
    device_id = 'device_id'
    user_name = 'user_name'
    user_email = 'user_email'
    device_os = 'device_os'
    def __init__(self, request = None, callback=None, *args, **kwargs):
        super(DevicesGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback


    def run(self):
        #Return All the users in the User table
        log = Logger('DevicesGetHandlerThread')
        TAG = 'run'

        page = self.request.get_argument('page', None)
        count = self.request.get_argument('count', None)
        sort_by = self.request.get_argument('sort_by', None)
        print page
        print count
        print sort_by

        device = DeviceDBHelper()
        device_list = device.get_devices_with_pages(None, int(page), int(count), str(sort_by))
        if device_list is None:
            log.i(TAG,'No device in Device Table')
            opJson = json.dumps({'pass': True, 'message': 'No Device registered'})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header ('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        inner_array = []
        for devices in device_list:
            self.user_id = devices[c.DEVICE_TABLE_USER]
            self.device_id = devices[c.DEVICE_TABLE_ID]
            self.device_os = devices[c.DEVICE_TABLE_OS]

            if self.user_id is None or self.device_id is None:
                log.e(TAG,'No user id corresponding to the device id = ' + str(self.device_id))
                opJson = json.dumps({'pass': False, 'message': 'No user id corresponding to the device id = ' + str(self.device_id)})
                #self.request.add_header('Access-Control-Allow-Origin', '*')
                self.request.set_header ('Content-Type', 'application/json')
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                user = UserDBHelper()
                user_list = user.get_user(str(self.user_id), [c.USER_TABLE_ROLE, c.USER_TABLE_TEAM, c.USER_TABLE_NAME, c.USER_TABLE_EMAIL ])

                if user_list is None:
                    log.e(TAG, 'No user details corresponding to the user id = ' + str(self.user_id))
                    opJson = json.dumps({'pass': False, 'message' : 'No user details corresponding to the user id = ' + str(self.user_id)})
                    #self.request.add_header('Access-Control-Allow-Origin', '*')
                    self.request.set_header ('Content-Type', 'application/json')
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
#                     for users in user_list:
                        self.user_email = user_list[c.USER_TABLE_EMAIL]
                        self.user_name = user_list[c.USER_TABLE_NAME]
                        user_role_id = user_list[c.USER_TABLE_ROLE]
                        user_team_id = user_list[c.USER_TABLE_TEAM]

                        if user_role_id is not None:
                            role = RoleDBHelper()
                            role_dict = role.get_role(str(user_role_id), [c.ROLE_TABLE_NAME])

                            if role_dict is None:
                                log.e(TAG, 'No role in role table corresponding to the role_id = ' + str(user_role_id))
                                opJson = json.dumps({'pass': False, 'message' : 'No role in role table corresponding to the role_id = ' + str(user_role_id)})
                                #self.request.add_header('Access-Control-Allow-Origin', '*')
                                self.request.set_header ('Content-Type', 'application/json')
                                self.request.write(opJson)
                                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                            else:
                                self.user_role = role_dict[c.ROLE_TABLE_NAME]

                        if user_team_id is not None:
                            team = TeamDBHelper()
                            team_dict = team.get_team(str(user_team_id), [c.TEAM_TABLE_NAME])
                            print team_dict

                            if team_dict is None:
                                log.e(TAG, 'No team in team table corresponding to the team_id = ' + str(user_team_id))
                                opJson = json.dumps({'pass': False, 'message' : 'No team in team table corresponding to the team_id = ' + str(user_team_id)})
                                #self.request.add_header('Access-Control-Allow-Origin', '*')
                                self.request.set_header ('Content-Type', 'application/json')
                                self.request.write(opJson)
                                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                            else:
                                self.user_team = role_dict[c.TEAM_TABLE_NAME]
                                print user_team_id
                                print self.user_team

            inner_dict = {}
            inner_dict['user_name'] = self.user_name
            inner_dict['email_id'] = self.user_email
            inner_dict['user_team'] = self.user_team
            inner_dict['user_role'] = self.user_role
            inner_dict['device_os'] = self.device_os
            inner_dict['device_id'] = self.device_id
            inner_array.append(inner_dict)

        self.final_dict['devices'] = inner_array
        self.final_dict['pass'] = True
        opJson = json.dumps(self.final_dict)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header ('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
