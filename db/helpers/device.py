from user import *

import psycopg2
from base import *
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import adapt
from db.constants import Constants as C


class DeviceDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('DeviceDBHelper')


    def is_device_valid(self,id):
        TAG='is_device_valid'
        try:
            self.cursor.execute("SELECT * FROM " + C.DEVICE_TABLE +\
                     " WHERE id = " + str(id) + " AND " \
                      + C.DEVICE_TABLE_DELETED + " = False")
            if self.cursor.rowcount > 0:
                return True
            return False
        except Exception, err:
            self.log.e(TAG, repr(err))
            return None


    def add_device(self, device):
        TAG = 'add_device'

        ## if user_id, udid and os is present then only we can do entry
        if type(device) == dict and C.DEVICE_TABLE_USER in device:

            if UserDBHelper().is_user_valid(str(device.get('user_id'))):
                if device.has_key(C.DEVICE_TABLE_OS):
                    if device.has_key(C.DEVICE_TABLE_UDID):
                        try:
                            self.cursor.execute("""INSERT INTO devices
                               (os, udid, user_id) VALUES({0}, {1}, {2})
                               RETURNING id""".format(adapt(device.get('os')),
                                 adapt(device.get('udid')),
                                  adapt(device.get('user_id'))))

                        except Exception,err:
                            self.log.e(TAG,'Exception : ' + repr(err))
                            return None
                        if self.cursor.rowcount > 0:
                            row = self.cursor.fetchone()
                            return row[0]
                        else:
                            self.log.e(TAG,'Not abe to insert in device table')
                            return None
                    else:
                        self.log.e(TAG,'UDID not found in dictionary')
                        return None
                else:
                    self.log.e(TAG, 'OS is not found in dictionary')
                    return None
            else:
                self.log.e(TAG, 'USER ID not found in dictionary')
                return None



    def get_device(self,id,pluck=None, status=False):
        TAG = 'get_device'

        if type(id) == str:
            if pluck is None:
                try:
                    self.cursor.execute("SELECT * FROM " + C.DEVICE_TABLE + \
                        " WHERE "+ C.DEVICE_TABLE_DELETED+ " = {0}".format(
                            status) + " and " \
                        + C.DEVICE_TABLE_ID + " = " + id)
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = {}
                    return_dict[C.DEVICE_TABLE_ID] = row[0]
                    return_dict[C.DEVICE_TABLE_NAME] = row[1]
                    return_dict[C.DEVICE_TABLE_USER] = row[2]
                    return_dict[C.DEVICE_TABLE_UDID] = row[3]
                    return_dict[C.DEVICE_TABLE_OS] = row[4]
                    return_dict[C.DEVICE_TABLE_OS_VERSION] = row[6]
                    return return_dict
                else:
                    self.log.e(TAG,'Not able to perform select operation on device table')
                    return None
            elif type(pluck) == list:
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute("SELECT " + query_var + " FROM " + C.DEVICE_TABLE + " WHERE " + C.DEVICE_TABLE_ID + " = " + id)
                except Exception, err:
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
            self.log.e(TAG,'ID is not string')
            return None



    def update_device(self,id,device):
        TAG = 'update_device'

        if type(id) == str and type(device) == dict:
            query_str = ''
            for key, value in device.iteritems():
                query_str += " {0} = {1}, ".format(key, adapt(value))

            query_str = query_str.rstrip(', ')
            print 'query str here \n', query_str
            try:
                self.cursor.execute("""UPDATE {0} SET {1} WHERE {2}={3};
                                    """.format(C.DEVICE_TABLE, query_str,
                                C.DEVICE_TABLE_ID, str(id)))
            except Exception, err:
                print 'query was \n', self.cursor.query
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                    return True
            else:
                self.log.e(TAG, 'Not able to update the device table')
                return False
        else:
            self.log.e(TAG,'ID is not string or Second parameter is not dictionary')
            return False


    def delete_device(self, device_id):
        TAG = 'delete_device'

        try:
            self.cursor.execute("UPDATE " + C.DEVICE_TABLE + " SET " + \
                    C.DEVICE_TABLE_DELETED + " = True  WHERE " + \
                        C.DEVICE_TABLE_ID + " = " + str(device_id))
        except Exception, err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return False

        if self.cursor.rowcount > 0:
            return True
        else:
            self.log.e(TAG,'Not able to delete from device table')
            return False


    def get_devices_of_user(self, user_id, pluck=None):
        TAG= 'get_devices_of_user'

        if isinstance(user_id, str):

            if pluck is None:
                try:
                    self.cursor.execute("""SELECT * FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE users.id={0}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(user_id))

                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        return_dict[C.DEVICE_TABLE_ID] = row[0]
                        return_dict[C.DEVICE_TABLE_NAME] = row[1]
                        return_dict[C.DEVICE_TABLE_USER] = row[2]
                        return_dict[C.DEVICE_TABLE_UDID] = row[3]
                        return_dict[C.DEVICE_TABLE_OS] = row[4]
                        return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.e(TAG,'Not able to perform select operation on device table')
                    return None

            elif type(pluck) == list:

                query_var = ', '.join(['devices.' + str(i) for i in pluck])

                try:
                    self.cursor.execute("""SELECT {0} FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE users.id={1}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(query_var, user_id))

                except Exception, err:
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
                self.log.e(TAG, 'Type of pluck is not list')
                return None
        else:
            self.log.e(TAG,'ID is not string')
            return None


    def get_devices_of_role(self, role_id, pluck=None):
        TAG= 'get_devices_of_role'

        if type(role_id) == str:
            if pluck is None:
                try:
                    self.cursor.execute("""SELECT * FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE roles.id={0}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(role_id))

                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        return_dict[C.DEVICE_TABLE_ID] = row[0]
                        return_dict[C.DEVICE_TABLE_NAME] = row[1]
                        return_dict[C.DEVICE_TABLE_USER] = row[2]
                        return_dict[C.DEVICE_TABLE_UDID] = row[3]
                        return_dict[C.DEVICE_TABLE_OS] = row[4]
                        return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.e(TAG, 'Not able to perform select operation on \
                         device table')
                    return None
            elif type(pluck) == list:

                query_var = ', '.join(['devices.' + str(i) for i in pluck])

                try:
                    self.cursor.execute("""SELECT {0} FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE roles.id={1}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(query_var, role_id))

                except Exception, err:
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
                self.log.e(TAG, 'Type of pluck is not list')
                return None
        else:
            self.log.e(TAG,'Role is not string')
            return None


    def get_devices_of_team(self, team_id, pluck=None):
        TAG= 'get_devices_of_team'

        if type(team_id) == str:
            if pluck is None:
                try:
                    self.cursor.execute("""SELECT * FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE teams.id={0}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(team_id))

                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        return_dict[C.DEVICE_TABLE_ID] = row[0]
                        return_dict[C.DEVICE_TABLE_NAME] = row[1]
                        return_dict[C.DEVICE_TABLE_USER] = row[2]
                        return_dict[C.DEVICE_TABLE_UDID] = row[3]
                        return_dict[C.DEVICE_TABLE_OS] = row[4]
                        return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.e(TAG,'Not able to perform select operation on device table')
                    return None

            elif type(pluck) == list:
                query_var = ', '.join(['devices.' + str(i) for i in pluck])

                try:
                    self.cursor.execute("""SELECT {0} FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE teams.id={1}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(query_var, team_id))
                except Exception, err:
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
                self.log.e(TAG, 'Type of pluck is not list')
                return None
        else:
            self.log.e(TAG,'team is not string')
            return None



    def get_device_with_udid(self, udid, status=False, pluck=None):
        TAG='get_device_with_udid'

        if type(udid) == str:
            if pluck is None:

                try:
                    self.cursor.execute("SELECT " + C.DEVICE_TABLE_ID + ", " \
                            + C.DEVICE_TABLE_NAME + ", " + C.DEVICE_TABLE_USER +\
                             ", " + C.DEVICE_TABLE_UDID + ", " + \
                            C.DEVICE_TABLE_OS + ", " + C.DEVICE_TABLE_DELETED + \
                        " FROM " + C.DEVICE_TABLE + " WHERE " +\
                        C.DEVICE_TABLE_UDID + " = {0}".format(adapt(udid))+" AND "\
                            + C.DEVICE_TABLE_DELETED + " = {0}".format(status))
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        return_dict[C.DEVICE_TABLE_ID] = row[0]
                        return_dict[C.DEVICE_TABLE_NAME] = row[1]
                        return_dict[C.DEVICE_TABLE_USER] = row[2]
                        return_dict[C.DEVICE_TABLE_UDID] = row[3]
                        return_dict[C.DEVICE_TABLE_OS] = row[4]
                        return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.e(TAG,'Not able to perform select operation on device table')
                    return None

            elif type(pluck) == list:
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute("SELECT " + query_var + " FROM " + C.DEVICE_TABLE + " WHERE " + C.DEVICE_TABLE_UDID + \
                                        " = '" + str(udid) + "' AND " + C.DEVICE_TABLE_DELETED + " = False")
                except Exception, err:
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
                self.log.e(TAG, 'Type of pluck is not list')
                return None
        else:
            self.log.e(TAG,'udid is not string')
            return None


    def get_devices(self, company_id):
        TAG= 'get_devices'

        try:
            self.cursor.execute("""SELECT * FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    INNER JOIN roles ON roles.id=users.role_id
                    INNER JOIN teams ON teams.id=users.team_id
                    WHERE users.company_id={0}
                    AND users.deleted=False AND devices.deleted=False
                    AND roles.deleted=False AND teams.deleted=False
                    ;""".format(company_id))
        except Exception, err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()
            return_array = []
            for row in rows:
                return_dict = {}
                return_dict[C.DEVICE_TABLE_ID] = row[0]
                return_dict[C.DEVICE_TABLE_NAME] = row[1]
                return_dict[C.DEVICE_TABLE_USER] = row[2]
                return_dict[C.DEVICE_TABLE_UDID] = row[3]
                return_dict[C.DEVICE_TABLE_OS] = row[4]
                return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                return_array.append(return_dict)
            return return_array
        else:
            self.log.e(TAG,'Not able to perform select operation on device table')
            return None


    def get_devices_with_pages(self, filter_dict=None, page = None, count = None, sort_by = None):
        TAG = 'get_devices_with_pages'
        query_string = ''
        skip = 0
        limit = 0
        if sort_by is None:
            sort_by = C.USER_TABLE_NAME

        if count == None:
            count = 10

        if page == 0 or page is None:
            page = 1

        skip = page * count - count
        limit = count

        if type(filter_dict) == dict:
            for key, value in filter_dict.iteritems():
                query_string += " {0} = {1} AND ".format(key, adapt(value))

            query_string = query_string.rstrip('AND ')

            try:
                self.cursor.execute("SELECT *  FROM " + C.DEVICE_TABLE + " WHERE " + query_string + " ORDER BY " + str(sort_by) + " LIMIT " + str(limit) + " OFFSET " + str(skip))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.DEVICE_TABLE_ID] = row[0]
                    return_dict[C.DEVICE_TABLE_NAME] = row[1]
                    return_dict[C.DEVICE_TABLE_USER] = row[2]
                    return_dict[C.DEVICE_TABLE_UDID] = row[3]
                    return_dict[C.DEVICE_TABLE_OS] = row[4]
                    return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(TAG,'Not able to perform select operation on Device table')
                return None
        elif filter_dict is None:
            try:
                self.cursor.execute("SELECT *  FROM " + C.DEVICE_TABLE + " ORDER BY " + str(sort_by) + " LIMIT " + str(limit) + " OFFSET " + str(skip))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.DEVICE_TABLE_ID] = row[0]
                    return_dict[C.DEVICE_TABLE_NAME] = row[1]
                    return_dict[C.DEVICE_TABLE_USER] = row[2]
                    return_dict[C.DEVICE_TABLE_UDID] = row[3]
                    return_dict[C.DEVICE_TABLE_OS] = row[4]
                    return_dict[C.DEVICE_TABLE_DELETED] = row[5]
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(TAG,'Not able to perform select operation on Device table')
                return None
        else:
            self.log.e(TAG, 'filter_dict is not of type dict')
            return None


    def get_devices_count(self, company_id, version=None):
        TAG = 'get_devices_count'

        base_query = """SELECT COUNT(*)  FROM devices
                        INNER JOIN users ON devices.user_id = users.id
                        WHERE users.company_id={0} AND users.deleted=False
                        AND devices.deleted=False
                    """

        if version:
            query = base_query + " AND devices.os_version='{1}';"
            query = query.format(company_id, version)
        else:
            query = base_query + ";"
            query = query.format(company_id)


        try:
            self.cursor.execute(query)

        except Exception, err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            self.log.e(TAG,'Not able to perform select operation on Device table')
            return None

    def is_udid_registered(self,udid):
        TAG = 'is_udid_registered'
        if type(udid) == str:
            try:
                self.cursor.execute("SELECT * FROM " + C.DEVICE_TABLE + " WHERE " + C.DEVICE_TABLE_DELETED + " = False AND " + C.DEVICE_TABLE_UDID + " = '" + str(udid) + "'")
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.i(TAG,'Not able to perform select operation on Device table')
                return False

    def get_os_distinct_version(self, company_id, os_name):
        TAG = 'get_os_distinct_version'
        try:
            self.cursor.execute("""SELECT DISTINCT  devices.os_version FROM devices
                            INNER JOIN users ON devices.user_id=users.id
                            WHERE users.company_id={0}
                            AND users.deleted=False AND devices.os='{1}'
                            AND devices.deleted = False;
                            """.format(company_id, os_name))
        except Exception, err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return False

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()
            return_array = []
            for row in rows:
                return_array.append(row[0])

            return return_array
        else:
            self.log.e(TAG,'Not able to perform select operation on Device table')
            return False


if __name__ == '__main__':
    device = DeviceDBHelper()
    pass
