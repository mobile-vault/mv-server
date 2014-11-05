from __future__ import division
from db.helpers.device import DeviceDBHelper
from db.helpers.dashboard import DashboardDBHelper
#from db.constants import Constants as c
from handlers.super import SuperHandler
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import threading
import json
from logger import Logger
#import ipdb


class DashboardDeviceCountRequestHandler(SuperHandler):

    @tornado.web.authenticated
    @asynchronous
    def get(self):
        DashboardDeviceCountGetHandlerThread(
            self,
            callback=self.finish,
            company_id=self.get_current_company()).start()


class DashboardDeviceCountGetHandlerThread(threading.Thread):
    log = 'log'

    def __init__(self, request=None, callback=None,
                 company_id=None, *args, **kwargs):
        super(
            DashboardDeviceCountGetHandlerThread,
            self).__init__(
            *args,
            **kwargs)
        self.request = request
        self.callback = callback
        self.company_id = company_id

    def run(self):
        # Return All the users in the User table
        self.log = Logger('DashboardDeviceCountGetHandlerThread')
#        TAG = 'run'

        company_id = self.company_id

        return_dict = {}
        drilldown_dict = {}
        data_dict = {}
        data_array = []
        ios_data_list = []
        samsung_data_list = []

        total = 0
#        category_list = []
        device = DeviceDBHelper()
        total = device.get_devices_count(company_id)
        print total

        dashboard = DashboardDBHelper()
        device_count_dict = dashboard.get_devices(company_id=company_id)
        ios_count = device_count_dict['ios']
        samsung_count = device_count_dict['samsung']

        ios_category_list = device.get_os_distinct_version(
            company_id=company_id, os_name='ios')

        samsung_category_list = device.get_os_distinct_version(
            company_id=company_id, os_name='samsung')

        if ios_category_list:
            for version in ios_category_list:
                count = device.get_devices_count(version=str(version),
                                                 company_id=company_id)
                if count is None:
                    score = 0
                else:
                    score = (count / total) * 100

                ios_data_list.append(score)

        if samsung_category_list:
            for version in samsung_category_list:
                count = device.get_devices_count(version=str(version),
                                                 company_id=company_id)
                if count is None:
                    score = 0
                else:
                    score = (count / total) * 100
                samsung_data_list.append(score)

        drilldown_dict['name'] = 'iOS'
        drilldown_dict['categories'] = ios_category_list
        drilldown_dict['data'] = ios_data_list

        data_dict['drilldown'] = drilldown_dict
        if ios_count:
            data_dict['y'] = (ios_count / total) * 100
        else:
            data_dict['y'] = 0
        data_array.append(data_dict)

        drilldown_dict1 = {}
        drilldown_dict1['name'] = 'Android'
        drilldown_dict1['categories'] = samsung_category_list
        drilldown_dict1['data'] = samsung_data_list

        data_dict1 = {}
        data_dict1['drilldown'] = drilldown_dict1
        if samsung_count:
            data_dict1['y'] = (samsung_count / total) * 100
        else:
            data_dict1['y'] = 0
        data_array.append(data_dict1)
        print data_array

        return_dict['data'] = data_array
        return_dict['pass'] = True
        return_dict['message'] = 'things seems to be working ...'
#        ipdb.set_trace()
        opJson = json.dumps(return_dict)
        #self.request.add_header('Access-Control-Allow-Origin', '*')
        self.request.set_header('Content-Type', 'application/json')
        self.request.write(opJson)
        tornado.ioloop.IOLoop.instance().add_callback(self.callback)
