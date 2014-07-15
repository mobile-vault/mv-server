import datetime
import time

import psycopg2
from base import *
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import adapt
from db.constants import Constants as C


class EnrollmentDBHelper(DBHelper):
    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('EnrollmentDBHelper')
        self.enroll_tuples = (C.ENROLLMENT_TABLE_ID, C.ENROLLMENT_TABLE_USER,
                        C.ENROLLMENT_TABLE_DEVICE, C.ENROLLMENT_TABLE_PASSWORD,
                                C.ENROLLMENT_TABLE_ENROLLED_ON,
                                C.ENROLLMENT_TABLE_SENT_ON,
                                C.ENROLLMENT_TABLE_IS_ENROLLED)
    def add_enrollment(self,enrollment):
        TAG= 'add_enrollment'

        if type(enrollment) == dict:
            if enrollment.has_key(C.ENROLLMENT_TABLE_USER):
                if enrollment.has_key(C.ENROLLMENT_TABLE_PASSWORD):
                        if enrollment.has_key(C.ENROLLMENT_TABLE_IS_ENROLLED):
                            try:
                                self.cursor.execute("SELECT * FROM " + \
                                    C.ENROLLMENT_TABLE + " WHERE " + \
                                    C.ENROLLMENT_TABLE_IS_ENROLLED+\
                                    " = False AND " + C.ENROLLMENT_TABLE_USER \
                                    + " = " + str(
                                    enrollment[C.ENROLLMENT_TABLE_USER]))
                            except Exception,err:
                                self.log.e(TAG,'Exception : ' + repr(err))
                                return None
                            if self.cursor.rowcount > 0:
                                self.log.i(TAG, str(
                                enrollment[C.ENROLLMENT_TABLE_USER]) +\
                                " exist already sending the id of that user")
                                row = self.cursor.fetchone()
                                return row[0]
                            else:
                                try:
                                    self.cursor.execute("INSERT INTO " + \
                                        C.ENROLLMENT_TABLE + "(" + \
                                        C.ENROLLMENT_TABLE_USER + "," + \
                                        C.ENROLLMENT_TABLE_PASSWORD + "," + \
                                        C.ENROLLMENT_TABLE_SENT_ON +\
                                        "," + C.ENROLLMENT_TABLE_IS_ENROLLED + \
                                        ") VALUES( %s,%s,%s,%s) RETURNING id",
                                    [enrollment[C.ENROLLMENT_TABLE_USER],
                                    enrollment[C.ENROLLMENT_TABLE_PASSWORD],
                                    datetime.datetime.now(),
                                    enrollment[C.ENROLLMENT_TABLE_IS_ENROLLED]])
                                except Exception,err:
                                    self.log.e(TAG,'Exception : ' + repr(err))
                                    return None

                                if self.cursor.rowcount > 0:
                                    row = self.cursor.fetchone()
                                    return row[0]
                                else:
                                    self.log.e(TAG,
                                    'Not able to insert in enrollment table')
                                    return None
                        else:
                            self.log.e(TAG,
                                    'IS_ENrolled field not found in dictionary')
                            return None
                else:
                    self.log.e(TAG, 'Password not found in dictionary')
                    return None
            else:
                self.log.e(TAG, 'User reference not found in dictionary')
                return None
        else:
            self.log.e(TAG, 'dictionary not sent for insertion')
            return None


    def get_enrollment(self,id,pluck=None):
        TAG = 'get_enrollment'

        if type(id) == str:
            if pluck is None:
                try:
                    self.cursor.execute("SELECT * FROM " + C.ENROLLMENT_TABLE +\
                                " WHERE " + C.ENROLLMENT_TABLE_ID + " = " + id)
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return_dict = dict(zip(self.enroll_tuples, row))
                    return return_dict
                else:
                    self.log.e(TAG,
                    'Not able to perform select operation on enrollment table')
                    return None
            elif type(pluck) == list:
                query_var = ''
                for item in pluck:
                    query_var = query_var + str(item) + ','

                query_var = query_var[:-1]

                try:
                    self.cursor.execute("SELECT " + query_var + " FROM " +
                                        C.ENROLLMENT_TABLE + " WHERE " + \
                                        C.ENROLLMENT_TABLE_ID + " = " + id)
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


    def set_enrolled(self,id):
        TAG= 'set_enrolled'

        if type(id) == str:
            try:
                self.cursor.execute("UPDATE " + C.ENROLLMENT_TABLE + " SET " +\
                                    C.ENROLLMENT_TABLE_ENROLLED_ON + " = '" +\
                                        str(datetime.datetime.now()) + "'," +\
                                        C.ENROLLMENT_TABLE_IS_ENROLLED + \
                                    " = True WHERE " + C.ENROLLMENT_TABLE_ID +\
                                                " = " + str(id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG,'Not able to update the enrollment table')
                return False
        else:
            self.log.e(TAG,'ID is not string ')
            return False


    def update_enrollment(self, id, update_dict):
        TAG = 'update_enrollment'
        if type(id) == str and type(update_dict) == dict:
            query_str = ''
            for key, value in update_dict.iteritems():
                query_str += str(key) + " = " + str(value) + ","

            query_str = query_str[:-1]

            try:
                self.cursor.execute("UPDATE " + C.ENROLLMENT_TABLE + " SET " +\
                                    query_str + " WHERE " + \
                                    C.ENROLLMENT_TABLE_ID + " = " + str(id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                    return True
            else:
                return False
        else:
            self.log.e(TAG,
                       'ID is not string or Second parameter is not dictionary')
            return False



    def delete_enrollment(self,id):
        TAG = 'delete_enrollment'

        if type(id) == str:
            try:
                self.cursor.execute("DELETE FROM " + C.ENROLLMENT_TABLE + \
                                    " WHERE " + C.ENROLLMENT_TABLE_ID + \
                                        " = " + str(id))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.e(TAG,'Not able to delete from the enrollment table')
                return False
        else:
            self.log.e(TAG,'ID type is not string')
            return False


    def get_enrollments(self, filter_dict=None, status=None):
        TAG= 'get_enrollments'
        if filter_dict is None:
            try:
                self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE )
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = dict(zip(self.enroll_tuples, row))
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
                return None
        elif type(filter_dict) == dict:

            query_string = ''
            for key, value in filter_dict.iteritems():
                query_string += " {0} = {1} AND ".format(key, adapt(value))

            query_string = query_string.rstrip('AND ')

            if status:
                try:
                    self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE + \
                                    " WHERE " + query_string+' AND '+\
                                    C.ENROLLMENT_TABLE_IS_ENROLLED+'='+ \
                                    str(status))
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

            else:
                try:
                    self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE+\
                                        " WHERE " + query_string)
                except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    return_dict = dict(zip(self.enroll_tuples, row))
                    return_array.append(return_dict)
                return return_array
            else:
                self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
                return None
        else:
            self.log.e(TAG,'filter_dict is not a dictionary')
            return None


    def get_enrollment_status_count(self, company_id, status):
        TAG= 'get_not_enrollment_count'

        try:
            self.cursor.execute("""SELECT COUNT(*)  FROM enrollments
                        INNER JOIN users ON enrollments.user_id = users.id
                        WHERE users.deleted = False AND users.company_id={0}
                        AND enrollments.is_enrolled={1};""".format(
                            company_id, status))
        except Exception, err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
            return None


    def get_enrolled(self, page= None, count = None):
        TAG= 'get_enrolled'
        # make a zip list without is_enrolled attribute
        zip_list = list(self.enroll_tuples).remove(
                                    C.ENROLLMENT_TABLE_IS_ENROLLED)
        if page is None or count is None:
            try:
                self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE + \
                        " WHERE " + C.ENROLLMENT_TABLE_IS_ENROLLED + " = True")
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    temp_dict = dict(zip(zip_list, row))

                    return_array.append(temp_dict)
                return return_array
            else:
                self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
                return None
        else:
            skip = 0
            limit = 0
            sort_by = C.ENROLLMENT_TABLE_ENROLLED_ON

            if count == None:
                count = 10

            if page == 0 or page is None:
                page = 1

            skip = page * count - count
            limit = count
            try:
                self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE + \
                                    " WHERE " + C.ENROLLMENT_TABLE_IS_ENROLLED\
                                    + " = True ORDER BY " + str(sort_by) + \
                                " LIMIT " + str(limit) + " OFFSET " + str(skip))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    temp_dict = dict(zip(zip_list, row))

                    return_array.append(temp_dict)
                return return_array
            else:
                self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
                return None


    def get_not_enrolled(self, page=None, count=None):
        TAG= 'get_not_enrolled'
        # make a zip list without is_enrolled attribute from enrolled_tuples
        zip_list = list(self.enroll_tuples).remove(
                                    C.ENROLLMENT_TABLE_IS_ENROLLED)
        if page is None or count is None:
            try:
                self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE + \
                                " WHERE " + C.ENROLLMENT_TABLE_IS_ENROLLED \
                                    + " = False" )
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                for row in rows:
                    temp_dict = dict(zip(zip_list, row))

                    return_array.append(temp_dict)
                return return_array
            else:
                self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
                return None
        else:
            skip = 0
            limit = 0
            sort_by = C.ENROLLMENT_TABLE_SENT_ON

            if count == None:
                count = 10

            if page == 0 or page is None:
                page = 1

            skip = page * count - count
            limit = count
            try:
                self.cursor.execute("SELECT *  FROM " + C.ENROLLMENT_TABLE +\
                                    " WHERE " + C.ENROLLMENT_TABLE_IS_ENROLLED \
                                    + " = False ORDER BY " + str(sort_by) + \
                                " LIMIT " + str(limit) + " OFFSET " + str(skip))
            except Exception, err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                rows = self.cursor.fetchall()
                return_array = []
                print rows
                for row in rows:
                    temp_dict = dict(zip(zip_list, row))

                    return_array.append(temp_dict)
                return return_array
            else:
                self.log.e(TAG,
                    'Not able to perform select operation on Enrollment table')
                return None


if __name__ == "__main__":
    email = "'ravi@codemymobile.com'"
    password ='6566'

    from db.helpers.user import UserDBHelper
    user = UserDBHelper()
    f= {C.USER_TABLE_EMAIL:email}
    print user.get_users(f)
#     enrollment = EnrollmentDBHelper()
#     filter_dict=dict()
#     filter_dict[C.ENROLLMENT_TABLE_USER]='5'
#     print enrollment.get_enrollments(filter_dict)
