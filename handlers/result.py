import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous

from logger import Logger
from db.constants import Constants as C
from db.helpers.ioscommand import *


class CommandResultRequestHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self, data):
        CommandResultGetHandlerThread(self, data, callback=self.finish).start()


class CommandResultGetHandlerThread(threading.Thread):
    uuid = 'uuid'
    log = 'log'
    final_dict = {}

    def __init__(
            self,
            request=None,
            data=None,
            callback=None,
            *args,
            **kwargs):
        super(CommandResultGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.data = data
        self.callback = callback

    def run(self):
        # Return All the users in the User table
        self.log = Logger('CommandResultGetHandlerThread')
        TAG = 'run'

        self.uuid = self.request.get_argument('uuid', None)
        print self.data
        print self.uuid
        self.uuid = self.data

        if self.uuid is None:
            self.log.e(TAG, 'UUID sent is none')
            self.final_dict['pass'] = False
            self.final_dict['message'] = 'UUID sent is none'
            opJson = json.dumps(self.final_dict)
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
        else:
            command = IOSCommandDBHelper()
            result_list = command.get_result(str(self.uuid))
            command_attributes = command.get_command_attributes(str(self.uuid))
            print 'result_list = ' + str(result_list)

            self.final_dict['pass'] = True
            self.final_dict['uuid'] = self.data
            self.final_dict[
                C.COMMAND_TABLE_TO] = command_attributes[
                C.COMMAND_TABLE_TO]
            self.final_dict[
                C.COMMAND_TABLE_TO_ID] = command_attributes[
                C.COMMAND_TABLE_TO_ID]
            self.final_dict['count'] = command.get_command_count(
                str(self.uuid))
            self.final_dict['data'] = result_list
            opJson = json.dumps(self.final_dict)
            #self.request.add_header('Access-Control-Allow-Origin', '*')
            self.request.set_header('Content-Type', 'application/json')
            self.request.write(opJson)
            tornado.ioloop.IOLoop.instance().add_callback(self.callback)
