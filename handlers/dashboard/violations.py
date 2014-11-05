import datetime
import json
from db.helpers.violations import ViolationsDBHelper
from handlers.super import SuperHandler
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import threading

from logger import Logger


class DashboardViolationRequestHandler(SuperHandler):

    @tornado.web.authenticated
    @asynchronous
    def get(self):
        DashboardViolationGetHandlerThread(
            self,
            callback=self.finish,
            company_id=self.get_current_company()).start()


class DashboardViolationGetHandlerThread(threading.Thread):
    log = 'log'

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(DashboardViolationGetHandlerThread,
              self).__init__(*args, **kwargs)

        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table
        self.log = Logger('DashboardViolationGetHandlerThread')
        TAG = 'run'

        company_id = self.company_id

        offset = self.request.get_argument('offset', None)
        count = self.request.get_argument('count', None)
        date_handler = lambda obj: obj.isoformat() if isinstance(
            obj,
            datetime.datetime) else None

        violation = ViolationsDBHelper()
        violation_list, total_count = violation.get_violations_with_pages(
            company_id=company_id, offset=offset, count=count)
        # print "\nprinting violations list here\n", violation_list
        if violation_list is None or len(violation_list) == 0:
            self.log.i(TAG, 'No violations found')
            pass_status = True
            violation_list = []
        else:
            pass_status = True

        opJson = json.dumps({'data': violation_list, 'count': total_count,
                             'message': 'Seems like things are working ...',
                             'pass': pass_status}, default=date_handler)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
