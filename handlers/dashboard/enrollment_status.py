from db.helpers.violations import ViolationsDBHelper
from db.helpers.enrollment import EnrollmentDBHelper
from db.helpers.user import UserDBHelper
# from db.constants import Constants as c
from handlers.super import SuperHandler

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import threading
import json
from logger import Logger


class DashboardEnrollmentStatusRequestHandler(SuperHandler):

    @tornado.web.authenticated
    @asynchronous
    def get(self):
        DashboardEnrollmentStatusGetHandlerThread(
            self,
            callback=self.finish,
            company_id=self.get_current_company()).start()


class DashboardEnrollmentStatusGetHandlerThread(threading.Thread):
    log = 'log'

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(
            DashboardEnrollmentStatusGetHandlerThread,
            self).__init__(
            *
            args,
            **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table
        self.log = Logger('DashboardEnrollmentStatusGetHandlerThread')
        # TAG = 'run'

        # ToDo : replace this with dynamic company id from cookies.
        company_id = self.company_id

        return_dict = {}
        user = UserDBHelper()
        violation = ViolationsDBHelper()
        enrollment = EnrollmentDBHelper()

        violation_count = violation.get_violation_count(company_id=company_id)
        not_enrolled_count = enrollment.get_enrollment_status_count(
            company_id=company_id, status=False)
        enrolled_count = enrollment.get_enrollment_status_count(
            company_id=company_id, status=True)

        print "\n printing enrolled count", not_enrolled_count
        user_count = user.get_users_count(company_id=company_id)

        user_info_dict = {}
        user_info_dict['Violations'] = violation_count
        user_info_dict['Not Enrolled'] = not_enrolled_count
        user_info_dict['Enrolled'] = enrolled_count
        user_info_dict['Total Users'] = user_count
        return_dict['UserInformation'] = user_info_dict

        opJson = json.dumps({'message': 'Everything seems to be working ...',
                             'data': return_dict, 'pass': True})
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
