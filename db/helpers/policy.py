import json
from datetime import datetime
# import psycopg2
from .base import *
from logger import Logger
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.constants import Constants as C


class PolicyDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('PolicyDBHelper')
        self.policy_tuple = (
            C.POLICY_TABLE_ID, C.POLICY_TABLE_NEW_ATTRIBUTES,
            C.POLICY_TABLE_OLD_ATTRIBUTES, C.POLICY_TABLE_CREATED_ON,
            C.POLICY_TABLE_MODIFIED_ON, C.POLICY_TABLE_DELETED)

    def is_policy_valid(self, policy_id):
        TAG = 'is_policy_valid'
        if isinstance(policy_id, str):
            try:
                self.cursor.execute(
                    "SELECT * FROM " + C.POLICY_TABLE + " WHERE " +
                    C.POLICY_TABLE_ID + " = " + policy_id)

            except Exception as err:
                self.log.e(TAG, 'Exception : ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG, 'Type of id is not string')
            return False

    def add_policy(self, policy):
        TAG = 'add_policy'

        if isinstance(policy, dict):
            if C.POLICY_TABLE_NEW_ATTRIBUTES in policy:
                try:
                    self.cursor.execute(
                        """INSERT INTO {0} ({1}) VALUES (%s)
                                        RETURNING id;""".format(
                            C.POLICY_TABLE, C.POLICY_TABLE_NEW_ATTRIBUTES), [
                            policy[
                                C.POLICY_TABLE_NEW_ATTRIBUTES], ])
                except Exception as err:
                    self.log.e(TAG, 'Exception : ' + repr(err))
                    return None

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    return row[0]
                else:
                    self.log.e(TAG, 'Not able to insert in Policy table')
                    return None
            else:
                self.log.e(TAG, 'Policy attributes not found in dictionary')
                return None

        else:
            self.log.e(TAG, 'Dictionary not sent for insertion')
            return None

    def get_policy(self, policy_id):
        TAG = 'get_policy'

        if isinstance(policy_id, str):
            try:
                self.cursor.execute(
                    "SELECT * FROM " + C.POLICY_TABLE + " WHERE " +
                    C.POLICY_TABLE_ID + " = " + policy_id)

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return None

            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                return_dict = {}
                return_dict = dict(zip(self.policy_tuple, row))
                return return_dict
            else:
                self.log.e(TAG, 'Not able to perform select operation \
on device table')
                return None
        else:
            self.log.e(TAG, 'ID is not string')
            return None

    def update_policy(self, policy_id, policy):
        TAG = 'update_policy'

        if isinstance(policy_id, str) and isinstance(policy, dict):
            try:
                query = self.cursor.mogrify("""UPDATE {0} SET {1}=(%s),
                            {2}=(%s), {3}=(%s) WHERE {4}=(%s)
                            RETURNING id;""".format(
                    C.POLICY_TABLE, C.POLICY_TABLE_NEW_ATTRIBUTES,
                    C.POLICY_TABLE_OLD_ATTRIBUTES, C.POLICY_TABLE_MODIFIED_ON,
                    C.POLICY_TABLE_ID),
                    [policy[C.POLICY_TABLE_NEW_ATTRIBUTES],
                        policy[C.POLICY_TABLE_OLD_ATTRIBUTES], datetime.now(),
                        policy_id])

                self.cursor.execute(query)

            except Exception as err:

                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        else:
            self.log.e(TAG, 'ID is not string or Second parameter is not \
                                                dictionary with attributes')
            return False

    # TODO : Implement if requirement arises...
    def delete_policy(self, policy_id):
        TAG = 'delete_policy'

        if isinstance(policy_id, str):
            try:
                self.cursor.execute(
                    "DELETE FROM " + C.POLICY_TABLE + " WHERE " +
                    C.POLICY_TABLE_ID + " = " + str(policy_id))

            except Exception as err:
                self.log.e(TAG, 'Exception: ' + repr(err))
                return False

            if self.cursor.rowcount > 0:
                return True
            else:
                self.log.i(TAG, 'policy not found for deleting')
                return False
        else:
            self.log.e(TAG, 'ID is not string')
            return False


if __name__ == '__main__':
    helper = PolicyDBHelper()
    print helper.get_policy('1')
    policy_json = json.dumps([{'policy': 'yahooooo'}])
    policy_dict = {
        C.POLICY_TABLE_NEW_ATTRIBUTES: policy_json
    }

#     print helper.add_policy(policy_dict)
    print helper.delete_policy('4')
    print helper.is_policy_valid('2')
    print helper.update_policy('2', policy_dict)
