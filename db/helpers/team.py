import datetime
import json

import psycopg2
from base import *
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, adapt
from db.constants import Constants as C


class TeamDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('TeamDBHelper')

    def is_team_valid(self,id):
        TAG = 'is_team_valid'
        if type(id):
            try:
                self.cursor.execute("SELECT * FROM " + C.TEAM_TABLE + " WHERE " + C.TEAM_TABLE_ID + " = " + id)
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

    def add_team(self,team):
        TAG = 'add_team'

        if type(team) == dict:
            if team.has_key(C.TEAM_TABLE_NAME) and team.has_key(
                    C.TEAM_TABLE_COMPANY):
                try:
                    self.cursor.execute("SELECT * FROM " + C.TEAM_TABLE + \
                                    " WHERE " + C.TEAM_TABLE_NAME + " = '" +\
                                    str(team[C.TEAM_TABLE_NAME]) + "' "+\
                                    " AND teams.company_id={0} ;".format(
                                        team.get('company_id')))
                except Exception,err:
                    self.log.e(TAG,'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    self.cursor.execute("""UPDATE teams set deleted = False,
                                    policy_id=null
                                    WHERE id={0};""".format(row[0]))
                    self.log.i(TAG, str(team[C.TEAM_TABLE_NAME]) +\
                         " exist previously sending the id of that team")

                    return row[0]
                elif self.cursor.rowcount == 0:
                    key_str = ''
                    value_str = ''
                    for key, value in team.iteritems():
                        if str(key) == C.TEAM_TABLE_NAME:
                            value_str +=  "'" + str(value) + "',"
                        else:
                            value_str +=  str(value) + ","
                        key_str += str(key) + ","

                        key_str = key_str[:-1]
                        value_str = value_str[:-1]
                    try:
                        self.cursor.execute("""INSERT INTO {0} ({1}, {2}, {3})
                                        VALUES (%s, %s, %s) RETURNING id;
                                    """.format(C.TEAM_TABLE, C.TEAM_TABLE_NAME,
                                 C.TEAM_TABLE_COMPANY, C.TEAM_TABLE_DELETED),
                                (team.get(C.TEAM_TABLE_NAME),
                                 int(team.get(C.TEAM_TABLE_COMPANY)),
                                team[C.TEAM_TABLE_DELETED]))

                    except Exception,err:
                        self.log.e(TAG,'Exception : ' + repr(err))
                        return None

                    if self.cursor.rowcount > 0:
                        row = self.cursor.fetchone()
                        return row[0]
                    else:
                        self.log.e(TAG,'Not able to insert in team table')
                        return None
                else:
                    self.log.e(TAG,'Not able to perform select query')
                    return None
        else:
            self.log.e(TAG,'Dictionary not sent ')
            return None


    def get_team(self, team_id, company_id=None, pluck=None):
        TAG = 'get_team'
        if isinstance(team_id, str):
            if pluck is None:

                base_query = """SELECT * FROM teams WHERE
                     teams.deleted=False AND teams.id = {0}""".format(
                        team_id)

                if company_id:
                    base_query += " AND teams.company_id = {0};".format(
                                   company_id)

                try:
                    self.cursor.execute(base_query)

                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = {}
                    return_dict[C.TEAM_TABLE_ID] = row[0]
                    return_dict[C.TEAM_TABLE_NAME] = row[1]
                    return_dict[C.TEAM_TABLE_COMPANY] = row[2]
                    return_dict[C.TEAM_TABLE_POLICY] = row[3]
                    return_dict[C.TEAM_TABLE_CREATED_ON] = row[4]
                    return_dict[C.TEAM_TABLE_LAST_MODIFIED] = row[5]
                    return return_dict
                else:
                    self.log.e(TAG,
                         'Not able to perform select operation on TEAM table')
                    return None

            elif isinstance(pluck, list):

                query_var = ', '.join([str(i) for i in pluck])

                base_query = """SELECT {0} FROM teams WHERE
                     teams.deleted=False AND teams.id = {1}""".format(
                        query_var, team_id)

                if company_id:
                    base_query += " AND teams.company_id = {0};".format(
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

    def set_team_policy(self, team_id, policy_id):
        TAG = 'set_team_policy'

        try:
            self.cursor.execute("UPDATE "+ C.TEAM_TABLE + " SET " +\
                             C.TEAM_TABLE_POLICY + " = " + str(policy_id) +\
                     " WHERE " + C.TEAM_TABLE_ID + " = " + str(team_id))
            if self.cursor.rowcount > 0:
                return True
            return False
        except Exception, err:
            self.log.e(TAG, repr(err))
            return False

    def update_team(self, team_id, company_id, team):
        TAG = 'update_team'

        if type(team_id) == str and type(team) == dict and company_id:
            query_str = ''
            for key, value in team.iteritems():
                if str(key) == C.TEAM_TABLE_NAME:
                    query_str += str(key) + " = '" + str(value) + "',"
                else:
                    query_str += str(key) + " = " + str(value) + ","

            query_str = query_str[:-1]

            try:
                self.cursor.execute("UPDATE " + C.TEAM_TABLE + " SET " + \
                    query_str + C.TEAM_TABLE_LAST_MODIFIED + " = {0}".format(
                    adapt(datetime.datetime.now())) + " WHERE " +\
                     C.TEAM_TABLE_ID + " = " + str(team_id) +\
                     " AND teams.company_id = {0}".format(company_id))

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


    def delete_team(self, team_id, company_id):
        TAG = 'delete_team'


        if isinstance(team_id, str) and company_id:
            try:
                self.cursor.execute("UPDATE " + C.TEAM_TABLE + " SET " \
                                + C.TEAM_TABLE_DELETED + " = True WHERE "\
                                + C.TEAM_TABLE_ID + " = " + str(team_id)\
                                + " AND teams.company_id={0}".format(
                                    company_id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                try:
                    self.cursor.execute("""UPDATE  {0} SET {1} = NULL,
                                    deleted=True WHERE
                                    {2} = {3} AND {4} = {5};""".format(
                                    C.USER_TABLE, C.USER_TABLE_TEAM,
                                    C.USER_TABLE_TEAM, team_id,
                                    C.USER_TABLE_COMPANY, company_id))
                    return True
                except Exception, err:
                    self.log.e(TAG, 'Exception: '+ repr(err))
                    return False
            else:
                self.log.i(TAG, 'Team to be deleted is not in the team table')
                return False
        else:
            self.log.e(TAG, 'ID is not string')
            return False



    def get_teams(self, company, pluck=None):
        TAG = 'get_teams'

        if type(company) == str:
            if pluck is None:
                try:
                    self.cursor.execute("SELECT * FROM " + C.TEAM_TABLE +\
                            " WHERE " + C.TEAM_TABLE_COMPANY + " = " + \
                            str(company) + " AND "+ C.ROLE_TABLE_DELETED\
                                + " = False ORDER BY "+ C.TEAM_TABLE_NAME\
                                +" ASC ;")
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    rows = self.cursor.fetchall()
                    return_array = []
                    for row in rows:
                        return_dict = {}
                        return_dict[C.TEAM_TABLE_ID] = row[0]
                        return_dict[C.TEAM_TABLE_NAME] = row[1]
                        return_dict[C.TEAM_TABLE_COMPANY] = row[2]
                        return_dict[C.TEAM_TABLE_POLICY] = row[3]
                        return_dict[C.TEAM_TABLE_CREATED_ON] = row[4]
                        return_dict[C.TEAM_TABLE_LAST_MODIFIED] = row[5]
                        return_array.append(return_dict)
                    return return_array
                else:
                    self.log.e(TAG,'Not able to perform select operation on Team table')
                    return None
            elif type(pluck) == list:
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute("SELECT " + query_var + " FROM " + \
                        C.TEAM_TABLE + " WHERE " + C.TEAM_TABLE_COMPANY\
                        + " = " + str(company)+ " AND "+ C.ROLE_TABLE_DELETED +\
                        " = False ORDER BY "+ C.ROLE_TABLE_NAME + " ASC;")
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



    def add_team_if_not_exists(self,team):
        TAG = 'add_team_if_not_exists'


        if type(team) == dict:
            if team.has_key(C.TEAM_TABLE_NAME):
                try:
                    self.cursor.execute("SELECT * FROM " + C.TEAM_TABLE + " WHERE " + C.TEAM_TABLE_NAME + " = '" + str(team[C.TEAM_TABLE_NAME]) + "'")
                except Exception,err:
                    self.log.e(TAG,'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    self.log.i(TAG, str(team[C.TEAM_TABLE_NAME]) + " exist previously sending the id of that team")
                    row = self.cursor.fetchone()
                    return row[0]
                elif self.cursor.rowcount == 0:
                    key_str = ''
                    value_str = ''
                    for key, value in team.iteritems():
                        if str(key) == C.TEAM_TABLE_NAME:
                            value_str +=  "'" + str(value) + "',"
                        else:
                            value_str +=  str(value) + ","
                        key_str += str(key) + ","

                        key_str = key_str[:-1]
                        value_str = value_str[:-1]
                    try:
                        self.cursor.execute("INSERT INTO " + C.TEAM_TABLE + "(" + str(key_str) + C.TEAM_TABLE_CREATED_ON + "," + C.TEAM_TABLE_LAST_MODIFIED +  ") VALUES(" + str(value_str) + "'" + str(datetime.datetime.now())  + "'," +  "'" + str(datetime.datetime.now()) + "') RETURNING id")
                    except Exception,err:
                        self.log.e(TAG,'Exception : ' + repr(err))
                        return None

                    if self.cursor.rowcount > 0:
                        row = self.cursor.fetchone()
                        return row[0]
                    else:
                        self.log.e(TAG,'Not able to insert in team table')
                        return None
                else:
                    self.log.e(TAG,'Not able to perform select query')
                    return None
        else:
            self.log.e(TAG,'Dictionary not sent ')
            return None



    def delete_team_policy(self,id):
        TAG = 'delete_team_policy'
        if type(id) == str:
            try:
                self.cursor.execute("UPDATE " + C.TEAM_TABLE + " SET " + C.TEAM_TABLE_POLICY + " = NULL WHERE " + C.TEAM_TABLE_ID + " = " + str(id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG, 'Not able to update the team table')
                return False
        else:
            self.log.e(TAG,'ID is not string')
            return False

    def get_team_by_name(self, name, company_id):
        TAG = 'get_team_id_by_name'
        if isinstance(name, str):
            try:
                self.cursor.execute("Select id from {0} where name='{1}'\
                        AND company_id={2} AND deleted=False;".format(
                        str(C.TEAM_TABLE), name, company_id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))

            if self.cursor.rowcount > 0:
                result_tuple = self.cursor.fetchone()
                return result_tuple[0]
            else:
                self.log.e(TAG, 'No row found with name in team table')
                return None
        else:
            self.log.e(TAG, 'name is not string')
            return None




if __name__ == "__main__":
    helper= TeamDBHelper()
    team_dict = {
                 C.TEAM_TABLE_NAME : 'Faltu',
                 C.TEAM_TABLE_POLICY: '6',
                 C.TEAM_TABLE_COMPANY : '1'
                 }
#     role_dict = {
#                  C.ROLE_TABLE_NAME: 'Developer'
#                  }
#
    print helper.add_team(team_dict)
    print helper.add_team_if_not_exists(team_dict)
    print helper.delete_team('6')
    print helper.get_team('4')
    print helper.get_team('4', [C.TEAM_TABLE_NAME, C.TEAM_TABLE_POLICY])
    print helper.get_teams('1')
    print helper.get_teams('1', [C.ROLE_TABLE_NAME, C.ROLE_TABLE_POLICY])
    print helper.is_team_valid('2')
    update_dict = {
                 C.TEAM_TABLE_NAME : 'Faltu',
                 C.TEAM_TABLE_POLICY: '2',
                 C.TEAM_TABLE_COMPANY : '1'
                 }
    print helper.update_team('7', update_dict)
