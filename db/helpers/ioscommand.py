import json
# import psycopg2
from .base import *
from logger import Logger
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import adapt
from db.constants import Constants as C


class IOSCommandDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('IOSCommandDBHelper')
        self.command_tuples = (
            C.COMMAND_TABLE_ID, C.COMMAND_TABLE_COMMAND_UUID,
            C.COMMAND_TABLE_EXECUTED, C.COMMAND_TABLE_DEVICE,
            C.COMMAND_TABLE_ACTION, C.COMMAND_TABLE_RESULT,
            C.COMMAND_TABLE_ATTRIBUTE, C.COMMAND_TABLE_SENT_ON,
            C.COMMAND_TABLE_EXECUTED_ON)

    def add_command(self, command):
        TAG = 'add_command'

        if isinstance(command, dict):
            if C.COMMAND_TABLE_COMMAND_UUID in command:
                if C.COMMAND_TABLE_ACTION in command:
                    if C.COMMAND_TABLE_ATTRIBUTE in command:
                        try:
                            self.cursor.execute(
                                "INSERT INTO " + C.COMMAND_TABLE + "(" +
                                C.COMMAND_TABLE_COMMAND_UUID + "," +
                                C.COMMAND_TABLE_DEVICE + "," +
                                C.COMMAND_TABLE_ACTION + "," +
                                C.COMMAND_TABLE_ATTRIBUTE + "," +
                                C.COMMAND_TABLE_EXECUTED +
                                ") VALUES(%s,%s,%s,%s,%s) RETURNING id",
                                [command[C.COMMAND_TABLE_COMMAND_UUID],
                                    command[C.COMMAND_TABLE_DEVICE],
                                    command[C.COMMAND_TABLE_ACTION],
                                    command[C.COMMAND_TABLE_ATTRIBUTE],
                                    str(False)])

                        except Exception as err:
                            self.log.e(TAG, 'Exception : ' + repr(err))
                            return None

                        if self.cursor.rowcount > 0:
                            row = self.cursor.fetchone()
                            return row[0]
                        else:
                            self.log.e(TAG, 'Not able to insert in IOS \
COMMAND table')
                            return None
                    else:
                        self.log.e(TAG,
                                   'Attribute field not found in dictionary')
                        return None
                else:
                    self.log.e(TAG, 'Action is not found in dictionary')
                    return None
            else:
                self.log.e(TAG, 'COmmand UUID not found in dictionary')
                return None
        else:
            self.log.e(TAG, 'dictionary not sent for insertion')
            return None

    def get_not_executed(self, device_id, pluck=None):
        TAG = 'get_not_executed'

        if isinstance(device_id, str):
            if pluck is None:
                try:
                    self.cursor.execute(
                        "SELECT * FROM " + C.COMMAND_TABLE + " WHERE " +
                        C.COMMAND_TABLE_EXECUTED + " = False AND " +
                        C.COMMAND_TABLE_DEVICE + " = '" + str(device_id) + "'")
                except Exception as err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = dict(zip(self.command_tuples, row))
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.i(TAG, 'No row to select')
                    return []

            elif isinstance(pluck, list):
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute(
                        "SELECT " + query_var + " FROM " + C.COMMAND_TABLE +
                        " WHERE " + C.COMMAND_TABLE_EXECUTED + " = False AND "
                        + C.COMMAND_TABLE_DEVICE + " = '" + device_id + "'")

                except Exception as err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        i = 0
                        for item in pluck:
                            return_dict[item] = row[i]
                            i = i + 1
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.i(TAG, 'No row to select')
                    return []
            else:
                self.log.e(TAG, 'Type of pluck is not list')
                return None
        else:
            self.log.e(TAG, 'udid is not string')
            return None

    def toggle_executed(self, uuid, device_id, status):
        TAG = 'set_executed'

        if isinstance(uuid, str) and isinstance(device_id, str):
            try:
                self.cursor.execute(
                    "UPDATE " + C.COMMAND_TABLE + " SET " +
                    C.COMMAND_TABLE_EXECUTED + " = " + str(status) +
                    " WHERE " + C.COMMAND_TABLE_COMMAND_UUID + " = '"
                    + uuid + "' AND " + C.COMMAND_TABLE_DEVICE + " = '"
                    + device_id + "'")

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG, 'UUID and UDID both are not string')
            return False

    def update_result(self, uuid, device_id, result):
        TAG = 'update_result'

        if isinstance(uuid, str) and isinstance(device_id, str):
            try:
                self.cursor.execute(
                    """UPDATE ios_commands  SET {0} = {1},
                    {2}=now() WHERE {3}='{4}' AND {5}={6}
                    ;""".format(
                        C.COMMAND_TABLE_RESULT,
                        adapt(
                            json.dumps(result)),
                        C.COMMAND_TABLE_EXECUTED_ON,
                        C.COMMAND_TABLE_COMMAND_UUID,
                        str(uuid),
                        C.COMMAND_TABLE_DEVICE,
                        device_id))

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG, 'UUID, UDID and result are not string')
            return False

    def get_result(self, uuid):
        TAG = 'get_result'

        if isinstance(uuid, str):
            try:
                self.cursor.execute(
                    "SELECT  " + C.COMMAND_TABLE_RESULT + "," +
                    C.COMMAND_TABLE_DEVICE + "," +
                    C.COMMAND_TABLE_EXECUTED_ON + " FROM " + C.COMMAND_TABLE +
                    " WHERE " + C.COMMAND_TABLE_EXECUTED + " = True AND " +
                    C.COMMAND_TABLE_COMMAND_UUID + " = '" + uuid + "'" +
                    " ORDER BY " + C.COMMAND_TABLE_EXECUTED +
                    " DESC LIMIT 10;")
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.COMMAND_TABLE_RESULT] = row[0]
                    return_dict[C.COMMAND_TABLE_DEVICE] = row[1]
                    return_dict[C.COMMAND_TABLE_EXECUTED_ON] = row[2]
                    return_array.append(return_dict)
                return return_array
            else:
                return None
        else:
            self.log.e(TAG, 'UUID is not string')
            return None

    def get_command_attributes(self, uuid):
        TAG = 'get_command_attributes'

        if isinstance(uuid, str):
            try:
                self.cursor.execute(
                    "SELECT * FROM " + C.COMMAND_TABLE + " WHERE " +
                    C.COMMAND_TABLE_COMMAND_UUID + " = '" + str(uuid) +
                    "'")

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return_dict = dict(zip(self.command_tuples, row))

                return return_dict
            else:
                self.log.i(TAG, 'No row to select')
                return None
        else:
            self.log.e(TAG, 'uuid is not string')
            return None

    def get_command_count(self, uuid):
        TAG = 'get_command_count'

        if isinstance(uuid, str):
            try:
                self.cursor.execute(
                    "SELECT COUNT(*) FROM " + C.COMMAND_TABLE + " WHERE "
                    + C.COMMAND_TABLE_COMMAND_UUID + " = '" + str(uuid)
                    + "'")

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return row[0]
            else:
                self.log.i(TAG, 'No row to select')
                return 0
        else:
            self.log.e(TAG, 'udid is not string')
            return None


if __name__ == '__main__':
    print 'hi'
    helper = IOSCommandDBHelper()
    json_dict = {'attributes': 'abc'}
    json_val = json.dumps(json_dict)
    command_dict = {
        C.COMMAND_TABLE_COMMAND_UUID: 'nsi8uyjassvu8a9a9',
        C.COMMAND_TABLE_ACTION: 'policy',
        C.COMMAND_TABLE_ATTRIBUTE: json_val
    }
#     print helper.add_command(command_dict)
    print helper.get_not_executed('dhduidid0duuidk')
    print helper.get_not_executed('dhduidid0duuidk',
                                  [C.COMMAND_TABLE_ACTION,
                                   C.COMMAND_TABLE_RESULT, C.COMMAND_TABLE_ID])
#    print helper.set_executed('nsi8uyjassvu8a9a9', 'dhduidid0duuidk')
    print helper.update_result('nsi8uyjassvu8a9a9', 'dhduidid0duuidk',
                               '<xml> abc </xml>')
