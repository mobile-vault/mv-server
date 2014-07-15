import datetime
import json

import psycopg2
from base import DBHelper
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, adapt
from db.constants import Constants as C


class RoleDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('RoleDBHelper')

    def is_role_valid(self, role_id):
        TAG= 'is_role_valid'
        if isinstance(role_id, str):
            try:
                self.cursor.execute("SELECT * FROM " + C.ROLE_TABLE +\
                         " WHERE " + C.ROLE_TABLE_ID + " = " + role_id\
                         +" AND " + C.ROLE_TABLE_DELETED + " = False;")
            except Exception,err:
                self.log.e(TAG,'Exception : ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:

            self.log.e(TAG,'Type of id is not string')
            return False

    #TODO: Compound keys can be used to make it faster while checking if
    # role already exists in table
    def add_role(self, role_dict):
        TAG = 'add_role'

        if type(role_dict) == dict:
            if role_dict.has_key(C.ROLE_TABLE_NAME) and role_dict.has_key(
                            C.ROLE_TABLE_COMPANY):
                try:
                    self.cursor.execute("SELECT * FROM " + C.ROLE_TABLE +\
                         " WHERE " + C.ROLE_TABLE_NAME + " = '" + \
                         str(role_dict[C.ROLE_TABLE_NAME]) + "'" + \
                         " AND roles.company_id={0};".format(role_dict.get(
                            'company_id')))
                except Exception,err:
                    self.log.e(TAG,'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    self.cursor.execute("""UPDATE roles set deleted = False,
                                    policy_id=null
                                    WHERE id={0};""".format(row[0]))
                    self.log.i(TAG, str(role_dict[C.ROLE_TABLE_NAME]) + " exist previously sending the id of that role")

                    return row[0]
                elif self.cursor.rowcount == 0:
                    try:
                        self.cursor.execute("""INSERT INTO {0} ({1}, {2}, {3})
                            VALUES (%s, %s, %s) RETURNING id;""".format(C.ROLE_TABLE,
                                C.ROLE_TABLE_NAME, C.ROLE_TABLE_COMPANY,
                                C.ROLE_TABLE_DELETED), (role_dict.get(C.ROLE_TABLE_NAME),
                                int(role_dict.get(C.ROLE_TABLE_COMPANY)), False))
                    except Exception,err:
                        self.log.e(TAG,'Exception : ' + repr(err))
                        return None

                    if self.cursor.rowcount > 0:
                        row = self.cursor.fetchone()
                        return row[0]
                    else:
                        self.log.e(TAG,'Not able to insert in Role table')
                        return None
                else:
                    self.log.e(TAG,'Not able to perform select query')
                    return None
        else:
            self.log.e(TAG,' Proper Dictionary not sent ')
            return None


    def get_role(self, role_id, company_id=None, pluck=None):
        TAG= 'get_role'

        if type(role_id) == str:
            if pluck is None:

                base_query = """SELECT * FROM roles WHERE
                     roles.deleted=False AND roles.id = {0}""".format(
                        role_id)

                if company_id:
                    base_query += " AND roles.company_id = {0};".format(
                                   company_id)

                try:
                    self.cursor.execute(base_query)

                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = {}
                    return_dict[C.ROLE_TABLE_ID] = row[0]
                    return_dict[C.ROLE_TABLE_NAME] = row[1]
                    return_dict[C.ROLE_TABLE_COMPANY] = row[2]
                    return_dict[C.ROLE_TABLE_POLICY] = row[3]
                    return_dict[C.ROLE_TABLE_CREATED_ON] = row[4]
                    return_dict[C.ROLE_TABLE_LAST_MODIFIED] = row[5]
                    return return_dict
                else:
                    self.log.e(TAG,'Not able to perform select operation on ROLE table')
                    return None

            elif type(pluck) == list:

                query_var = ', '.join([str(i) for i in pluck])

                base_query = """SELECT {0} FROM roles WHERE
                     roles.deleted=False AND roles.id = {1}""".format(
                        query_var, role_id)

                if company_id:
                    base_query += " AND roles.company_id = {0};".format(
                                   company_id)

                try:
                    self.cursor.execute(base_query)

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



    def update_role(self, role_id, company_id, role):
        TAG = 'update_role'

        if type(role_id) == str and type(role) == dict and company_id:
            query_str = ''
            for key, value in role.iteritems():
                if str(key) == C.ROLE_TABLE_NAME:
                    query_str += str(key) + " = '" + str(value) + "',"
                else:
                    query_str += str(key) + " = " + str(value) + ","

            query_str = query_str[:-1]

            try:
                self.cursor.execute("UPDATE " + C.ROLE_TABLE + " SET " + \
                    query_str + C.ROLE_TABLE_LAST_MODIFIED + " = {0}".format(
                        adapt(datetime.datetime.now())) + " WHERE " + \
                    C.ROLE_TABLE_ID + " = " + str(role_id) + \
                    " AND roles.company_id={0}".format(company_id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG,'ID is not string or Second parameter is not dictionary')
            return False


    def delete_role(self, role_id, company_id):
        TAG = 'delete_role'

        if isinstance(role_id, str):
            try:
                self.cursor.execute("UPDATE " + C.ROLE_TABLE + " SET " +\
                                C.ROLE_TABLE_DELETED + " = True WHERE "\
                                + C.ROLE_TABLE_ID + " = " + str(role_id)\
                                + " AND roles.company_id={0} ".format(
                                    company_id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                try:
                    self.cursor.execute("""UPDATE {0} SET {1} = NULL,
                                deleted=True WHERE {2}={3}
                                AND {4}={5};""".format(C.USER_TABLE,
                                 C.USER_TABLE_ROLE, C.USER_TABLE_ROLE,
                                 role_id, C.USER_TABLE_COMPANY, company_id))
                    return True
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return False
            else:
                self.log.i(TAG,'Role to be deleted is not in the role table')
                return False
        else:
            self.log.e(TAG,'ID is not string')
            return False



    def get_roles(self,company,pluck=None):
        TAG = 'get_roles'

        if type(company) == str:
            if pluck is None:
                try:
                    self.cursor.execute("SELECT * FROM " + C.ROLE_TABLE\
                                + " WHERE " + C.ROLE_TABLE_COMPANY + " = "\
                                 + str(company)+ " AND "+ C.ROLE_TABLE_DELETED\
                                + " = False ORDER BY "+ C.ROLE_TABLE_NAME\
                                +" ASC ;")
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        return_dict[C.ROLE_TABLE_ID] = row[0]
                        return_dict[C.ROLE_TABLE_NAME] = row[1]
                        return_dict[C.ROLE_TABLE_COMPANY] = row[2]
                        return_dict[C.ROLE_TABLE_POLICY] = row[3]
                        return_dict[C.ROLE_TABLE_CREATED_ON] = row[4]
                        return_dict[C.ROLE_TABLE_LAST_MODIFIED] = row[5]
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.e(TAG,'Not able to perform select operation on ROLE table')
                    return None
            elif type(pluck) == list:
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute("SELECT " + query_var + " FROM " \
                            + C.ROLE_TABLE + " WHERE " + C.ROLE_TABLE_COMPANY\
                            + " = " + str(company) + " AND " +\
                            C.ROLE_TABLE_DELETED + " = False ORDER BY " +\
                            C.ROLE_TABLE_NAME +" ASC ;")
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
            self.log.e(TAG,'company is not string')
            return None






    def add_role_if_not_exists(self,role):
        TAG = 'add_role_if_not_exists'

        if type(role) == dict:
            if role.has_key(C.ROLE_TABLE_NAME):
                try:
                    self.cursor.execute("SELECT * FROM " + C.ROLE_TABLE + " WHERE " + C.ROLE_TABLE_NAME + " = '" + str(role[C.ROLE_TABLE_NAME]) + "'")
                except Exception,err:
                    self.log.e(TAG,'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    self.log.i(TAG, str(role[C.ROLE_TABLE_NAME]) + " exist previously sending the id of that role")
                    row = self.cursor.fetchone()
                    return row[0]
                elif self.cursor.rowcount == 0:
                    key_str = ''
                    value_str = ''
                    for key, value in role.iteritems():
                        if str(key) == C.ROLE_TABLE_NAME:
                            value_str +=  "'" + str(value) + "',"
                        else:
                            value_str +=  str(value) + ","
                        key_str += str(key) + ","

#                         key_str = key_str[:-1]
#                         value_str = value_str[:-1]
                    try:
                        self.cursor.execute("INSERT INTO " + C.ROLE_TABLE + "(" + str(key_str) + C.ROLE_TABLE_CREATED_ON + "," + C.ROLE_TABLE_LAST_MODIFIED +  ") VALUES(" + str(value_str) + "'" + str(datetime.datetime.now())  + "'," +  "'" + str(datetime.datetime.now()) + "') RETURNING id")
                    except Exception,err:
                        self.log.e(TAG,'Exception : ' + repr(err))
                        return None

                    if self.cursor.rowcount > 0:
                        row = self.cursor.fetchone()
                        return row[0]
                    else:
                        self.log.e(TAG,'Not able to insert in Role table')
                        return None
                else:
                    self.log.e(TAG,'Not able to perform select query')
                    return None
        else:
            self.log.e(TAG,'Dictionary not sent ')
            return None



    def set_role_policy(self, role_id, policy_id):
        TAG = 'set_role_policy'
        if isinstance(role_id, str) and isinstance(policy_id, str):
            try:
                self.cursor.execute("UPDATE " + C.ROLE_TABLE + " SET " + \
                                C.ROLE_TABLE_POLICY + " = "+ str(policy_id) +\
                            " WHERE " + C.ROLE_TABLE_ID + " = " + str(role_id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Not able to update the role table')
                return False
        else:
            self.log.e(TAG, 'ID is not string')
            return False


    def get_role_by_name(self, name, company_id):
        TAG = 'get_role_id_by_name'
        if isinstance(name, str):
            try:
                self.cursor.execute("Select id from {0} where name='{1}'\
                        AND company_id={2} AND deleted=False;".format(
                                str(C.ROLE_TABLE), name, company_id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))

            if self.cursor.rowcount > 0:
                result_tuple = self.cursor.fetchone()
                return result_tuple[0]
            else:
                self.log.e(TAG, 'No row found with name in role table')
                return None
        else:
            self.log.e(TAG, 'name is not string')
            return None


if __name__ == '__main__':
    helper= RoleDBHelper()
    role_dict = {
                 C.ROLE_TABLE_NAME : 'Chotu',
                 C.ROLE_TABLE_POLICY: '6',
                 C.ROLE_TABLE_COMPANY : '1'
                 }

    print helper.delete_role_policy('7')
