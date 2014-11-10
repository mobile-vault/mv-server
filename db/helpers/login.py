# import psycopg2
from .base import *
from logger import Logger
from psycopg2.extensions import adapt
from db.constants import Constants as C


class LoginDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('LoginDBHelper')

    def is_user_valid(self, user_id):
        if isinstance(user_id, str):
            TAG = "is_user_valid"
            try:
                self.cursor.execute(""" SELECT id FROM admin_profile
                                WHERE {0}={1} AND deleted=False
                                ;""".format(C.LOGIN_TABLE_ID, user_id))
            except Exception as err:
                self.log.e(TAG, repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.i(TAG, "user_id = {0} is not of type str".format(
                user_id))
            return False

    def set_login(self, login_id, company_id):
        TAG = 'set_login'

        try:
            self.cursor.execute('''UPDATE companies set deleted=False
                                WHERE id={0};'''.format(company_id))

            self.cursor.execute('''UPDATE admin_profile set deleted=False
                             WHERE id={0} AND company_id={1};'''.format(
                                login_id, company_id))
        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            return True
        else:
            self.log.e(TAG,
                       'Not able to perform update operation on Login table')
            return None

    def add_admin(self, admin_dict):
        TAG = 'add_admin'
        print 'IN add_admin'
        adm = admin_dict
        duplicate = False

        if isinstance(admin_dict, dict):
            try:
                self.cursor.execute("""SELECT id, deleted from admin_profile
                               where email={0};""".format(
                                    adapt(adm.get('email'))))

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    admin_id = row[0]
                    deleted = row[1]

                    if deleted:
                        return admin_id, duplicate
                    else:
                        duplicate = True
                        return admin_id, duplicate

                else:
                    self.cursor.execute("""INSERT INTO admin_profile (name,
                            email, login_id, company_id) VALUES ({0}, {1},
                                {2}, {3}) RETURNING id;""".format(
                        adapt(adm.get('name')),
                        adapt(adm.get('email')),
                        adapt(adm.get('login_id')),
                        adapt(adm.get('company_id'))))

                    if self.cursor.rowcount > 0:
                        row = self.cursor.fetchone()
                        return row[0], duplicate
                    else:
                        return None, duplicate

            except Exception as err:
                self.log.e(TAG, repr(err))
                return None, duplicate
        else:
            self.log.e(TAG, "parameter are not of type dict")
            return None, duplicate

    def get_login(self, username, update_flag=None):
        TAG = 'get_login'

        try:
            self.cursor.execute("""SELECT U.id, U.email, U.company_id,
                                P.password, P.id FROM admin_profile as U
                                INNER JOIN logins as P ON U.login_id=P.id
                                WHERE U.email={0} AND U.deleted=False
                                ;""".format(adapt(username)))
        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return_dict = {}
            return_dict[C.LOGIN_TABLE_ID] = row[0]
            return_dict[C.LOGIN_TABLE_USERNAME] = row[1]
            return_dict[C.LOGIN_TABLE_COMPANY] = row[2]
            return_dict['password'] = row[3]  # Explicitly defined name here

            if update_flag:
                return_dict[C.LOGIN_TABLE_PASSWORD] = row[4]
            return return_dict
        else:
            self.log.e(TAG, 'Not able to perform select operation on \
Login table')
            return None

    def get_login_name(self, id):
        TAG = 'get_login'

        try:
            self.cursor.execute(
                "SELECT " + C.LOGIN_TABLE_USERNAME + " FROM " + C.LOGIN_TABLE
                + " WHERE " + C.LOGIN_TABLE_ID + " = " + str(id))

        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return None

        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            self.log.e(TAG,
                       'Not able to perform select operation on Login table')
            return None

    def update_login_password(self, login_id, password):
        TAG = 'update_login_password'

        try:
            self.cursor.execute("""UPDATE logins set password={0}
                                WHERE id={1};""".format(adapt(password),
                                                        adapt(login_id)))

        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return False
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def set_login_password(self, password):
        TAG = 'set_login_password'

        try:
            self.cursor.execute("""INSERT INTO logins (password, deleted)
                                VALUES({0}, FALSE) RETURNING id;""".format(
                                adapt(password)))

        except Exception as err:
            self.log.e(TAG, 'Exception: ' + repr(err))
            return False
        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            return False


if __name__ == "__main__":
    login = LoginDBHelper()
    print login.get_login('1')
    print login.is_company_valid('1')
