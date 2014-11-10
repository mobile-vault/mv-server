from db.helpers.session import SessionDBHelper
# from db.constants import Constants as c
from handlers.super import SuperHandler
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import threading
import json
import datetime
from logger import Logger
import httpagentparser


class DashboardSessionRequestHandler(SuperHandler):

    @tornado.web.authenticated
    @asynchronous
    def get(self):
        DashboardSessionGetHandlerThread(
            self,
            callback=self.finish,
            company_id=self.get_current_company()).start()


class DashboardSessionGetHandlerThread(threading.Thread):
    log = 'log'

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(DashboardSessionGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table
        self.log = Logger('DashboardSessionGetHandlerThread')
        TAG = 'run'

        date_handler = lambda obj: obj.isoformat() if isinstance(
            obj,
            datetime.datetime) else None
        offset = self.request.get_argument('offset', None)
        count = self.request.get_argument('count', None)

        session = SessionDBHelper()
        session_list = session.get_sessions_with_page(self.company_id,
                                                      offset, count)
        if session_list is None or len(session_list) == 0:
            self.log.i(TAG, 'No Session in Session table')
            session_list = []

        for each_session in session_list:
            temp_user_agent = httpagentparser.detect(each_session.get(
                'user_agent'))
            if 'browser' in temp_user_agent:
                temp_browser = temp_user_agent.get('browser').get('name')
            else:
                temp_browser = None
            if 'os' in temp_user_agent:
                temp_os = temp_user_agent.get('os').get('name')
            else:
                temp_os = None

            each_session[
                'user_agent'] = '{0}/{1}'.format(temp_os, temp_browser)
        return_dict = {}
        return_dict['count'] = session.get_sessions_count(self.company_id)
        return_dict['data'] = session_list
        return_dict['message'] = "Seems like things are working ..."
        return_dict['pass'] = True
        opJson = json.dumps(return_dict, default=date_handler)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
