import json

# import psycopg2
from .base import DBHelper
from logger import Logger
from db.constants import Constants as C


class DeviceDetailsDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('DeviceDetailsDBHelper')

    def add_device_detail(self, detail):
        TAG = 'add_device_detail'

        if isinstance(detail, dict):
            if C.DEVICE_DETAILS_TABLE_EXTRAS not in detail:
                detail[C.DEVICE_DETAILS_TABLE_EXTRAS] = "{}"

            try:
                query = ("INSERT INTO " + C.DEVICE_DETAILS_TABLE + "(" +
                         C.DEVICE_DETAILS_TABLE_DEVICE + "," +
                         C.DEVICE_DETAILS_TABLE_EXTRAS + ") VALUES( " +
                         str(detail[C.DEVICE_DETAILS_TABLE_DEVICE]) + ", '" +
                         json.dumps(detail[C.DEVICE_DETAILS_TABLE_EXTRAS]) +
                         "') RETURNING " + C.DEVICE_DETAILS_TABLE_DEVICE)
                self.cursor.execute(query)

            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return None
            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]

        else:
            self.log.e(TAG, 'Dictionary is not sent')
            return None

    # pass the device id
    def get_device_details(self, id, pluck=None):
        TAG = 'get_device_details'

        if isinstance(id, str):
            if pluck is None:
                try:
                    print("SELECT * FROM " + C.DEVICE_DETAILS_TABLE +
                          " WHERE " + C.DEVICE_DETAILS_TABLE_DEVICE + " = "
                          + id)
                    self.cursor.execute("SELECT * FROM " +
                                        C.DEVICE_DETAILS_TABLE + " WHERE " +
                                        C.DEVICE_DETAILS_TABLE_DEVICE + " = "
                                        + id)
                except Exception as err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None
                print self.cursor.rowcount
                if self.cursor.rowcount > 0:
                    # print self.cursor.rowcount
                    row = self.cursor.fetchone()
                    # print row
                    return_dict = {}
                    return_dict[C.DEVICE_DETAILS_TABLE_DEVICE] = row[1]
                    return_dict[C.DEVICE_DETAILS_TABLE_EXTRAS] = row[2]
                    return return_dict
                else:
                    self.log.e(TAG, 'Not able to perform select operation on\
                               device details table')
                    return None
            elif isinstance(pluck, list):
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute("SELECT " + query_var + " FROM " +
                                        C.DEVICE_DETAILS_TABLE + " WHERE " +
                                        C.DEVICE_DETAILS_TABLE_DEVICE + " = "
                                        + id)
                except Exception as err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = {}
                    i = 0
                    for item in pluck:
                        return_dict[item] = row[i]
                        i = i + 1
                    return return_dict
            else:
                self.log.e(TAG, 'Type of pluck is not list')
                return None
        else:
            self.log.e(TAG, 'ID is not string')
            return None

    def update_device_details(self, device, extras):
        TAG = 'update_device_details'

        if device is not None and isinstance(extras, dict):
            original_device_details = self.get_device_details(device)
            previous_extras = original_device_details.get(
                C.DEVICE_DETAILS_TABLE_EXTRAS)

            if isinstance(previous_extras, str):
                previous_extras = json.loads(previous_extras)

            new_extras = dict(previous_extras.items() + extras.items())

            try:
                query = ("UPDATE " + C.DEVICE_DETAILS_TABLE +
                         " SET extras = '" + json.dumps(new_extras) +
                         "' WHERE " + C.DEVICE_DETAILS_TABLE_DEVICE + " = "
                         + str(device))
                self.cursor.execute(query)
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG, 'ID is not string or Second parameter is not\
                       dictionary')
            return False


if __name__ == "__main__":
    device_detail = DeviceDetailsDBHelper()
    details = {
        "gcm_reg": "1234567890",
        "new": "123"
    }
    log = Logger('DeviceDetails')
    device_detail.update_device_details('13', details)
    # print device_detail.update_device_details('100', details)
    log.e('__main__', 'This is a message')
