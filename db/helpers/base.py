import psycopg2
from logger import Logger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config


class DBHelper:

    def __init__(self):
        TAG = '__init__'
        self.log = Logger('DBHelper')
        try:

            self.conn = psycopg2.connect(
                "dbname='" + config.DB_NAME + "' user='" + config.DB_USER +
                "'host='" + config.DB_HOST + "' password='" +
                config.DB_PASSWORD + "'")
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()
        except:
            self.log.e(TAG, 'Unable to connect to database')
