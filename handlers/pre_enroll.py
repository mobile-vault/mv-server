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
from handlers.super import SuperHandler


class PreEnrollRequestHandler(SuperHandler):

    @tornado.web.authenticated
    @asynchronous
    def get(self):

        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        PreEnrollGetHandlerThread(
            self,
            callback=self.finish,
            company_id=self.get_current_company()).start()


class PreEnrollGetHandlerThread(threading.Thread):
    final_dict = {}

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(PreEnrollGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table

        company_id = self.company_id

        log = Logger('PreEnrollGetHandlerThread')
        TAG = 'run'

        role = RoleDBHelper()
        role_list = role.get_roles(company_id)
        if role_list is None:
            log.i(TAG, 'No user in User Table')
        else:
            role_array = []
            for roles in role_list:
                role_name = roles[c.ROLE_TABLE_NAME]
                role_id = roles[c.ROLE_TABLE_ID]

                role_dict = {}
                role_dict['role'] = str(role_name)
                role_dict['role_id'] = str(role_id)

                role_array.append(role_dict)

            self.final_dict['roles'] = role_array

        team = TeamDBHelper()
        team_list = team.get_teams(company_id)
        if team_list is None:
            log.i(TAG, 'No team in Team Table')
        else:
            team_array = []
            for teams in team_list:
                team_name = teams[c.TEAM_TABLE_NAME]
                team_id = teams[c.TEAM_TABLE_ID]

                team_dict = {}
                team_dict['team'] = str(team_name)
                team_dict['team_id'] = str(team_id)

                team_array.append(team_dict)

            self.final_dict['teams'] = team_array

        opJson = json.dumps({'data': self.final_dict, 'pass': True})
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
