'''
Company DB Helper With Postgress
'''

import psycopg2
from base import *
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, adapt
from db.constants import Constants as C


class CompanyDBHelper(DBHelper):
    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('CompanyDBHelper')

    def is_company_valid(self,company_id):
        TAG = 'is_company_valid'

        if isinstance(company_id, str):
            try:
                self.cursor.execute("""SELECT id FROM companies
                                WHERE {0}={1} AND deleted=False
                                ;""".format(C.COMPANY_TABLE_ID,
                                company_id))

            except Exception, err:
                self.log.e(TAG, repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True

            else:
                return False
        else:
            self.log.i(TAG, "company id = {0} is not of type str".format(
                                    company_id))
            return False

    def add_company(self, company_dict):
        TAG= 'add_company'
        print 'IN add_company'
        cm = company_dict
        duplicate = False

        if isinstance(company_dict, dict):
            try:
                self.cursor.execute("""SELECT id, deleted from companies where
                                   email={0};""".format(
                                    adapt(cm.get('email'))))

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    company_id = row[0]
                    deleted = row[1]

                    if deleted:
                        return company_id, duplicate
                    else:
                        duplicate = True
                        return company_id, duplicate

                else:
                    self.cursor.execute("""INSERT INTO companies (name, email,
                                  contact, address) VALUES ({0}, {1}, {2},
                                 {3}) RETURNING id;""".format(
                                 adapt(cm.get('name')),
                                  adapt(cm.get('email')),
                                adapt(cm.get('contact')),
                                  adapt(cm.get('address'))))

                    if self.cursor.rowcount > 0:
                        row = self.cursor.fetchone()
                        return row[0], duplicate
                    else:
                        return None, duplicate

            except Exception, err:
                self.log.e(TAG, repr(err))
                return None, duplicate
        else:
            self.log.e(TAG, "parameter are not of type dict")
            return None, duplicate


    def set_company_policy(self,company_id,policy_id):
        TAG = 'set_company_policy'

        try:
            self.cursor.execute("UPDATE "+ C.COMPANY_TABLE + " SET " + C.COMPANY_TABLE_POLICY + " = " + str(policy_id) + " WHERE " + C.COMPANY_TABLE_ID + " = " + str(company_id))
            if self.cursor.rowcount > 0:
                return True
            return False
        except Exception, err:
            self.log.e(TAG, repr(err))
            return False


    def get_company(self, company_id):
        TAG= 'get_company'
        print 'IN get_company'

        try:

            self.cursor.execute("SELECT id, name, policy_id, email FROM " \
                    + C.COMPANY_TABLE +\
                     " WHERE " + C.COMPANY_TABLE_ID + " = " + str(company_id))

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return_dict = {}
                return_dict[C.COMPANY_TABLE_ID] = row[0]
                return_dict[C.COMPANY_TABLE_NAME] = row[1]
                return_dict[C.COMPANY_TABLE_POLICY] = row[2]
                return_dict['email'] = row[3]
                return return_dict
            else:
                return None
        except Exception, err:
            self.log.e(TAG, repr(err))
            return None


if __name__ == "__main__":
    print CompanyDBHelper().set_company_policy('1', 3)
    print CompanyDBHelper().is_company_valid('1')
    print CompanyDBHelper().get_company('1')
    print CompanyDBHelper().set_company_policy('1', '1')
