import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
from .plugins import (get_individual_plugin, put_individual_plugin,
                      setup_default_policy)
from logger import Logger
from db.constants import Constants as c
from db.helpers.role import RoleDBHelper
from db.helpers.team import TeamDBHelper
from db.helpers.user import UserDBHelper
from db.helpers.company import CompanyDBHelper
from handlers.super import SuperHandler
from tasks import create_command_handler_task


class UserPolicyRequestHandler(SuperHandler):

    '''
This class won't have any POST method because Policies will be created
initially by default or on request by get method.
    '''

    def callback(self):
        self.finish()

    def options(self, data):
        self.add_header(
            'Access-Control-Allow-Methods',
            'GET,POST, PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        UserPolicyGetHandlerThread(request=self, data=data,
                                   company_id=self.get_current_company(),
                                   callback=self.callback).start()

    @tornado.web.authenticated
    @asynchronous
    def put(self, data):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        UserPolicyPutHandlerThread(data=data, request=self,
                                   company_id=self.get_current_company(),
                                   callback=self.callback).start()


class UserPolicyGetHandlerThread(threading.Thread):

    '''
    This class have different method to handle get request from UI
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(UserPolicyGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('UserPolicyGetHandlerThread')
        TAG = 'run'
        if self.data and self.company_id:
            # do stuff here
            user = UserDBHelper()
            url_data = self.data.split('/')
            user_id = url_data[0]
            plugin_name = url_data[1]
            user_detail = user.get_user(str(user_id),
                                        company_id=self.company_id)

            if user_detail:
                user_policy_id = user_detail.get('policy_id')

                if plugin_name == 'actions':
                    action_command = True
                else:
                    action_command = False

                print '\nplugin name \n', plugin_name
                if user_policy_id and not action_command:
                    plugin_data = get_individual_plugin(user_policy_id,
                                                        plugin_name)
                elif not action_command:
                    user_policy_id, plugin_data = setup_default_policy()
                    if user_policy_id:
                        user.update_user_policy(str(user_id),
                                                str(user_policy_id))
                        plugin_data = plugin_data.get(plugin_name)
                        print 'printing plugin data here ... \n', plugin_data
                    else:
                        log.e(TAG, 'User Policy ID setup failed.')
                        opJson = json.dumps(
                            {'pass': False,
                                'message': 'User policy creation failed.'})

                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                else:
                    plugin_data = {}

                if isinstance(plugin_data, str):
                    plugin_data = json.loads(plugin_data)
                plugin_data['_id'] = user_policy_id
                plugin_data['object_type'] = 'User'
                plugin_data['name'] = user_detail.get(c.USER_TABLE_NAME)
                opJson = json.dumps({'count': 1, 'message': 'Successfull',
                                     'pass': True, 'data': plugin_data})

                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                log.e(TAG, 'No Valid User id is sent in request')
                opJson = json.dumps(
                    {'pass': False, 'count': 0,
                        'message': 'No User id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for user policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class UserPolicyPutHandlerThread(threading.Thread):

    '''
    This class have method to handle put request related with particular
    plugin.
    It'll simply update the related plugin in the plugin table and invoke
    command parser method to assign commands to command controller part.
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(UserPolicyPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('UserPolicyPutHandlerThread')
        TAG = 'run'
        # Flag to track status of policy
        status = False

        if self.data and self.company_id:
            # do stuff here
            user = UserDBHelper()
            url_data = self.data.split('/')
            request_data = json.loads(self.request.request.body)
            user_id = url_data[0]
            plugin_name = url_data[1]
            command_handler_json = {'to': 'user', 'id': str(user_id),
                                    'company_id': self.company_id}
            user_detail = user.get_user(str(user_id),
                                        company_id=self.company_id)

            if user_detail:

                user_policy_id = user_detail.get('policy_id')

                if plugin_name != 'actions':
                    status = put_individual_plugin(user_policy_id, plugin_name,
                                                   request_data)
                else:
                    status = True
                    command_handler_json['action'] = request_data.get('action')
                    command_handler_json[
                        'passcode'] = request_data.get('lock_key')
                if status:
                    print "\nprinting the json output will be send to command\
                          handler\n", command_handler_json
                    create_command_handler_task.delay(command_handler_json)
                    request_data['_id'] = user_policy_id
                    request_data['object_type'] = 'User'
                    request_data['name'] = user_detail[c.USER_TABLE_NAME]
                    opJson = json.dumps(
                        {'data': request_data, 'pass': True,
                            'count': 1, 'message': 'Everything fine'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)

                else:
                    opJson = json.dumps(
                        {'pass': False, 'count': 0,
                            'message': 'Update operation at policy table \
failed'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
            else:
                log.e(TAG, 'No valid user id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid user id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for user policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class TeamPolicyRequestHandler(SuperHandler):

    def callback(self):
        self.finish()

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self, data):
        self.set_header('Content-Type', 'application/json')
        #self.add_header('Access-Control-Allow-Origin', '*')
        TeamPolicyGetHandlerThread(data=data, request=self,
                                   company_id=self.get_current_company(),
                                   callback=self.callback).start()

    @tornado.web.authenticated
    @asynchronous
    def put(self, data):
        self.set_header('Content-Type', 'application/json')
        #self.add_header('Access-Control-Allow-Origin', '*')
        TeamPolicyPutHandlerThread(data=data, request=self,
                                   company_id=self.get_current_company(),
                                   callback=self.callback).start()


class TeamPolicyGetHandlerThread(threading.Thread):

    '''
    This class have different method to handle get request from UI
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(TeamPolicyGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('TeamPolicyGetHandlerThread')
        TAG = 'run'
        if self.data and self.company_id:
            # do stuff here
            url_data = self.data.split('/')
            team_id = url_data[0]
            plugin_name = url_data[1]
            team = TeamDBHelper()
            print type(str(team_id))
            team_detail = team.get_team(str(team_id),
                                        company_id=self.company_id)

            if team_detail:

                team_policy_id = team_detail.get('policy_id')

                if plugin_name == 'actions':
                    action_command = True
                else:
                    action_command = False

                if team_policy_id and not action_command:
                    plugin_data = get_individual_plugin(team_policy_id,
                                                        plugin_name)
                elif not action_command:
                    team_policy_id, plugin_data = setup_default_policy()
                    if team_policy_id:
                        team.set_team_policy(team_id, team_policy_id)
                        plugin_data = plugin_data.get(plugin_name)
                        print 'printing plugin data here ... \n', plugin_data
                    else:
                        log.e(TAG, 'Team Policy ID setup failed.')
                        opJson = json.dumps(
                            {'pass': False,
                                'message': 'Team policy creation failed.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                else:
                    plugin_data = {}

                if isinstance(plugin_data, str):
                    plugin_data = json.loads(plugin_data)
                plugin_data['_id'] = team_policy_id
                plugin_data['object_type'] = 'Team'
                plugin_data['name'] = team_detail.get(c.TEAM_TABLE_NAME)
                opJson = json.dumps({'count': 1, 'message': 'Successfull',
                                     'data': plugin_data, 'pass': True})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                log.e(TAG, 'No valid team id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid team id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for team policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class TeamPolicyPutHandlerThread(threading.Thread):

    '''
    This class have method to handle put request related with particular
    plugin.
    It'll simply update the related plugin in the plugin table and invoke
    command parser method to assign commands to command controller part.
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(TeamPolicyPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('TeamPolicyPutHandlerThread')
        TAG = 'run'
        # Flag to track status of policy
        status = False
        if self.data and self.company_id:
            # do stuff here
            team = TeamDBHelper()
            url_data = self.data.split('/')
            request_data = json.loads(self.request.request.body)
            team_id = url_data[0]
            plugin_name = url_data[1]
            team_detail = team.get_team(str(team_id),
                                        company_id=self.company_id)

            if team_detail:

                team_policy_id = team_detail.get('policy_id')
                command_handler_json = {'to': 'team', 'id': str(team_id),
                                        'company_id': self.company_id}

                if plugin_name != 'actions':
                    status = put_individual_plugin(team_policy_id, plugin_name,
                                                   request_data)
                else:
                    status = True
                    command_handler_json['action'] = request_data.get('action')
                    command_handler_json['passcode'] = request_data.get(
                        'lock_key')

                if status:
                    print "\nprinting the json output will be send to command\
                          handler\n", command_handler_json
                    create_command_handler_task.delay(command_handler_json)
                    request_data['_id'] = team_policy_id
                    request_data['object_type'] = 'Team'
                    request_data['name'] = team_detail.get(c.TEAM_TABLE_NAME)
                    opJson = json.dumps(
                        {'data': request_data, 'pass': True,
                            'message': 'Everything fine', 'count': 1})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
                else:
                    opJson = json.dumps(
                        {'pass': False, 'count': 0,
                            'message': 'Update operation at policy table \
failed'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)

            else:
                log.e(TAG, 'No valid team id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid team id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for team policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class RolePolicyRequestHandler(SuperHandler):

    def callback(self):
        self.finish()

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                        'GET,POST,PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self, data):
        self.set_header('Content-Type', 'application/json')
        #self.add_header('Access-Control-Allow-Origin', '*')
        RolePolicyGetHandlerThread(request=self, data=data,
                                   company_id=self.get_current_company(),
                                   callback=self.callback).start()

    @tornado.web.authenticated
    @asynchronous
    def put(self, data):
        self.set_header('Content-Type', 'application/json')
        #self.add_header('Access-Control-Allow-Origin', '*')
        RolePolicyPutHandlerThread(request=self, data=data,
                                   company_id=self.get_current_company(),
                                   callback=self.callback).start()


class RolePolicyGetHandlerThread(threading.Thread):

    '''
    This class have different method to handle get request from UI
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(RolePolicyGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('RolePolicyGetHandlerThread')
        TAG = 'run'
        if self.data and self.company_id:
            # do stuff here
            role = RoleDBHelper()
            url_data = self.data.split('/')
            role_id = url_data[0]
            plugin_name = url_data[1]
            role_detail = role.get_role(str(role_id),
                                        company_id=self.company_id)

            if role_detail:

                role_policy_id = role_detail.get('policy_id')

                if plugin_name == 'actions':
                    action_command = True
                else:
                    action_command = False

                if role_policy_id and not action_command:
                    plugin_data = get_individual_plugin(role_policy_id,
                                                        plugin_name)
                elif not action_command:
                    role_policy_id, plugin_data = setup_default_policy()
                    if role_policy_id:
                        role.set_role_policy(str(role_id), str(role_policy_id))
                        plugin_data = plugin_data.get(plugin_name)
                    else:
                        log.e(TAG, 'Role Policy ID setup failed.')
                        opJson = json.dumps(
                            {'pass': False, 'count': 0,
                                'message': 'Role policy creation failed.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                else:
                    plugin_data = {}

                if isinstance(plugin_data, str):
                    plugin_data = json.loads(plugin_data)
                plugin_data['_id'] = role_policy_id
                plugin_data['object_type'] = 'Role'
                plugin_data['name'] = role_detail.get(c.ROLE_TABLE_NAME)
                opJson = json.dumps({'count': 1, 'message': 'Successfull',
                                     'data': plugin_data, 'pass': True})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                log.e(TAG, 'No valid role id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid role id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for role policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class RolePolicyPutHandlerThread(threading.Thread):

    '''
    This class have method to handle put request related with
    particular plugin.
    It'll simply update the related plugin in the plugin table and invoke
    command parser method to assign commands to command controller part.
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(RolePolicyPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('RolePolicyPutHandlerThread')
        TAG = 'run'
        # Flag to track status of policy
        status = False
        if self.data:
            # do stuff here
            role = RoleDBHelper()
            url_data = self.data.split('/')
            print self.request.request.body
            request_data = json.loads(self.request.request.body)
            role_id = url_data[0]
            plugin_name = url_data[1]
            role_detail = role.get_role(str(role_id),
                                        company_id=self.company_id)

            if role_detail:

                role_policy_id = role_detail.get('policy_id')
                command_handler_json = {'to': 'role', 'id': str(role_id),
                                        'company_id': self.company_id}

                if plugin_name != 'actions':
                    status = put_individual_plugin(role_policy_id, plugin_name,
                                                   request_data)
                else:
                    status = True
                    command_handler_json['action'] = request_data.get('action')
                    command_handler_json[
                        'passcode'] = request_data.get('lock_key')
                if status:
                    print "\nprinting the json output will be send to command\
                          handler\n", command_handler_json
                    create_command_handler_task.delay(command_handler_json)
                    request_data['_id'] = role_policy_id
                    request_data['object_type'] = 'Role'
                    request_data['name'] = role_detail.get(c.ROLE_TABLE_NAME)
                    opJson = json.dumps(
                        {'data': request_data, 'pass': True,
                            'count': 1, 'message': 'Everything fine'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
                else:
                    opJson = json.dumps(
                        {'pass': False, 'count': 0,
                            'message': 'Update operation at policy table \
failed'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)

            else:
                log.e(TAG, 'No valid role id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid role id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for role policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class CompanyPolicyRequestHandler(SuperHandler):

    '''
    This class have all the methods related with /policy/company {get,put}
    verbs
    '''

    def callback(self):
        self.finish()

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                        'GET,POST,PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self, data):
        self.set_header('Content-Type', 'application/json')
        #self.add_header('Access-Control-Allow-Origin', '*')
        CompanyGetHandlerThread(request=self, data=data,
                                company_id=self.get_current_company(),
                                callback=self.callback).start()

    @tornado.web.authenticated
    @asynchronous
    def put(self, data):
        self.set_header('Content-Type', 'application/json')
        #self.add_header('Access-Control-Allow-Origin', '*')
        CompanyPutHandlerThread(request=self, data=data,
                                company_id=self.get_current_company(),
                                callback=self.callback).start()


class CompanyGetHandlerThread(threading.Thread):

    '''
    This class have different method to handle get request from UI
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(CompanyGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('CompanyPolicyGetHandlerThread')
        TAG = 'run'
        if self.data:
            # do stuff here
            url_data = self.data.split('/')
            company_id = self.company_id
            plugin_name = url_data[1]
            company = CompanyDBHelper()
            company_detail = company.get_company(str(company_id))

            if company_detail:

                company_policy_id = company_detail.get('policy_id')

                if plugin_name == 'actions':
                    action_command = True
                else:
                    action_command = False

                if company_policy_id and not action_command:
                    plugin_data = get_individual_plugin(company_policy_id,
                                                        plugin_name)
                elif not action_command:
                    company_policy_id, plugin_data = setup_default_policy()

                    if company_policy_id:
                        company.set_company_policy(company_id,
                                                   company_policy_id)
                        plugin_data = plugin_data.get(plugin_name)
                    else:
                        log.e(TAG, 'Company Policy ID setup failed.')
                        opJson = json.dumps(
                            {'pass': False, 'count': 0,
                                'message': 'Company policy creation failed.'})
                        self.request.write(opJson)
                        tornado.ioloop.IOLoop.instance().add_callback(
                            self.callback)
                else:
                    plugin_data = {}

                if isinstance(plugin_data, str):
                    plugin_data = json.loads(plugin_data)

                plugin_data['_id'] = company_policy_id
                plugin_data['object_type'] = 'Company'
                plugin_data['name'] = company_detail.get(c.COMPANY_TABLE_NAME)
                opJson = json.dumps({'count': 1, 'message': 'Successfull',
                                     'data': plugin_data, 'pass': True})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

            else:
                log.e(TAG, 'No valid company id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid company id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for company policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)


class CompanyPutHandlerThread(threading.Thread):

    '''
    This class have method to handle put request related with
    particular plugin.
    It'll simply update the related plugin in the plugin table and issue invoke
    command parser method to assign commands to command controller part.
    '''

    def __init__(self, callback, request=None, data=None,
                 company_id=None, *args, **kwargs):
        super(CompanyPutHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback
        self.company_id = company_id

    def run(self):
        log = Logger('CompanyPutHandlerThread')
        TAG = 'run'
        # flag to track policy query
        status = False

        if self.data:
            # do stuff here
            company = CompanyDBHelper()
            url_data = self.data.split('/')
            request_data = json.loads(self.request.request.body)
            company_id = self.company_id  # url_data[0]
            plugin_name = url_data[1]
            company_detail = company.get_company(str(company_id))

            if company_detail:

                company_policy_id = company_detail.get('policy_id')
                command_handler_json = {'to': 'company', 'id': str(company_id),
                                        'company_id': self.company_id}

                if plugin_name != 'actions':
                    status = put_individual_plugin(company_policy_id,
                                                   plugin_name, request_data)
                else:
                    status = True
                    command_handler_json['action'] = request_data.get('action')
                    command_handler_json['passcode'] = request_data.get(
                        'lock_key')

                if status:
                    create_command_handler_task.delay(command_handler_json)
                    request_data['_id'] = company_policy_id
                    request_data['object_type'] = 'Company'
                    request_data['name'] = company_detail.get(
                        c.COMPANY_TABLE_NAME)
                    opJson = json.dumps(
                        {'data': request_data, 'pass': True,
                            'count': 1, 'message': 'Everything fine'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)
                else:
                    opJson = json.dumps(
                        {'pass': False, 'count': 0,
                            'message': 'Update operation at policy table \
failed'})
                    self.request.write(opJson)
                    tornado.ioloop.IOLoop.instance().add_callback(
                        self.callback)

            else:
                log.e(TAG, 'No valid company id is sent in request')
                opJson = json.dumps(
                    {'pass': False,
                        'message': 'No valid company id is sent in request'})
                self.request.write(opJson)
                tornado.ioloop.IOLoop.instance().add_callback(self.callback)

        else:
            log.e(TAG, 'UnAuthorized Access for company policy ')
            self.request.set_status(401)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
