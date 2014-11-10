# import cgi
import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from logger import Logger
from db.constants import Constants as c
from db.helpers.device import *
from db.helpers.user import *
from db.helpers.violations import *


class ViolationRequestHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self, data):
        if data is None or len(data) == 0:
            ViolationsGetHandlerThread(self, callback=self.finish).start()


class ViolationsGetHandlerThread(threading.Thread):
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
    violation_id = 'violation_id'
    final_dict = {}

    def __init__(self, request=None, callback=None, *args, **kwargs):
        super(ViolationsGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback

    def run(self):
        # Return All the users in the User table
        log = Logger('ViolationsGetHandlerThread')
        TAG = 'run'

        violation = ViolationsDBHelper()
        violation_list = violation.get_violations()

        if violation_list is None:
            opJson = json.dumps(
                {'pass': True, 'message': 'No Violation in Table'})
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        for violations in violation_list:
            self.user_id = violations[c.VIOLATION_TABLE_USER]

            if self.user_id is None:
                log.e(TAG, 'No user id in Violation List')
                opJson = json.dumps(
                    {'pass': False, 'message': 'No user id in Violation List'})
                #self.request.add_header('Access-Control-Allow-Origin', '*')
                self.request.set_header('Content-Type', 'application/json')
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                user = UserDBHelper()
                user_list = user.get_user(
                    self.user_id, [
                        c.USER_TABLE_NAME, c.USER_TABLE_EMAIL, ])
