import datetime
import json

import psycopg2
from base import *
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.constants import Constants as C


class LogsDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('LogsDBHelper')

    def add_log(self,component_id, component, level,tag,message,raw=None , company = '1'):
        TAG = 'add_log'
        if component_id is not None and component is not None and level is not None and message is not None:
            try:
                self.cursor.execute("INSERT INTO " + C.LOGS_TABLE + "(" + C.LOGS_TABLE_COMPONENT_TYPE + "," + C.LOGS_TABLE_COMPONENT_ID  + "," + C.LOGS_TABLE_LEVEL +\
                                    ","+ C.LOGS_TABLE_TAG + "," + C.LOGS_TABLE_MESSAGE + "," + C.LOGS_TABLE_RAW + "," + C.LOGS_TABLE_COMPANY + "," + C.LOGS_TABLE_TIMESTAMP +\
                                     ") VALUES( %s,%s,%s,%s,%s,%s,%s,%s) RETURNING id", [component, component_id, level , tag, message, raw, company, datetime.datetime.now()])
            except Exception,err:
                self.log.e(TAG,'Exception : ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                self.log.e(TAG,'Not able to insert in Logs table')
                return None
        else:
            self.log.e(TAG,'Some of required fields are not sent')

    def get_logs(self, company, levels=None, count=None):
        TAG = 'get_logs'

        skip = 0
        limit = 0

        if count is None:
            limit = 20
        else:
            limit = int(count)


        if company is not None:
            if levels is None:
                try:
                    self.cursor.execute("SELECT * FROM " + C.LOGS_TABLE + \
                                    " WHERE " + C.LOGS_TABLE_COMPANY + " = " \
                                    + str(company) + " ORDER BY " + \
                                C.LOGS_TABLE_TIMESTAMP + " DESC LIMIT " +\
                                 str(limit))
                except Exception,err:
                    self.log.e(TAG,'Exception : ' + repr(err))
                    print 'got exception ', err
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        temp_dict = {}
                        temp_dict[C.LOGS_TABLE_ID] = row[0]
                        temp_dict[C.LOGS_TABLE_COMPONENT_TYPE] = row[1]
                        temp_dict[C.LOGS_TABLE_COMPONENT_ID] = row[2]
                        temp_dict[C.LOGS_TABLE_LEVEL] = row[3]
                        temp_dict[C.LOGS_TABLE_TAG] = row[4]
                        temp_dict[C.LOGS_TABLE_MESSAGE] = row[5]
                        temp_dict[C.LOGS_TABLE_RAW] = row[6]
                        temp_dict[C.LOGS_TABLE_COMPANY] = row[7]
                        temp_dict[C.LOGS_TABLE_TIMESTAMP] = row[8]

                        return_array.append(temp_dict)

                    return return_array
                else:
                    self.log.e(TAG,'Not able to select from Logs table')
                    return None

            elif type(levels) == list:
                level_string = ''
                for level in levels:
                    level_string += C.LOGS_TABLE_LEVEL + " = '" + str(level)\
                                        + "' OR "

                level_string = level_string[:-4]
                try:
                    self.cursor.execute("SELECT * FROM " + C.LOGS_TABLE + \
                                " WHERE " + str(level_string) + " AND " +\
                                C.LOGS_TABLE_COMPANY + " = " + str(company) +\
                                " ORDER BY " + C.LOGS_TABLE_TIMESTAMP + \
                                         " DESC LIMIT " + str(limit))
                except Exception,err:
                    self.log.e(TAG,'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        temp_dict = {}
                        temp_dict[C.LOGS_TABLE_COMPONENT_ID] = row[0]
                        temp_dict[C.LOGS_TABLE_COMPONENT_TYPE] = row[1]
                        temp_dict[C.LOGS_TABLE_COMPONENT_ID] = row[2]
                        temp_dict[C.LOGS_TABLE_LEVEL] = row[3]
                        temp_dict[C.LOGS_TABLE_TAG] = row[4]
                        temp_dict[C.LOGS_TABLE_MESSAGE] = row[5]
                        temp_dict[C.LOGS_TABLE_RAW] = row[6]
                        temp_dict[C.LOGS_TABLE_COMPANY] = row[7]
                        temp_dict[C.LOGS_TABLE_TIMESTAMP] = str(row[8])

                        return_array.append(temp_dict)

                    return return_array
                else:
                    self.log.e(TAG,'Not able to select from Logs table')
                    print ('Not able to select from Logs table')
                    return None
            else:
                self.log.e(TAG,'Type of level is not string')
                print ('Type of level is not string')
                return None
        else:
            self.log.e(TAG,'Company ID not sent in the parameters')
            print ('Company ID not sent in the parameters')
            return None


if __name__ == '__main__':
    helper = LogsDBHelper()
    print helper.add_log(5, 'user', 'info', None, 'Insertion',None, '1')
