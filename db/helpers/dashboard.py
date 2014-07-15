import psycopg2
from base import *
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.constants import Constants as C


class DashboardDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('DashboardDBHelper')

    def get_devices(self, company_id):
        TAG = 'get_devices'

        result_dict ={}
        os_list = ['ios', 'samsung']
        
        for device_os in os_list:

            try:
                self.cursor.execute("""SELECT COUNT(*) FROM  devices
                    INNER JOIN users ON devices.user_id=users.id
                    WHERE devices.os='{0}' AND users.company_id={1} 
                    AND users.deleted=False AND devices.deleted=False
                    ;""".format(device_os,
                    company_id))

                if self.cursor.rowcount > 0:
                    row = self.cursor.fetchone()
                    os_count = row[0]
                    result_dict[device_os] = os_count

                else:
                    return None

            except Exception, err:
                self.log.e(TAG, repr(err))
                return None

        return result_dict


if __name__ == "__main__":
    helper = DashboardDBHelper()
    print helper.get_devices()