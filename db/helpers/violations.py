import datetime
# import json

# import psycopg2
from .base import *
from logger import Logger
from psycopg2.extensions import adapt
from db.constants import Constants as C


class ViolationsDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('ViolationsDBHelper')

    def add_violation(self, device):
        TAG = 'add_violation'
        if isinstance(device, str):
            try:
                self.cursor.execute(
                    """INSERT INTO {0} ({1}, {2})
                                    VALUES (%s, %s) RETURNING id;""".format(
                    C.VIOLATION_TABLE,
                    C.VIOLATION_TABLE_DEVICE,
                    C.VIOLATION_TABLE_TIMESTAMP),
                    (str(device),
                     datetime.datetime.now(),
                     ))

            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                self.log.e(TAG, 'Not able to insert in Violation table')
                return None
        else:
            self.log.e(TAG, 'Device id is not string type')

    def update_violations(self, device_id):
        TAG = 'update violations'

        if isinstance(device_id, str):
            try:
                self.cursor.execute(""" UPDATE violations set
                    deleted = True WHERE device_id = {0} RETURNING id
                    """.format(adapt(device_id)))
            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                self.log.e(TAG, 'Not able to update in Violation table')

        else:
            self.log.e(TAG, 'Device id is not string type')

    def get_violation(self, violation_id, pluck=None):
        TAG = 'get_violation'

        if pluck is None:
            try:
                self.cursor.execute("SELECT *  FROM " + C.VIOLATION_TABLE +
                                    " WHERE " + C.VIOLATION_TABLE_ID +
                                    " = " + str(violation_id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return_dict = {}
                return_dict[C.VIOLATION_TABLE_ID] = row[0]
                return_dict[C.VIOLATION_TABLE_DEVICE] = row[1]
                return_dict[C.VIOLATION_TABLE_TIMESTAMP] = row[2]

                return return_dict
            else:
                self.log.e(
                    TAG,
                    'Not able to perform select operation on Violation table')
                return None
        elif isinstance(pluck, list):

            query_var = ','.join([str(i) for i in pluck])

            try:
                self.cursor.execute(
                    "SELECT " +
                    query_var +
                    " FROM " +
                    C.DEVICE_TABLE +
                    " WHERE " +
                    C.VIOLATION_TABLE_ID +
                    " = " +
                    str(violation_id))

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
                self.log.e(
                    TAG,
                    'Not Able to perform select operation on Violation table')
                return None
        else:
            self.log.e(TAG, 'Type of violation id is not string')
            return None

    def get_violations(self, device=None):
        TAG = 'get_violations'

        if device is None:
            try:
                self.cursor.execute(
                    "SELECT * FROM {0};".format(C.VIOLATION_TABLE))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.VIOLATION_TABLE_ID] = row[0]
                    return_dict[C.VIOLATION_TABLE_DEVICE] = row[1]
                    return_dict[C.VIOLATION_TABLE_TIMESTAMP] = row[2]
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(
                    TAG,
                    'Not able to perform select operation on Violation table')
                return None
        elif isinstance(device, str):
            try:
                self.cursor.execute("SELECT *  FROM " + C.VIOLATION_TABLE +
                                    " WHERE " + C.VIOLATION_TABLE_DEVICE +
                                    " = " + str(device))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.VIOLATION_TABLE_ID] = row[0]
                    return_dict[C.VIOLATION_TABLE_DEVICE] = row[1]
                    return_dict[C.VIOLATION_TABLE_TIMESTAMP] = row[2]
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(
                    TAG,
                    'Not Able to perform select operation on Violation table')
                return None
        else:
            self.log.e(TAG, 'Type of device id is not string')
            return None

    def get_violations_with_pages(self, company_id, offset=None, count=None):
        TAG = 'get_violations_with_pages'

        if offset is None:
            offset = 0

        if count is None:
            count = 'ALL'
        total_count = 0

        try:
            self.cursor.execute("""SELECT COUNT(*) FROM violations
                        INNER JOIN devices ON violations.device_id=devices.id
                        INNER JOIN users ON devices.user_id = users.id
                        INNER JOIN roles ON users.role_id=roles.id
                        INNER JOIN teams ON users.team_id=teams.id
                        WHERE users.company_id={0} AND users.deleted=False
                        AND teams.deleted = False AND roles.deleted=False
                        ;""".format(company_id))

            total_count = self.cursor.fetchone()[0]

            self.cursor.execute("""SELECT devices.udid, devices.os, users.id,
                        users.name, teams.name, roles.name,
                        violations.timestamp FROM violations
                        INNER JOIN devices ON violations.device_id=devices.id
                        INNER JOIN users ON devices.user_id = users.id
                        INNER JOIN roles ON users.role_id=roles.id
                        INNER JOIN teams ON users.team_id=teams.id
                        WHERE users.company_id={0} AND users.deleted=False
                        AND teams.deleted = False AND roles.deleted=False
                        ORDER BY violations.timestamp DESC
                        OFFSET {1} LIMIT {2};
                        """.format(company_id, offset, count))
        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None, total_count

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()
            return_array = []

            mapping_list = [
                'user_device',
                'user_device_os',
                'user_id',
                'user_name',
                'user_team',
                'user_role',
                'time_stamp']
            for row in rows:
                return_dict = dict(zip(mapping_list, row))
                return_array.append(return_dict)

            return return_array, total_count
        else:
            self.log.e(
                TAG,
                'Not able to perform select operation on Violation table')
            return None, total_count

    def get_violation_count(self, company_id, device_id=None):
        TAG = 'get_violation_count'
        if device_id is None and company_id:
            try:
                self.cursor.execute("""SELECT COUNT(*) FROM violations
                        INNER JOIN devices ON violations.device_id=devices.id
                        INNER JOIN users ON devices.user_id = users.id
                        WHERE users.company_id={0} AND users.deleted=False
                        AND violations.deleted = False;
                        """.format(str(company_id)))
            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                self.log.e(TAG, 'Not able to query in Violation table')
                return None
        elif isinstance(device_id, str):
            try:
                self.cursor.execute("SELECT COUNT(*) FROM " +
                                    C.VIOLATION_TABLE + " WHERE " +
                                    C.VIOLATION_TABLE_DEVICE + " = " +
                                    device_id)
            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                self.log.e(TAG, 'Not able to query in Violation table')
                return None
        else:
            self.log.e(TAG, 'Device id sent is not of string type')
            return None

if __name__ == '__main__':
    violation = ViolationsDBHelper()
    print violation.get_violation_count()
