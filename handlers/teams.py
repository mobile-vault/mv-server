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


## Async class to get the enroll request by using the POST method
class TeamsRequestHandler(SuperHandler):

    ##Get all the roles info

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
             'GET,POST, PUT,OPTIONS, DELETE')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self,data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        if data is None or len(data) == 0:
            TeamsGetHandlerThread(self,callback=self.finish,
                    company_id=self.get_current_company()).start()
        else:
            TeamGetHandlerThread(self,data,callback=self.finish,
                company_id=self.get_current_company()).start()

    ## Add a team in the table
    @tornado.web.authenticated
    @asynchronous
    def post(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        TeamsPostHandlerThread(request=self, callback=self.finish,
                    company_id=self.get_current_company()).start()

    ## Delete a team in the table
    @tornado.web.authenticated
    @asynchronous
    def delete(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        TeamsDeleteHandlerThread(self, data,
                company_id=self.get_current_company(),
                callback=self.finish).start()

    ## Update a team in the table
    @tornado.web.authenticated
    @asynchronous
    def put(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        TeamsPutHandlerThread(self, data,
                company_id=self.get_current_company(),
                callback=self.finish).start()


class TeamsGetHandlerThread(threading.Thread):


    def __init__(self, request = None,callback=None,
                company_id=None,  *args, **kwargs):
        super(TeamsGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id


    def run(self):
        #Return All the users in the User table
        log = Logger('TeamsGetHandlerThread')
        tag = 'run'
        print 'In TeamsGetHandlerThread'
        final_dict = {}

        role = RoleDBHelper()
        team = TeamDBHelper()
        user = UserDBHelper()


        team_name = self.request.get_argument('team', None)
        offset = self.request.get_argument('offset', None)
        count = self.request.get_argument('count', None)
        sort_by = self.request.get_argument('sort_by', True)#Intentionally done
        name_query = self.request.get_argument('name', None)
        role_query = self.request.get_argument('role', None)
        device_query = self.request.get_argument('device_id', None)
        sort_order = self.request.get_argument('sort', None)
        filter_key = str(self.request.get_argument('filter_key', None))
        filter_value = self.request.get_argument('filter_value', None)

        ## Find all the roles in the Roles Table

        if filter_key == 'role':
            role_name = filter_value
            role_id = role.get_role_by_name(str(role_name), self.company_id)
        else:
            role_name = None
            role_id = None

        if name_query:
            query  = name_query
            query_type = 'name'
        elif role_query:
            query = role_query
            query_type = 'role'
        elif device_query:
            query = device_query
            query_type = 'device'
        else:
            query = None
            query_type = None

        if team_name:
            team_id = team.get_team_by_name(str(team_name), self.company_id)
        else:
            team_id = None
            teams_list = team.get_teams(self.company_id, [c.TEAM_TABLE_NAME,
                                                        c.TEAM_TABLE_ID])

        if team_id:
            result_list, total_count = user.get_users_for_team(
                            team_name=team_name, team_id=team_id,
                            role_name=role_name, role_id=role_id,
                            offset=offset, count=count, sort_by=sort_by,
                            query=query, query_type=query_type,
                            sort_order=sort_order)

        elif teams_list:
            for _team in teams_list:
                _team['team_type'] = _team.get('name')
                _team['team_name'] = _team.get('name')
                _team['team_id'] = _team.get('id')
                del _team['name']
                del _team['id']
            result_list = teams_list
            total_count = len(result_list)

        else:
            result_list = None

        if result_list:
            print "\n total", total_count
            final_dict['data'] = result_list
            final_dict['count'] = total_count
            final_dict['pass'] = True
            final_dict['message'] = 'Success ...'
        else:
            final_dict['pass'] = True
            final_dict['data'] = []
            log.e(tag,'No Team in Team Table')
            final_dict['message'] = 'Failed ...'
            final_dict['count'] = 0

        opJson = json.dumps(final_dict)
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class TeamsPostHandlerThread(threading.Thread):
    team_id = 'team_id'
    user_team = 'user_team'
    def __init__(self, request = None, callback=None,
                company_id=None, *args, **kwargs):
        super(TeamsPostHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback =callback
        self.company_id = company_id


    def run(self):
        #Return All the users in the User table
        company = self.company_id

        log = Logger('TeamsPostHandlerThread')
        tag = 'run'
        request_body = json.loads(self.request.request.body)

        self.user_team = request_body.get('name')

        if self.user_team is None or self.user_team == '':
            log.e(tag, 'sent Role is either None or blank')
            opJson = json.dumps({'pass': False,
                 'message': 'sent team is either None or blank'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        team = TeamDBHelper()
        insert_dict = {
                      c.TEAM_TABLE_NAME: self.user_team,
                      c.TEAM_TABLE_COMPANY: company,
                      c.TEAM_TABLE_DELETED: False
                      }
        self.team_id = team.add_team(insert_dict)
        if self.team_id is None:
            log.e(tag,'Team not inserted in table')
            opJson = json.dumps({'pass': False,
                 'message': 'Team not inserted in table'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            log.e(tag,'Team inserted in table')
            opJson = json.dumps({'pass': True, 'team_id': self.team_id})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)



class TeamGetHandlerThread(threading.Thread):
    '''
    user_id = 'user_id'
    user_name = 'user_name'
    user_email = 'user_email'
    user_team_id = 'user_team_id'
    user_role_id = 'user_role_id'
    user_policy_id = 'user_policy_id'
    team_name = 'team_name'
    user_violations = 'user_violations'
    user_role = 'user_role'
    '''

    final_dict = {}

    def __init__(self, request = None, data = None,callback=None,
                    company_id=None, *args, **kwargs):
        super(TeamGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('TeamGetHandlerThread')
        TAG = 'GET'
        page = self.request.get_argument('page', None)
        count = self.request.get_argument('count', None)
        sort_by = self.request.get_argument('sort_by', None)

        if self.data is None:
            log.e(TAG, 'No Team ID in Request')
            opJson = json.dumps({'pass': False,
             'message':'No team found corresponding to the team id '+str(
                        self.data)})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            team = TeamDBHelper()
            teams = team.get_team(str(self.data), company_id=self.company_id)
            outer_dict = {}
            outer_array = []
            print teams
            if teams is None:
                log.e(TAG, 'No team found corresponding to the team id ' + str(self.data))
                opJson = json.dumps({'pass': False, 'message':'No team found corresponding to the team id ' + str(self.data)})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                self.team_name = teams.get(c.TEAM_TABLE_NAME)
                user = UserDBHelper()
                filter_dict = {
                               c.USER_TABLE_TEAM: str(teams.get('id'))
                               }
                user_list = user.get_users_with_pages(filter_dict, int(page), int(count), str(sort_by))


                inner_array = []
                if user_list is not None:
                    for users in user_list:
                        inner_dict = {}
                        self.user_id = str(users[c.USER_TABLE_ID])
                        self.user_name = str(users[c.USER_TABLE_NAME])
                        self.user_email = str(users[c.USER_TABLE_EMAIL])
                        self.user_role_id = str(users[c.USER_TABLE_ROLE])

                        ## Find out the role for user
                        role = RoleDBHelper()
                        roles = role.get_role(self.user_role_id, [c.ROLE_TABLE_NAME])
                        if roles is None:
                            self.user_role= None
                        else:
                            self.user_role = str(roles[c.ROLE_TABLE_NAME])

                        ## Find out the device for user
                        device = DeviceDBHelper()
                        device_list = device.get_devices_of_user(self.user_id)
                        if device_list is None:
                            self.user_device = None
                        else:
                            devices = device_list[0]
                            self.user_device = str(devices[c.DEVICE_TABLE_UDID])
                            self.user_device_os = str(devices[c.DEVICE_TABLE_OS])
                            # Find out user violations
                            violation = ViolationsDBHelper()
                            violation_count = violation.get_violation_count(
                                str(devices.get('id')))


                        inner_dict = {
                               'user_id': self.user_id,
                               'user_name': self.user_name,
                               'user_role': self.user_role,
                               'user_team': self.team_name,
                               'user_device': self.user_device,
                               'user_violations': violation_count,
                               'user_device_os': self.user_device_os,
                               'user_email': self.user_email
                                    }
                        inner_array.append(inner_dict)


            outer_dict['name'] = self.team_name
            outer_dict['users'] = inner_array
            outer_dict['team_id'] = self.data
            print '\nouter_dict'
            print outer_dict
            outer_array.append(outer_dict)

            self.final_dict['pass'] = True
            self.final_dict['teams'] = outer_array

            opJson = json.dumps(self.final_dict)
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class TeamsPutHandlerThread(threading.Thread):
    team_id = 'role_id'
    team_name = 'role_name'
    team_policy_id = 'role_policy_id'
    def __init__(self, request=None, data=None,
                    company_id=None, callback=None, *args, **kwargs):
        super(TeamsPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('TeamsPutHandlerThread')
        TAG = 'PUT'

        input_dict = json.loads(self.request.request.body)
        self.team_id = input_dict.get('team_id')
        if self.team_id is None:
            log.e(TAG, 'No team_id sent aborting update')
            opJson = json.dumps({'pass': False, 'message': 'No team_id sent'})
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            if input_dict.has_key('name'):
                print 'Name found'
                self.team_name = input_dict['name']
                if self.team_name is None:
                    log.e(TAG, 'No team_name sent aborting update')
                    opJson = json.dumps({'pass': False, 'message': 'No team_name sent'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    team = TeamDBHelper()
                    update_dict = {
                                   c.TEAM_TABLE_NAME: self.team_name
                                   }
                    result = team.update_team(str(self.team_id),
                            self.company_id, update_dict)
                    if result == False:
                        log.e(TAG, 'Not able to update the team_name at DB')
                        opJson = json.dumps({'pass': False, 'message': 'Not able to update the team_name at DB'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                    else:
                        log.i(TAG, 'team_name Updated successfully')
                        opJson = json.dumps({'pass': True, 'message': 'team_name updated for team.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            elif input_dict.has_key('policy_id'):
                print 'Policy found'
                self.team_policy_id = input_dict['policy_id']
                if self.team_policy_id is None:
                    log.e(TAG, 'No team_policy_id sent aborting update')
                    opJson = json.dumps({'pass': False, 'message': 'No team_policy_id sent'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                else:
                    team = TeamDBHelper()
                    update_dict = {
                                   c.TEAM_TABLE_POLICY: self.team_policy_id
                                   }
                    result = team.update_team(str(self.team_id),
                              self.company_id, update_dict)
                    if result == False:
                        log.e(TAG,
                                'Not able to update the team_policy_id at DB')
                        opJson = json.dumps({'pass': False,
                          'message': 'Not able to update the team_policy_id at DB'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
                    else:
                        log.i(TAG, 'team_policy_id Updated successfully')
                        opJson = json.dumps({'pass': True, 'message': 'team_policy_id updated.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(self.callback)



class TeamsDeleteHandlerThread(threading.Thread):
    team_id = 'role_id'
    team_name = 'role_name'
    team_policy_id = 'role_policy_id'
    def __init__(self, request=None, data=None,
             company_id=None, callback=None, *args, **kwargs):
        super(TeamsDeleteHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data.replace('/', '')
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('TeamsDeleteHandlerThread')
        TAG = 'DELETE'

        if self.data is None:
            log.e(TAG, 'No Team ID in Request')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            team = TeamDBHelper()
            is_deleted = team.delete_team(str(self.data), self.company_id)
            if is_deleted:
                log.i(TAG, 'Team Successfully deleted')
                opJson = json.dumps({'pass': True, 'message': 'Team Successfully deleted'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
            else:
                log.e(TAG, 'Team Not Deleted')
                opJson = json.dumps({'pass': False, 'message': 'Team Not Deleted'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)
