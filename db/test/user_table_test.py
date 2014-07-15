from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.user import *
from toppatch_db.constants import Constants as c
import time

#    USER_TABLE= 'users'
#     USER_TABLE_ID= 'id'
#     USER_TABLE_EMAIL= 'email'
#     USER_TABLE_NAME = 'name'
#     USER_TABLE_TEAM = 'team'
#     USER_TABLE_ROLE = 'role'
#     USER_TABLE_POLICY = 'policy'
#     USER_TABLE_COMPANY = 'company'
#     USER_TABLE_LAST_COMMAND = 'last_command'
#     USER_TABLE_LAST_COMMAND_SENT_ON = 'last_command_on'

################# Test cases for add_user()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        

#Email is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: '',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
#Email is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: None,
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
        
#Email is invalid
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: "rk12aaaaaaaaa@gmail.com",
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
        
#username is Blank
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: '',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
#username is None
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: None,
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
#Company is None
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: None,
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
#Company is Blank
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: '',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        self.assertEqual(None, id)            


#Team is blank is blank        
class MyTestCase9(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: '',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        
#Team is NULL        
class MyTestCase10(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: None,
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        
#Role is blank is blank        
class MyTestCase11(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: '',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        
#Role is NULL        
class MyTestCase12(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: None,
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        

#Policy  is blank        
class MyTestCase13(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        
#Policy is NULL        
class MyTestCase14(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: None,
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        
        
        
#Last Command  is blank        
class MyTestCase15(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: '',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        
#Last Command  is NULL        
class MyTestCase16(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: None,
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        

#Duplicate Entries        
class MyTestCase17(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = {
                    c.USER_TABLE_EMAIL: 'aman12@gmail.com',
                    c.USER_TABLE_NAME: 'aman',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: None,
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.add_user(userDict)
        assert id is not None
        print id
        userDict1 = {
                    c.USER_TABLE_EMAIL: 'aman12@gmail.com',
                    c.USER_TABLE_NAME: 'aman',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: None,
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id1 = user1.add_user(userDict)
        self.assertEqual(None, id1)
        
        
#Dictionary not sent        
class MyTestCase18(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        userDict = [{
                    c.USER_TABLE_EMAIL: 'aman12@gmail.com',
                    c.USER_TABLE_NAME: 'aman',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }]
        id = user1.add_user(userDict)
        self.assertEqual(None, id)
        
# TODO: Check again for wrong parameters of pluck()        
####### Test case for get_user() ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = user1.get_user(tableID,[c.USER_TABLE_ROLE])
        assert id is not None
#         print id[c.USER_TABLE_ROLE]
        
#List not sent       
class MyTestCase20(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = user1.get_user(tableID,c.USER_TABLE_ROLE)
        self.assertEqual(None, id)  
        
        
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9'
        id = user1.get_user(tableID,[c.USER_TABLE_ROLE])
        self.assertEqual(None, id)
        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = ['38a9ab90-ad9c-46a7-ac94-9f984a4d93af']
        id = user1.get_user(tableID,[c.USER_TABLE_ROLE])
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = None
        id = user1.get_user(tableID,[c.USER_TABLE_ROLE])
        self.assertEqual(None, id)
        
        
# Pluck is None       
class MyTestCase22a(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = user1.get_user(tableID,None)
        self.assertEqual(None, id)
        
# Pluck is Empty       
class MyTestCase22b(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = user1.get_user(tableID,'')
        self.assertEqual(None, id)
        
# Pluck is non dict       
class MyTestCase22c(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = user1.get_user(tableID,{c.USER_TABLE_ROLE})
        self.assertEqual(None, id)             
        
        
################### Test Case for update_user() #######################################

##All OK
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        userDict = {
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm1234',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.update_user(tableID, userDict)
        self.assertEqual(True, id)
        
##TableID is wrong
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac9'
        userDict = {
                    
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm1234',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)
        
    
##TableID is Blank
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = ''
        userDict = {
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm1234',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)
        
##TableID is None
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = None
        userDict = {
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm1234',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)


##TableID is List
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = ['38a9ab90-ad9c-46a7-ac94-9f984a4d93af']
        userDict = {
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm1234',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)
        
##updateDict is List
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        userDict = [{
                    c.USER_TABLE_NAME: 'atul',
                    c.USER_TABLE_TEAM: 'development',
                    c.USER_TABLE_ROLE: 'developer',
                    c.USER_TABLE_POLICY: '0',
                    c.USER_TABLE_COMPANY: 'cmm1234',
                    c.USER_TABLE_LAST_COMMAND: 'CameraON',
                    c.USER_TABLE_LAST_COMMAND_SENT_ON: time.strftime("%c")
                    }]
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)

##updateDict is Blank
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        userDict = {}
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)


##updateDict is NULL
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        userDict = None
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)
        
##Can't update email
class MyTestCase30a(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        userDict = {
                    c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com'
                    }
        id = user1.update_user(tableID, userDict)
        self.assertEqual(False, id)


############## Test cases for delete_user() ################################

# All OK
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = user1.delete_user(tableID)
        self.assertEqual(True, id)


# Incorrect tableID        
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = '38a9ab90-ad9c-46a7-a'
        id = user1.delete_user(tableID)
        self.assertEqual(False, id)
        
    
# Blank tableID        
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = ''
        id = user1.delete_user(tableID)
        self.assertEqual(False, id)
        
        
# NULL tableID        
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = None
        id = user1.delete_user(tableID)
        self.assertEqual(False, id)
        
#  tableID is list        
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        tableID = ['38a9ab90-ad9c-46a7-ac94-9f984a4d93af']
        id = user1.delete_user(tableID)
        self.assertEqual(False, id)
        
        
################### Test cases for get_users() ##############################

#All OK
class MyTestCase36(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        filterDict = {
                      c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                      c.USER_TABLE_TEAM: 'development',
                      c.USER_TABLE_ROLE: 'developer'
                     }
        id = user1.get_users(filterDict)
        assert id is not None
        print id

#Wrong details in the filter        
class MyTestCase37(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        filterDict = {
                      c.USER_TABLE_EMAIL: 'fgdeagdghadefdegvdadea@gmail.com',
                      c.USER_TABLE_TEAM: 'fsdzvvsgs',
                      c.USER_TABLE_ROLE: 'develgagaeeagtertvddoper'
                     }
        id = user1.get_users(filterDict)
        self.assertEqual(None, id)


#filter is a list        
class MyTestCase38(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        filterDict = [{
                      c.USER_TABLE_EMAIL: 'atuldhawan90@gmail.com',
                      c.USER_TABLE_TEAM: 'development',
                      c.USER_TABLE_ROLE: 'developer'
                     }]
        id = user1.get_users(filterDict)
        self.assertEqual(None, id)
        
#filter is a empty        
class MyTestCase39(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        filterDict = {}
        id = user1.get_users(filterDict)
        self.assertEqual(None, id)
 
#filter is a NULL         
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        user1 = UserDBHelper()
        filterDict = None
        id = user1.get_users(filterDict)
        self.assertEqual(None, id)
        
        
if __name__ == '__main__':
    unittest.main()  