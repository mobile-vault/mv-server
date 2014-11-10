# import json
# import ipdb
# import psycopg2
from logger import Logger
from psycopg2.extensions import adapt
from db.constants import Constants as C
from db.helpers.base import *
from psycopg2 import IntegrityError


class UserDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('UserDBHelper')

    def is_user_valid(self, user_id):
        TAG = 'is_user_valid'

        if isinstance(user_id, str):
            try:
                self.cursor.execute(
                    """SELECT * FROM {0} WHERE {1} = False
                    AND {2} = {3};""".format(
                    C.USER_TABLE,
                    C.USER_TABLE_DELETED,
                    C.USER_TABLE_ID,
                    user_id))

            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG, 'User id is not string ')
            return False

    def add_user_if_not_exists(self, user):
        TAG = 'add_user_if_not_exists'

        duplicate = None

        if isinstance(user, dict):
            if C.USER_TABLE_EMAIL in user and \
                    C.USER_TABLE_NAME in user and \
                    C.USER_TABLE_COMPANY in user:

                from validate_email import validate_email

                if validate_email(user[C.USER_TABLE_EMAIL]):

                    try:
                        self.cursor.execute("SELECT * FROM " +
                                            C.USER_TABLE +
                                            " WHERE " +
                                            C.USER_TABLE_DELETED +
                                            " = False AND " +
                                            C.USER_TABLE_EMAIL +
                                            " = '" +
                                            str(user[C.USER_TABLE_EMAIL]) +
                                            "'")
                    except Exception as err:
                        self.log.e(TAG, 'Exception : ' + repr(err))
                        return None

                    if self.cursor.rowcount > 0:
                        self.log.i(
                            TAG, str(
                                user[
                                    C.USER_TABLE_NAME]) +
                            " exist already sending the id of that user")

                        row = self.cursor.fetchone()
                        duplicate = True

                        return row[0], duplicate

                    elif self.cursor.rowcount == 0:
                        key_str = ''
                        value_str = ''

                        for key, value in user.iteritems():
                            key_str += str(key) + ","

                            if str(key) == C.USER_TABLE_NAME or str(key)\
                                    == C.USER_TABLE_EMAIL:
                                value_str += "'" + str(value) + "',"
                            else:
                                value_str += str(value) + ","

                        key_str = key_str[:-1]
                        value_str = value_str[:-1]

                        print "INSERT INTO " + C.USER_TABLE + "(" \
                            + str(key_str) + ") VALUES(" + str(value_str) + ")\
                                 RETURNING id"
                        try:
                            self.cursor.execute(
                                "INSERT INTO " +
                                C.USER_TABLE +
                                "(" +
                                str(key_str) +
                                "," +
                                C.USER_TABLE_DELETED +
                                ") VALUES(" +
                                str(value_str) +
                                ", False) RETURNING id")

                        except IntegrityError as err:
                            self.log.e(TAG, 'Exception : ' + repr(err))
                            self.cursor.execute(
                                """ UPDATE users
                                set deleted=False, name={0}, role_id = {1},
                                team_id={2}, company_id={3} WHERE {4}={5}
                                RETURNING id
                                """.format(
                                adapt(
                                    user.get('name')),
                                user.get('role_id'), user.get('team_id'),
                                user.get('company_id'), 'email',
                                adapt(user.get('email'))))

                        if self.cursor.rowcount > 0:
                            row = self.cursor.fetchone()

                            return row[0], duplicate

                        else:
                            self.log.e(TAG, 'Not able to insert in TEam table')
                            return None, duplicate
                    else:
                        self.log.e(TAG, 'Not able to perform select query')
                        return None, duplicate
                else:
                    self.log.e(TAG, 'Email is not valid')
                    return None, duplicate
        else:
            self.log.e(TAG, 'Dictionary not sent ')
            return None, duplicate

    def add_user(self, user):
        TAG = 'add_user'

        if isinstance(user, dict):

            if C.USER_TABLE_EMAIL in user and\
                    C.USER_TABLE_NAME in user and \
                    C.USER_TABLE_COMPANY in user:

                from validate_email import validate_email

                if validate_email(user[C.USER_TABLE_EMAIL]):
                    try:
                        self.cursor.execute("SELECT * FROM " +
                                            C.USER_TABLE +
                                            " WHERE " +
                                            C.USER_TABLE_DELETED +
                                            " = False AND " +
                                            C.USER_TABLE_NAME +
                                            " = '" +
                                            str(user[C.USER_TABLE_NAME]) +
                                            "'")
                    except Exception as err:
                        self.log.e(TAG, 'Exception : ' + repr(err))
                        return None

                    if self.cursor.rowcount > 0:
                        self.log.i(
                            TAG, str(
                                user[
                                    C.USER_TABLE_NAME]) +
                            " exist already sending the id of that user")

                        row = self.cursor.fetchone()
                        return row[0]

                    elif self.cursor.rowcount == 0:
                        key_str = ''
                        value_str = ''

                        for key, value in user.iteritems():
                            key_str += str(key) + ","

                            if str(key) == C.USER_TABLE_NAME or str(key)\
                                    == C.USER_TABLE_EMAIL:
                                value_str += "'" + str(value) + "',"
                            else:
                                value_str += str(value) + ","

                        key_str = key_str[:-1]
                        value_str = value_str[:-1]

                        print "INSERT INTO " + C.USER_TABLE + "(" +\
                            str(key_str) + ") VALUES(" +\
                            str(value_str) + ") RETURNING id"
                        try:
                            self.cursor.execute(
                                "INSERT INTO " +
                                C.USER_TABLE +
                                " (" +
                                str(key_str) +
                                "," +
                                C.USER_TABLE_DELETED +
                                ") VALUES(" +
                                str(value_str) +
                                ", False) RETURNING id")
                        except Exception as err:
                            self.log.e(TAG, 'Exception : ' + repr(err))
                            return None

                        if self.cursor.rowcount > 0:
                            row = self.cursor.fetchone()
                            return row[0]
                        else:
                            self.log.e(TAG, 'Not able to insert in TEam table')
                            return None
                    else:
                        self.log.e(TAG, 'Not able to perform select query')
                        return None
                else:
                    self.log.e(TAG, 'Email is not valid')
                    return None
        else:
            self.log.e(TAG, 'Dictionary not sent ')
            return None

    def get_user_with_email(self, email):
        TAG = 'get_user_with_email'
        if email is not None:
            try:
                self.cursor.execute(
                    "SELECT * FROM users WHERE deleted=FALSE AND EMAIL='{0}'".format(email))

                print self.cursor.query

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = {}
                    return_dict[C.USER_TABLE_ID] = row[0]
                    return_dict[C.USER_TABLE_EMAIL] = row[1]
                    return_dict[C.USER_TABLE_NAME] = row[2]
                    return_dict[C.USER_TABLE_ROLE] = row[3]
                    return_dict[C.USER_TABLE_TEAM] = row[4]
                    return_dict[C.USER_TABLE_POLICY] = row[5]
                    return_dict[C.USER_TABLE_COMPANY] = row[6]
                    return_dict[C.USER_TABLE_DELETED] = row[7]
                    return return_dict

                else:
                    return None
            except Exception as err:
                self.log.e(TAG, repr(err))
                return None
        else:
            return None

    def get_user(self, user_id, company_id=None, pluck=None):
        TAG = 'get_user'

        if isinstance(user_id, str):
            if pluck is None:

                base_query = """SELECT * FROM users WHERE
                     users.deleted=False AND users.id = {0}""".format(
                    user_id)

                if company_id:
                    base_query += " AND users.company_id = {0};".format(
                        company_id)

                try:
                    print "\n here is user_id \n", user_id
                    self.cursor.execute(base_query)
                except Exception as err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = {}
                    return_dict[C.USER_TABLE_ID] = row[0]
                    return_dict[C.USER_TABLE_EMAIL] = row[1]
                    return_dict[C.USER_TABLE_NAME] = row[2]
                    return_dict[C.USER_TABLE_ROLE] = row[3]
                    return_dict[C.USER_TABLE_TEAM] = row[4]
                    return_dict[C.USER_TABLE_POLICY] = row[5]
                    return_dict[C.USER_TABLE_COMPANY] = row[6]
                    return_dict[C.USER_TABLE_DELETED] = row[7]
                    return return_dict
                else:
                    self.log.e(
                        TAG,
                        'Not able to perform select operation on User table')
                    return None

            elif isinstance(pluck, list):

                query_var = ', '.join([str(i) for i in pluck])

                base_query = """SELECT {0} FROM users WHERE
                     users.deleted=False AND users.id = {1}""".format(
                    query_var, user_id)

                if company_id:
                    base_query += " AND users.company_id = {0};".format(
                        company_id)

                try:
                    print "\n here is user_id \n", user_id
                    self.cursor.execute(base_query)

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

    def update_user(self, user_id, user_dict):
        TAG = 'update_user'

        if isinstance(user_id, str) and isinstance(user_dict, dict):
            try:
                self.cursor.execute(
                    """UPDATE {0} SET {1}='{2}', {3}={4},
                                 {5}={6} WHERE {7} = False AND {8} = {9}
                                 ;""".format(
                    C.USER_TABLE, C.USER_TABLE_NAME, user_dict.get(
                        C.USER_TABLE_NAME), C.USER_TABLE_TEAM, user_dict.get(
                        C.USER_TABLE_TEAM), C.USER_TABLE_ROLE, user_dict.get(
                        C.USER_TABLE_ROLE), C.USER_TABLE_DELETED,
                    C.USER_TABLE_ID, user_id))

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG,
                           'Either user is deleted or not in the user table')
                return False
        else:
            self.log.e(
                TAG,
                'ID is not string or Second parameter is not dictionary')
            return False

    def update_user_role(self, user_id, role_id):
        TAG = 'update_user_role'

        if isinstance(user_id, str) and isinstance(role_id, str):
            try:
                self.cursor.execute(
                    "UPDATE " +
                    C.USER_TABLE +
                    " SET " +
                    C.USER_TABLE_ROLE +
                    " = " +
                    str(role_id) +
                    " WHERE " +
                    C.USER_TABLE_DELETED +
                    " = False AND " +
                    C.USER_TABLE_ID +
                    " = " +
                    str(user_id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Not able to update the user table')
                return False
        else:
            self.log.e(TAG, 'ID and role are not string')
            return False

    def update_user_team(self, user_id, team_id):
        TAG = 'update_user_team'

        if isinstance(user_id, str) and isinstance(team_id, str):
            try:
                self.cursor.execute(
                    "UPDATE " +
                    C.USER_TABLE +
                    " SET " +
                    C.USER_TABLE_TEAM +
                    " = " +
                    str(team_id) +
                    " WHERE " +
                    C.USER_TABLE_DELETED +
                    " = False AND " +
                    C.USER_TABLE_ID +
                    " = " +
                    str(user_id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Either user is deleted or not present in\
                             the user table')
                return False
        else:
            self.log.e(TAG, 'ID and team are not string')
            return False

    def update_user_policy(self, user_id, policy_id):
        TAG = 'update_user_policy'
        if isinstance(user_id, str) and isinstance(policy_id, str):
            try:
                self.cursor.execute(
                    "UPDATE " +
                    C.USER_TABLE +
                    " SET " +
                    C.USER_TABLE_POLICY +
                    " = " +
                    str(policy_id) +
                    " WHERE " +
                    C.USER_TABLE_DELETED +
                    " = False AND " +
                    C.USER_TABLE_ID +
                    " = " +
                    str(user_id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Either user is deleted or not present in\
                             the user table')
                return False
        else:
            self.log.e(TAG, 'User_id and/or policy_id are not string')
            return False

    def delete_user_policy(self, user_id):
        TAG = 'delete_user_policy'
        if isinstance(user_id, str):
            try:
                self.cursor.execute("UPDATE " + C.USER_TABLE + " SET " +
                                    C.USER_TABLE_POLICY + " = NULL WHERE "
                                    + C.USER_TABLE_DELETED + " = False AND " +
                                    C.USER_TABLE_ID + " = " + str(user_id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Either user is deleted or not present in\
                             the user table')
                return False
        else:
            self.log.e(TAG, 'User_id is not string')
            return False

    def update_user_name(self, id, name):
        TAG = 'update_user_name'

        if isinstance(id, str) and isinstance(name, str):
            try:
                self.cursor.execute(
                    "UPDATE " +
                    C.USER_TABLE +
                    " SET " +
                    C.USER_TABLE_NAME +
                    " = '" +
                    str(name) +
                    "' WHERE " +
                    C.USER_TABLE_ID +
                    " = " +
                    str(id))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Not able to update the user table')
                return False
        else:
            self.log.e(TAG, 'ID and/or name are not string')
            return False

    def delete_user(self, user_id):
        TAG = 'delete_user'

        if isinstance(user_id, str):
            try:
                self.cursor.execute("UPDATE " + C.USER_TABLE + " SET " +
                                    C.USER_TABLE_DELETED + " = True  WHERE " +
                                    C.USER_TABLE_ID + " = " + user_id)
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:

                return True
            else:
                self.log.e(TAG, 'Not able to delete from User table')
                return False

    def get_users(self, filter_dict=None):
        TAG = 'get_users'
        order_by = 'users.name'
        total_count = 0

        if isinstance(filter_dict, dict) and 'company_id' in filter_dict:
            query_string = ''
            for key, value in filter_dict.iteritems():
                if str(key) == C.USER_TABLE_EMAIL or str(
                        key) == C.USER_TABLE_NAME:
                    query_string += 'users.' + \
                        str(key) + " = '" + str(value) + "' AND "
                else:
                    query_string += 'users.' + \
                        str(key) + " = " + str(value) + ","

            query_string = query_string[:-1]

            try:
                self.cursor.execute("""SELECT COUNT(DISTINCT users.id)
                            FROM users
                            INNER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            WHERE users.company_id={0} AND users.deleted=False;
                            """.format(filter_dict['company_id']))
                total_count = self.cursor.fetchone()[0]

                self.cursor.execute("""SELECT DISTINCT devices.udid, users.id,
                            users.email, devices.os, users.name, roles.name,
                            teams.name FROM users
                            INNER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            WHERE {0} users.deleted=False
                            ORDER BY {1};""".format(
                    query_string, order_by))
                print self.cursor.query
            except Exception as err:
                self.log.e(TAG, 'Exception 2: ' + repr(err))
                return None, total_count

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()

                final_list = []

                mapping_tuple = (
                    'user_device',
                    'user_id',
                    'user_email',
                    'user_device_os',
                    'user_name',
                    'user_role',
                    'user_team')

                for row in rows:
                    inner_dict = dict(zip(mapping_tuple, row))
                    final_list.append(inner_dict)

                return final_list, total_count
            else:
                self.log.e(
                    TAG,
                    'No user found over select operation on User table')
                return None, total_count
        else:
            self.log.e(TAG, 'Filter is not a dictionary')
            return None, total_count

    def get_users_with_pages(self, filter=None, page=None, count=None,
                             sort_by=None):
        TAG = 'get_users_with_pages'
        query_string = ''
        skip = 0
        limit = 0
        if sort_by is None:
            sort_by = C.USER_TABLE_NAME

        if count is None:
            count = 20

        if page == 0 or page is None:
            page = 1

        skip = int(page) * int(count) - int(count)
        limit = int(count)
        print skip
        print limit

        if isinstance(filter, dict):
            for key, value in filter.iteritems():
                query_string += " {0} = {1} AND ".format(key, adapt(value))

            query_string = query_string.rstrip('AND ')

            try:
                self.cursor.execute(
                    "SELECT *  FROM " +
                    C.USER_TABLE +
                    " WHERE " +
                    query_string +
                    " ORDER BY " +
                    str(sort_by) +
                    " LIMIT " +
                    str(limit) +
                    " OFFSET " +
                    str(skip))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.USER_TABLE_ID] = row[0]
                    return_dict[C.USER_TABLE_EMAIL] = row[1]
                    return_dict[C.USER_TABLE_NAME] = row[2]
                    return_dict[C.USER_TABLE_ROLE] = row[3]
                    return_dict[C.USER_TABLE_TEAM] = row[4]
                    return_dict[C.USER_TABLE_POLICY] = row[5]
                    return_dict[C.USER_TABLE_COMPANY] = row[6]
                    return_dict[C.USER_TABLE_DELETED] = row[7]
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(TAG, 'Not able to perform select operation on \
                                    User table')
                return None
        elif filter is None:
            try:
                self.cursor.execute(
                    "SELECT *  FROM " +
                    C.USER_TABLE +
                    " ORDER BY " +
                    str(sort_by) +
                    " LIMIT " +
                    str(limit) +
                    " OFFSET " +
                    str(skip))
            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = {}
                    return_dict[C.USER_TABLE_ID] = row[0]
                    return_dict[C.USER_TABLE_EMAIL] = row[1]
                    return_dict[C.USER_TABLE_NAME] = row[2]
                    return_dict[C.USER_TABLE_ROLE] = row[3]
                    return_dict[C.USER_TABLE_TEAM] = row[4]
                    return_dict[C.USER_TABLE_POLICY] = row[5]
                    return_dict[C.USER_TABLE_COMPANY] = row[6]
                    return_dict[C.USER_TABLE_DELETED] = row[7]
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(TAG, 'Not able to perform select operation on\
                                             User table')
                return None
        else:
            self.log.e(TAG, 'Filter is not of type dict')
            return None

    def get_users_count(self, company_id):
        TAG = 'get_users'
        try:
            self.cursor.execute(
                "SELECT COUNT(*)  FROM " +
                C.USER_TABLE +
                " WHERE " +
                C.USER_TABLE_COMPANY +
                "=" +
                str(company_id) +
                " AND " +
                C.USER_TABLE_DELETED +
                " = False;")
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

    def get_users_for_role(self, role_name, role_id, team_name=None,
                           team_id=None, offset=None, count=None, sort_by=None,
                           query=None, query_type=None, sort_order=None):

        TAG = 'get_users_for_role'

        if offset is None:
            offset = 0

        if count is None:
            count = 'ALL'

        if sort_order is None:
            sort_order = 'ASC'
        else:
            sort_order = sort_order.upper()

        total_count = 0

        base_query_total = """SELECT COUNT(DISTINCT users.id) FROM users
                        LEFT OUTER JOIN devices ON users.id = devices.user_id
                            INNER JOIN teams ON users.team_id = teams.id
                            WHERE users.role_id={0} AND users.deleted=False
                            AND teams.deleted = False
                            """

        base_query = """SELECT DISTINCT devices.udid, devices.os,
                        devices.deleted, users.id, users.name, teams.name
                        FROM users
                        LEFT OUTER JOIN devices ON users.id = devices.user_id
                            INNER JOIN teams ON users.team_id = teams.id
                            WHERE users.role_id={0} AND users.deleted=False
                            AND teams.deleted = False
                            """

        final_query_total = base_query_total.format(role_id)
        final_query = base_query.format(role_id)

        if query:
            print '\nprinting query in dbhelper ..\n', query

            if query_type == 'name':

                final_query_total += """ AND users.name ILIKE '%{0}%' """
                final_query_total = final_query_total.format(str(query))

                final_query += """ AND users.name ILIKE '%{0}%' """

                final_query = final_query.format(str(query))

            elif query_type == 'device':

                final_query_total += """ AND devices.udid::text LIKE '%{0}%'
                                         AND devices.deleted=False """
                final_query_total = final_query_total.format(str(query))

                final_query += """ AND devices.udid::text LIKE '%{0}%'
                                  AND devices.deleted = False """

                final_query = final_query.format(str(query))

            elif query_type == 'team':

                final_query_total += """ AND teams.name ILIKE '%{0}%' """

                final_query_total = final_query_total.format(str(query))

                final_query += """ AND teams.name ILIKE '%{0}%' """

                final_query = final_query.format(str(query))

        if team_id:
            print team_id

            final_query_total += """ AND users.team_id={0} """

            final_query_total = final_query_total.format(team_id)

            final_query += """ AND users.team_id={0} """
            final_query = final_query.format(team_id)

        if sort_by:
            print sort_by

            if sort_by == 'device_id':

                final_query_total = final_query_total

                final_query += """ ORDER BY devices.udid::text {0} OFFSET
                                    {1} LIMIT {2};"""

            elif sort_by == 'team':

                final_query_total = final_query_total

                final_query += """ ORDER BY teams.name {0} OFFSET {1}
                                     LIMIT {2}; """

            else:

                final_query_total = final_query_total

                final_query += """ ORDER BY users.name {0} OFFSET {1}
                                    LIMIT {2}; """

        final_query = final_query.format(sort_order, offset, count)
        print "\nhere is the final query ..\n", final_query

        try:
            self.cursor.execute(final_query_total)
            total_count = self.cursor.fetchone()[0]

            self.cursor.execute(final_query)

        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()

            final_list = []

            mapping_tuple = ('user_device', 'user_device_os', 'device_deleted',
                             'user_id', 'user_name', 'user_team')

            for row in rows:
                row = list(row)
                inner_dict = dict(zip(mapping_tuple, row))
                device_deleted = inner_dict.pop('device_deleted')
                if device_deleted:
                    inner_dict['user_device'] = None
                    inner_dict['user_device_os'] = None
                inner_dict['user_role'] = role_name
                final_list.append(inner_dict)

            return final_list, total_count

        else:
            self.log.e(TAG,
                       'Not able to perform select operation on User table')
            return None, total_count

    def get_users_for_team(
            self,
            team_name,
            team_id,
            role_name=None,
            role_id=None,
            offset=None,
            count=None,
            sort_by=None,
            query=None,
            query_type=None,
            sort_order=None):

        TAG = 'get_users_for_team'
        if offset is None:
            offset = 0
        if count is None:
            count = 'ALL'
        if sort_order is None:
            sort_order = 'ASC'
        else:
            sort_order = sort_order.upper()

        total_count = 0

        base_query_total = """SELECT COUNT(DISTINCT users.id) FROM users
                          LEFT OUTER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            WHERE users.team_id={0} AND users.deleted=False
                            AND roles.deleted = False
                            """

        base_query = """SELECT DISTINCT devices.udid, devices.os,
                         devices.deleted,
                         users.id, users.name, roles.name FROM users
                    LEFT OUTER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            WHERE users.team_id={0} AND users.deleted=False
                            AND roles.deleted = False
                            """

        final_query_total = base_query_total.format(team_id)
        final_query = base_query.format(team_id)

        if query:

            print '\nprinting query in users team dbhelper ..\n', query

            if query_type == 'name':

                final_query_total += """ AND users.name ILIKE '%{0}%' """
                final_query_total = final_query_total.format(str(query))

                final_query += """ AND users.name ILIKE '%{0}%' """

                final_query = final_query.format(str(query))

            elif query_type == 'device':

                final_query_total += """ AND devices.udid::text LIKE '%{0}%'
                                    AND devices.deleted=False """
                final_query_total = final_query_total.format(str(query))

                final_query += """ AND devices.udid::text LIKE '%{0}%'
                                    AND devices.deleted=False """

                final_query = final_query.format(str(query))

            elif query_type == 'role':

                final_query_total += """ AND roles.name ILIKE '%{0}%' """

                final_query_total = final_query_total.format(str(query))

                final_query += """ AND roles.name ILIKE '%{0}%' """
                final_query = final_query.format(str(query))

        if role_id:
            print role_id

            final_query_total += """ AND users.role_id={0} """

            final_query_total = final_query_total.format(role_id)

            final_query += """ AND users.role_id={0} """
            final_query = final_query.format(role_id)

        if sort_by:
            print sort_by

            if sort_by == 'device_id':

                final_query_total = final_query_total

                final_query += """ ORDER BY devices.udid::text {0} OFFSET
                                    {1} LIMIT {2};"""

            elif sort_by == 'role':

                final_query_total = final_query_total

                final_query += """ ORDER BY roles.name {0} OFFSET {1}
                                     LIMIT {2}; """

            else:

                final_query_total = final_query_total

                final_query += """ ORDER BY users.name {0} OFFSET {1}
                                    LIMIT {2}; """

        final_query = final_query.format(sort_order, offset, count)
        print "\nhere is the final query ..\n", final_query

        try:
            self.cursor.execute(final_query_total)
            total_count = self.cursor.fetchone()[0]

            self.cursor.execute(final_query)

        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()

            final_list = []

            mapping_tuple = ('user_device', 'user_device_os', 'device_deleted',
                             'user_id', 'user_name', 'user_role')

            for row in rows:
                row = list(row)
                inner_dict = dict(zip(mapping_tuple, row))

                device_deleted = inner_dict.pop('device_deleted')

                if device_deleted:
                    inner_dict['user_device'] = None
                    inner_dict['user_device_os'] = None

                final_list.append(inner_dict)

            return final_list, total_count

        else:
            self.log.e(
                TAG,
                'Not able to perform select operation on User table')
            return None, total_count

    def get_users_base_helper(
            self,
            company_id,
            final_query,
            final_query_total,
            offset=None,
            count=None,
            query=None,
            query_type=None,
            role_id=None,
            team_id=None,
            os_type=None,
            sort_by=None,
            sort_order=None,
            filter_key=None,
            filter_value=None):

        TAG = 'get_users_for_user'
        if offset is None:
            offset = 0
        if count is None:
            count = 'ALL'
        if sort_order is None:
            sort_order = 'ASC'
        else:
            sort_order = sort_order.upper()

        print "\n here is sort order \n", sort_order

        total_count = 0
        # Sort By dict  Will be used to match and apply sorting accordingly
        sort_by_dict = {'name': 'users', 'team': 'teams', 'role': 'roles'}

        if query:

            print '\nprinting query in dbhelper ..\n', query

            if query_type == 'name':

                final_query_total += """ AND users.name ILIKE '%{0}%' """
                final_query_total = final_query_total.format(str(query))

                final_query += """ AND users.name ILIKE '%{0}%' """

                final_query = final_query.format(str(query))

            elif query_type == 'device':

                final_query_total += """
  AND devices.udid::text LIKE '%{0}%' """

                final_query_total = final_query_total.format(str(query))

                final_query += """ AND devices.udid::text LIKE '%{0}%' """

                final_query = final_query.format(str(query))

            elif query_type == 'team':

                final_query_total += """ AND teams.name ILIKE '%{0}%' """

                final_query_total = final_query_total.format(str(query))

                final_query += """ AND teams.name ILIKE '%{0}%' """

                final_query = final_query.format(str(query))

            elif query_type == 'role':

                final_query_total += """ AND roles.name ILIKE '%{0}%' """

                final_query_total = final_query_total.format(str(query))

                final_query += """ AND roles.name ILIKE '%{0}%' """

                final_query = final_query.format(str(query))

        if team_id:
            print team_id

            final_query_total += """ AND users.team_id={0} """

            final_query_total = final_query_total.format(team_id)

            final_query += """ AND users.team_id={0} """
            final_query = final_query.format(team_id)

        if role_id:
            print role_id

            final_query_total += """ AND users.role_id={0} """

            final_query_total = final_query_total.format(role_id)

            final_query += """ AND users.role_id={0} """
            final_query = final_query.format(role_id)

        if os_type:
            print os_type

            final_query_total += """ AND devices.os = '{0}'
                                     AND devices.deleted=False """
            final_query_total = final_query_total.format(str(os_type))

            final_query += """ AND devices.os = '{0}'
                               AND devices.deleted=False """
            final_query = final_query.format(str(os_type))

        if sort_by:

            print sort_by

            if sort_by == 'device_id':

                final_query_total = final_query_total

                final_query += """ ORDER BY devices.udid::text {0} OFFSET
                                    {1} LIMIT {2};"""
                final_query = final_query.format(sort_order, offset, count)

            elif sort_by in sort_by_dict:

                final_query_total = final_query_total

                final_query += """ ORDER BY {0}.name {1} OFFSET {2} LIMIT
                                    {3};"""
                final_query = final_query.format(sort_by_dict[sort_by],
                                                 sort_order, offset, count)

            else:
                final_query_total = final_query_total

                final_query += """ ORDER BY users.name {0} OFFSET {1} LIMIT
                                    {2};"""

        final_query = final_query.format(sort_order, offset, count)
        print "\nhere is the final query ..\n", final_query

        try:
            self.cursor.execute(final_query_total)
            total_count = self.cursor.fetchone()[0]

            self.cursor.execute(final_query)

        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))

        if self.cursor.rowcount > 0:
            rows = self.cursor.fetchall()

            final_list = []

            mapping_tuple = (
                'user_device',
                'user_id',
                'user_email',
                'user_device_os',
                'user_name',
                'user_role',
                'user_team')

            for row in rows:
                row = list(row)
                inner_dict = dict(zip(mapping_tuple, row))
                final_list.append(inner_dict)

            return final_list, total_count

        else:
            self.log.e(
                TAG,
                'Not able to perform select operation on User table')
            return None, total_count

    def get_users_for_user(self, company_id, offset, count, query=None,
                           query_type=None, role_id=None, team_id=None,
                           os_type=None, sort_by=None, sort_order=None,
                           filter_key=None, filter_value=None):

        base_query_total = """SELECT COUNT(DISTINCT users.id) FROM users
                            LEFT OUTER JOIN devices ON
                            users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            WHERE users.company_id={0} AND users.deleted=False
                            AND roles.deleted=False AND teams.deleted=False"""

        base_query = """SELECT DISTINCT devices.udid, users.id,
                            users.email, devices.os, users.name, roles.name,
                            teams.name FROM users
                    LEFT OUTER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            WHERE users.company_id={0} AND users.deleted=False
                            AND roles.deleted=False AND teams.deleted=False"""

        final_query_total = base_query_total.format(company_id)
        final_query = base_query.format(company_id)

        final_list, total_count = self.get_users_base_helper(
            company_id=company_id, offset=offset, count=count,
            final_query=final_query, final_query_total=final_query_total,
            query=query, query_type=query_type, role_id=role_id,
            team_id=team_id, os_type=os_type, sort_by=sort_by,
            sort_order=sort_order, filter_key=filter_key,
            filter_value=filter_value)

        return final_list, total_count

    def get_users_for_user_status(
            self,
            company_id,
            offset,
            count,
            data,
            query=None,
            query_type=None,
            role_id=None,
            team_id=None,
            os_type=None,
            sort_by=None,
            sort_order=None,
            filter_key=None,
            filter_value=None):

        if data == 'enrolled':
            status = True
            device_join = "INNER JOIN"
        else:
            status = False
            device_join = "LEFT OUTER JOIN"

        base_query_total = """SELECT COUNT(DISTINCT users.id) FROM users
                            {2} devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            INNER JOIN enrollments ON
                            users.id = enrollments.user_id
                            WHERE users.company_id={0} AND users.deleted=False
                            AND enrollments.is_enrolled = {1}
                            AND roles.deleted=False AND teams.deleted=False"""

        base_query = """SELECT DISTINCT devices.udid, users.id,
                            users.email, devices.os, users.name, roles.name,
                            teams.name FROM users
                            {2} devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            INNER JOIN enrollments ON
                            users.id = enrollments.user_id
                            WHERE users.company_id={0} AND users.deleted=False
                            AND enrollments.is_enrolled = {1}
                            AND roles.deleted=False AND teams.deleted=False"""

        if status:
            base_query_total += """ AND devices.deleted=False"""
            base_query += """ AND devices.deleted=False"""

        final_query_total = base_query_total.format(company_id, status,
                                                    device_join)

        final_query = base_query.format(company_id, status, device_join)

        final_list, total_count = self.get_users_base_helper(
            company_id=company_id, offset=offset, count=count,
            final_query=final_query, final_query_total=final_query_total,
            query=query, query_type=query_type, role_id=role_id,
            team_id=team_id, os_type=os_type, sort_by=sort_by,
            sort_order=sort_order, filter_key=filter_key,
            filter_value=filter_value)

        return final_list, total_count

    def get_users_for_user_violation(
            self,
            company_id,
            offset,
            count,
            query=None,
            query_type=None,
            role_id=None,
            team_id=None,
            os_type=None,
            sort_by=None,
            sort_order=None,
            filter_key=None,
            filter_value=None):

        base_query_total = """SELECT COUNT(DISTINCT users.id) FROM users
                            INNER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            INNER JOIN violations ON
                            devices.id = violations.device_id
                            WHERE users.company_id={0} AND users.deleted=False
                            AND roles.deleted=False
                            AND teams.deleted=False
                            AND violations.deleted=False
                            """

        base_query = """SELECT DISTINCT devices.udid, users.id,
                            users.email, devices.os, users.name, roles.name,
                            teams.name FROM users
                            INNER JOIN devices ON users.id = devices.user_id
                            INNER JOIN roles ON users.role_id = roles.id
                            INNER JOIN teams ON users.team_id = teams.id
                            INNER JOIN violations
                            ON devices.id = violations.device_id
                            WHERE users.company_id={0} AND users.deleted=False
                            AND roles.deleted=False
                            AND teams.deleted=False
                            AND violations.deleted=False
                            """

        final_query_total = base_query_total.format(company_id)

        final_query = base_query.format(company_id)

        final_list, total_count = self.get_users_base_helper(
            company_id=company_id, offset=offset, count=count,
            final_query=final_query, final_query_total=final_query_total,
            query=query, query_type=query_type, role_id=role_id,
            team_id=team_id, os_type=os_type, sort_by=sort_by,
            sort_order=sort_order, filter_key=filter_key,
            filter_value=filter_value)

        return final_list, total_count


if __name__ == "__main__":
    user = UserDBHelper()
    print user.get_user_with_email('aman@codemymobile.com')
