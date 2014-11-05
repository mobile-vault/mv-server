import datetime
# import json

# import psycopg2
from .base import *
from logger import Logger
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.constants import Constants as C


class SessionDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('SessionDBHelper')

        self.session_tuple = (
            C.SESSION_TABLE_ID,
            C.SESSION_TABLE_CREATED_ON,
            C.SESSION_TABLE_DESTROYED_ON,
            C.SESSION_TABLE_IP,
            C.SESSION_TABLE_INVALID,
            C.SESSION_TABLE_USER_AGENT,
            C.SESSION_TABLE_USER)

    def add_session(self, session):
        TAG = 'add_session'

        if isinstance(session, dict):
            if (C.SESSION_TABLE_IP in session and
                    C.SESSION_TABLE_USER in session and
                    C.SESSION_TABLE_USER_AGENT in session):

                key_str = ''
                value_str = ''

                for key, value in session.iteritems():

                    key_str += str(key) + ","

                    if (str(key) == C.SESSION_TABLE_IP or
                        str(key) == C.SESSION_TABLE_USER or
                        str(key) == C.SESSION_TABLE_USER_AGENT or
                        str(key) == C.SESSION_TABLE_CREATED_ON or
                            str(key) == C.SESSION_TABLE_DESTROYED_ON):

                        value_str += "'" + str(value) + "',"

                    else:
                        value_str += str(value) + ","

                key_str = key_str[:-1]
                value_str = value_str[:-1]

                try:
                    self.cursor.execute("INSERT INTO " +
                                        C.SESSION_TABLE +
                                        "(" +
                                        str(key_str) +
                                        "," +
                                        C.SESSION_TABLE_CREATED_ON +
                                        "," +
                                        C.SESSION_TABLE_INVALID +
                                        ") VALUES(" +
                                        str(value_str) +
                                        ",'" +
                                        str(datetime.datetime.now()) +
                                        "', False) RETURNING id")
                except Exception as err:
                    self.log.e(TAG, 'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return row[0]
                else:
                    self.log.e(TAG, 'Not abe to insert in device table')
                    return None
            else:
                self.log.e(
                    TAG,
                    'IP/UserID/User Agent is not sent in insertion dictionary')

    def get_session(self, id, pluck=None):
        TAG = 'get_session'

        if isinstance(id, str):
            if pluck is None:
                try:
                    self.cursor.execute(
                        "SELECT * FROM " +
                        C.SESSION_TABLE +
                        " WHERE " +
                        C.SESSION_TABLE_ID +
                        " = " +
                        id)
                except Exception as err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = dict(zip(self.session_tuple, row))
                else:
                    self.log.e(TAG, 'Not able to perform select operation \
on Session Table')
                    return None

            elif isinstance(pluck, list):

                query_var = ''

                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute(
                        "SELECT " +
                        query_var +
                        " FROM " +
                        C.SESSION_TABLE +
                        " WHERE " +
                        C.SESSION_TABLE_ID +
                        " = " +
                        id)
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

    def get_sessions(self, filter=None):
        TAG = 'get_sessions'

        try:
            self.cursor.execute("SELECT *  FROM " + C.SESSION_TABLE)
        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()
            return_array = []

            for row in rows:
                return_dict = dict(zip(self.session_tuple, row))
                return_array.append(return_dict)
            return return_array
        else:
            self.log.e(
                TAG,
                'Not able to perform select operation on Session table')
            return None

    def destroy_session(self, id):
        TAG = 'destroy_session'

        if isinstance(id, str):
            print(
                "UPDATE " + C.SESSION_TABLE + " SET " +
                C.SESSION_TABLE_INVALID + " = True AND " +
                C.SESSION_TABLE_DESTROYED_ON + " = '" +
                str(datetime.datetime.now()) + "' WHERE " +
                C.SESSION_TABLE_ID + " = " + str(id))

            try:
                self.cursor.execute("UPDATE " +
                                    C.SESSION_TABLE +
                                    " SET " +
                                    C.SESSION_TABLE_INVALID +
                                    " = True, " +
                                    C.SESSION_TABLE_DESTROYED_ON +
                                    " = '" +
                                    str(datetime.datetime.now()) +
                                    "' WHERE " +
                                    C.SESSION_TABLE_ID +
                                    " = " +
                                    str(id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Not able to update the Session table')
                return False
        else:
            self.log.e(TAG, 'ID is not string ')
            return False

    def validate_session(self, id, ip, user_agent):
        session = self.get_session(
            id, [
                C.SESSION_TABLE_IP, C.SESSION_TABLE_USER_AGENT])
        if session[
                C.SESSION_TABLE_IP] == ip and session[
                C.SESSION_TABLE_USER_AGENT] == user_agent:
            return True
        else:
            return False

    def get_sessions_with_page(self, company_id, page=None, count=None):
        TAG = 'get_logs'

        skip = 0
        limit = 0

        if count is None:
            count = 5

        if page is None:
            skip = 0
        else:
            skip = page

#        skip = int(page) * int(count) - int(count)
        limit = int(count)

        try:
            self.cursor.execute("""SELECT s.id, s.user_id, s.ip,
                            s.user_agent, s.invalid, s.created_on,
                            s.destroyed_on, l.name FROM
                            sessions as s INNER JOIN admin_profile as l
                            ON s.user_id=l.id WHERE l.company_id={0}
                            AND l.deleted=False ORDER BY s.created_on
                            DESC OFFSET {1} LIMIT {2}
                            ;""".format(company_id, str(skip), str(limit)))

        except Exception as err:
            self.log.e(TAG, 'Exception : ' + repr(err))
            return None

        if self.cursor.rowcount > 0:

            mapping_tuple = ('id', 'user_id', 'ip', 'user_agent', 'invalid',
                             'created_on', 'destroyed_on', 'username')
            rows = self.cursor.fetchall()
            return_array = []
            for row in rows:
                return_dict = dict(zip(mapping_tuple, row))
                return_array.append(return_dict)
            return return_array
        else:
            self.log.e(TAG, 'Not able to select from Logs table')
            return None

    def get_sessions_count(self, company_id):
        TAG = 'get_sessions_count'
        try:
            self.cursor.execute("""SELECT COUNT(DISTINCT s.id) FROM
                            sessions as s INNER JOIN admin_profile as l
                            ON s.user_id=l.id WHERE l.company_id={0}
                            AND l.deleted=False""".format(company_id))
        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            self.log.e(
                TAG,
                'Not able to perform select operation on User table')
            return None


if __name__ == '__main__':
    session = SessionDBHelper()
    session_dict = {
        C.SESSION_TABLE_IP: '192.168.2.1',
        C.SESSION_TABLE_USER: '1',
        C.SESSION_TABLE_USER_AGENT: 'Firefox'
    }
#     print session.add_session(session_dict)
    print session.destroy_session('10')
    print session.get_session('9')
    print session.get_session('9', [C.SESSION_TABLE_CREATED_ON,
                                    C.SESSION_TABLE_USER_AGENT])
    print session.get_sessions(None)
    print session.validate_session('9', '192.168.2.1', 'Firefox')
