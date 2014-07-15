import json
import threading

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
from logger import Logger
from handlers.super import SuperHandler

class OperatingSystemRequestHandler(SuperHandler):

    def options(self, data):
        self.add_header('Access-Control-Allow-Methods',
                                 'GET,POST, PUT,OPTIONS, DELETE')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    @tornado.web.authenticated
    @asynchronous
    def get(self):

        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header ('Content-Type', 'application/json')

        OperatingSystemGetHandlerThread(request=self,
                        company_id=self.get_current_company(),
                        callback=self.finish).start()


class OperatingSystemGetHandlerThread(threading.Thread):

    def __init__(self, request=None, callback=None,
                    company_id=None, *args, **kwargs):
        super(OperatingSystemGetHandlerThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        #Return All the users in the User table
        log = Logger('OperatingSystemGetHandlerThread')
        tag = 'run'

        # hardcoded Operating System lists to save unnecessary db query
        final_dict = {
            "message": "Hardcoded OS list from backend ...",
            "count": 2,
            "data": [
                "Android",
                "iOS"
            ],
            "pass": True
        }

        opJson = json.dumps(final_dict)
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
