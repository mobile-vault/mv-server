import datetime
from db.helpers.logs import LogsDBHelper
# from db.constants import Constants as c
from handlers.super import SuperHandler
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import threading
import json
from logger import Logger


class DashboardLogsRequestHandler(SuperHandler):

    @tornado.web.authenticated
    @asynchronous
    def get(self):
        DashboardLogsGetHandlerThread(
            self,
            callback=self.finish,
            company_id=self.get_current_company()).start()


class DashboardLogsGetHandlerThread(threading.Thread):
    log = 'log'

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(DashboardLogsGetHandlerThread, self).__init__(*args, **kwargs)

        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table
        self.log = Logger('DashboardLogsGetHandlerThread')
        TAG = 'run'
        company_id = self.company_id
        #page = self.request.get_argument('page', None)
        #count = self.request.get_argument('count', None)
        count = 20
        date_handler = lambda obj: obj.isoformat() if isinstance(
            obj,
            datetime.datetime) else None
        logs = LogsDBHelper()
        logs_list = logs.get_logs(company_id, count=int(count))
        if logs_list is None or len(logs_list) == 0:
            self.log.i(TAG, 'No Logs in Log table')
            logs_list = []

        return_dict = {}
        return_dict['logs'] = logs_list
        return_dict['pass'] = True
        return_dict['message'] = 'Successfull ...'
        opJson = json.dumps(return_dict, default=date_handler)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
