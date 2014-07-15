import threading
import json
import tornado
import tornado.web
from tornado.web import asynchronous
from handlers.super import SuperHandler
from logger import Logger
from tasks import create_command_handler_task

class BroadCastMessageHandler(SuperHandler):

    def options(self):
        self.add_header('Access-Control-Allow-Methods', 'GET,POST, PUT,OPTIONS')
        self.add_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        #self.add_header('Access-Control-Allow-Origin', '*')

    def onComplete(self):
        self.finish()

    @tornado.web.authenticated
    @asynchronous
    def post(self):
        #self.add_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')
        BroadCastMesageThread(self, callback=self.onComplete,
                     company_id=self.get_current_company()).start()


class BroadCastMesageThread(threading.Thread):
    log = 'log'
    def __init__(self, request=None, callback=None, company_id=None,
                                                    *args, **kwargs):
        super(BroadCastMesageThread, self).__init__(*args, **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):

        company_id = self.company_id
        json_data = {}

        self.log = Logger('BroadCastMesageThread')
        TAG = 'run'
#        print 'In BroadCastMesageThread\'s POST'
#        print self.request.request.body
        data = json.loads(self.request.request.body)
        broadcast_message = data.get('broadcast')

        if broadcast_message and len(broadcast_message.strip()) > 0:
            json_data['broadcast'] = broadcast_message
            json_data['to'] = 'company'
            json_data['id'] = company_id
            json_data['company_id'] = company_id

            create_command_handler_task.delay(json_data)

            opJson = json.dumps({'pass': True,
                        'message': 'Message will be delivered to devices immediately.'})
        else:
            opJson = json.dumps({'pass': False,
                        'message': 'Please send some human readable broadcast message'})

        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
