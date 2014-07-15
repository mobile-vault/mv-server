import json
from threading import Thread

from base import DBHelper
from logger import Logger
from db.constants import Constants as C
from psycopg2.extensions import adapt

class SamsungCommandsDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = Logger('SamsungCommandsDBHelper')

    def get_commands(self,uuid=None, executed=None, device_id=None,pluck=None,start=None,limit=None):
        '''
        Not implementing the start and limit. Why? Fuck you. that's why.
        '''
        TAG = 'get_commands'
        try:
            where_clause =''
            if uuid is not None:
                where_clause= C.SAMSUNG_COMMANDS_TABLE_UUID+" = '"+str(uuid)+"'"
            if executed is not None:
                if not where_clause:
                    where_clause = C.SAMSUNG_COMMANDS_TABLE_EXECUTED+' = '+str(executed)
                else:
                    where_clause = where_clause+' and '+C.SAMSUNG_COMMANDS_TABLE_EXECUTED+' = '+str(executed)
            if device_id is not None:
                if not where_clause:
                    where_clause = C.SAMSUNG_COMMANDS_TABLE_DEVICE+'='+str(device_id)
                else:
                    where_clause = where_clause+' and '+ C.SAMSUNG_COMMANDS_TABLE_DEVICE+'='+str(device_id)
        except Exception,err:
            self.log.e(TAG, repr(err))

        try:
            query_var = ''
            if pluck is not None:
                for item in pluck:
                    query_var = query_var + str(item) + ','
                query_var = query_var[:-1]
        except Exception,err:
            self.log.e(TAG, repr(err))

        try:
            if not query_var:
                if not where_clause:
                    self.cursor.execute("SELECT * FROM "+C.SAMSUNG_COMMANDS_TABLE)
                else:
                    self.cursor.execute("SELECT * FROM "+C.SAMSUNG_COMMANDS_TABLE+" where "+where_clause)
            else:
                if not where_clause:
                    self.cursor.execute("SELECT "+query_var+" FROM "+C.SAMSUNG_COMMANDS_TABLE)
                else:
                    self.cursor.execute("SELECT "+query_var+" FROM "+C.SAMSUNG_COMMANDS_TABLE+ " where "+where_clause)

            columns = [descs[0] for descs in self.cursor.description]
            if self.cursor.rowcount >0:
                rows = self.cursor.fetchall()
                return_arr = []
                for row in rows:
                    i=0
                    for column in columns:
                        cmd= dict()
                        cmd[column] = row[i]
                        i=i+1
                        return_arr.append(cmd)
                return return_arr
            else:
                return None

        except Exception,err:
            self.log.e(TAG, repr(err))
            return None

    def get_command(self,command_id,pluck=None):
        TAG ='get_command'
        if command_id is not None:
            print "SELECT * FROM "+C.SAMSUNG_COMMANDS_TABLE+" WHERE "+C.SAMSUNG_COMMANDS_TABLE_ID+"= "+str(command_id)
            self.cursor.execute("SELECT * FROM "+C.SAMSUNG_COMMANDS_TABLE+" WHERE "+C.SAMSUNG_COMMANDS_TABLE_ID+"= "+str(command_id))
            print self.cursor.rowcount
            if self.cursor.rowcount>0:
                columns = [descs[0] for descs in self.cursor.description]
                row=self.cursor.fetchone()
                i=0
                cmd= dict()
                for column in columns:
                    cmd[column] = row[i]
                    i=i+1
                return cmd
            else:
                return None
        else:
            self.log.i(TAG, 'command_id sent None')
            return None

    def add_command(self,command):
        TAG = 'add_command'
        if isinstance(command, dict):
            if command.get(C.SAMSUNG_COMMANDS_TABLE_ACTION) and \
               command.get(C.SAMSUNG_COMMANDS_TABLE_DEVICE) \
                and command.get(C.SAMSUNG_COMMANDS_TABLE_UUID):

                if not command[C.SAMSUNG_COMMANDS_TABLE_ATTRIBUTE]:
                    command[C.SAMSUNG_COMMANDS_TABLE_ATTRIBUTE]= "{}"

                self.cursor.execute(""" insert into samsung_commands
                                    (device_id, action,attribute,command_uuid)
                                    values( %s,%s,%s,%s) returning id""",
                                    [command[C.SAMSUNG_COMMANDS_TABLE_DEVICE],
                                    command[C.SAMSUNG_COMMANDS_TABLE_ACTION],
                            adapt(command[C.SAMSUNG_COMMANDS_TABLE_ATTRIBUTE]),
                            adapt(command[C.SAMSUNG_COMMANDS_TABLE_UUID])])

                if self.cursor.rowcount>0:
                    row = self.cursor.fetchone();
                    return row[0]
                else:
                    return None
        else:
            self.log.i(TAG, 'Not all required parameters sent in '+command.__repr__())
            return None
    #BIGNET299

    def update_result(self, uuid, device_id, result):
        TAG = 'update_result'

        if isinstance(uuid, str) and isinstance(device_id, str):
            try:
                self.cursor.execute("""UPDATE samsung_commands  SET {0} = {1},
                         {2}=now() WHERE {3}='{4}' AND {5}={6}
                        ;""".format(C.COMMAND_TABLE_RESULT,
                        adapt(json.dumps(result)), C.COMMAND_TABLE_EXECUTED_ON,
                        C.COMMAND_TABLE_COMMAND_UUID, str(uuid),
                        C.COMMAND_TABLE_DEVICE, device_id))
            except Exception, err:
                    self.log.e(TAG, 'Exception: ' + repr(err))
                    return False

            if self.cursor.rowcount > 0:
                    return True
            else:
                return False
        else:
            self.log.e(TAG, 'UUID, UDID and result are not string')
            return False

    def set_executed(self,command_id,result=None):
        TAG = 'set_executed'
        if command_id is not None:
            if not result:
                query = "UPDATE "+C.SAMSUNG_COMMANDS_TABLE+" SET "+C.SAMSUNG_COMMANDS_TABLE_EXECUTED+" = true "\
                +" WHERE "+C.SAMSUNG_COMMANDS_TABLE_ID+"="+str(command_id)
                print query
                self.cursor.execute(query)
            else:
                query = "UPDATE "+C.SAMSUNG_COMMANDS_TABLE+" SET "+C.SAMSUNG_COMMANDS_TABLE_EXECUTED+" = true , "+C.SAMSUNG_COMMANDS_TABLE_RESULT+"= '"+str(result)\
                +"' WHERE "+C.SAMSUNG_COMMANDS_TABLE_ID+"="+str(command_id)
                print query
                self.cursor.execute(query)
            if self.cursor.rowcount>0:
                return True
            else:
                return False
        else:
            self.log.i(TAG, 'command_id is none...')
            return False



if __name__ == '__main__':
    command = dict()
    command[C.SAMSUNG_COMMANDS_TABLE_ACTION]= 'action'
    command[C.SAMSUNG_COMMANDS_TABLE_DEVICE]= 1
    command[C.SAMSUNG_COMMANDS_TABLE_UUID]= '1234'
    command[C.SAMSUNG_COMMANDS_TABLE_EXECUTED]= False
    command[C.SAMSUNG_COMMANDS_TABLE_ATTRIBUTE]= '{}'
    helper = SamsungCommandsDBHelper()
    print helper.add_command(command)
