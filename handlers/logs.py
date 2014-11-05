import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from logger import Logger
# from db.constants import Constants as c
from db.helpers.logs import *


class LogsRequestHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self, data):
        LogsGetHandlerThreadWithPage(self, data, callback=self.finish).start()


class LogsGetHandlerThreadWithPage(threading.Thread):
    final_dict = {}
    log = 'log'

    def __init__(
            self,
            request=None,
            data=None,
            callback=None,
            *args,
            **kwargs):
        super(LogsGetHandlerThreadWithPage, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback

    def run(self):
        # Return All the users in the User table
        self.log = Logger('LogsGetHandlerThreadWithPage')
        TAG = 'run'
        print self.data
        page = self.request.get_argument('page', None)
        count = self.request.get_argument('count', None)

        logs = LogsDBHelper()
        logs_list = logs.get_logs(
            '1', [
                'error', 'warning', 'info'], count, page)

        if logs_list is None or len(logs_list) == 0:
            self.log.i(TAG, 'No more logs to show')

        self.final_dict['pass'] = True
        self.final_dict['logs'] = logs_list
        opJson = json.dumps(self.final_dict)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
