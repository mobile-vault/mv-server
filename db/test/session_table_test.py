from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.session import *
from toppatch_db.constants import Constants as c
import time


#     SESSION_TABLE = ''
#     SESSION_TABLE_ID = ''
#     SESSION_TABLE_USER = ''
#     SESSION_TABLE_CREATED_ON = ''
#     SESSION_TABLE_DESTROYED_ON = ''
#     SESSION_TABLE_IP = ''
#     SESSION_TABLE_INVALID = ''
#     SESSION_TABLE_USER_AGENT = ''


sessionTableID = ''

################################### Test cases for add_session()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'jnfj8ufjnfjn8uw44nnnjvui',
                       c.SESSION_TABLE_IP: '120.220.20.20',
                       c.SESSION_TABLE_INVALID: 'No',
                       c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                       }
        id = session1.add_session(sessionDict)
        assert id is not None
        print id
        

#UserTableID is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                    c.SESSION_TABLE_USER: '',
                    c.SESSION_TABLE_IP: '120.220.20.20',
                    c.SESSION_TABLE_INVALID: 'No',
                    c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                    c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                    }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
#UserTableID is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                    c.SESSION_TABLE_USER: None,
                    c.SESSION_TABLE_IP: '120.220.20.20',
                    c.SESSION_TABLE_INVALID: 'No',
                    c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                    c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                    }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
        
#UserTableID is invalid
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                    c.SESSION_TABLE_USER: "7634udy7uydhdhduy",
                    c.SESSION_TABLE_IP: '120.220.20.20',
                    c.SESSION_TABLE_INVALID: 'No',
                    c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                    c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                    }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
        
#IP is Blank
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                    c.SESSION_TABLE_USER: "7634udy7uydhdhduy",
                    c.SESSION_TABLE_IP: '',
                    c.SESSION_TABLE_INVALID: 'No',
                    c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                    c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                    }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
#IP is None
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                    c.SESSION_TABLE_USER: "7634udy7uydhdhduy",
                    c.SESSION_TABLE_IP: None,
                    c.SESSION_TABLE_INVALID: 'No',
                    c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                    c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                    }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
#Invalid Field is None
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'jnfj8ufjnfjn8uw44nnnjvui',
                       c.SESSION_TABLE_IP: '120.220.20.20',
                       c.SESSION_TABLE_INVALID: None,
                       c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                       }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
#Invalid Field is Blank
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'jnfj8ufjnfjn8uw44nnnjvui',
                       c.SESSION_TABLE_IP: '120.220.20.20',
                       c.SESSION_TABLE_INVALID: '',
                       c.SESSION_TABLE_USER_AGENT: 'Mozilla FireFox',
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                       }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
        
#UserAgent is None
class MyTestCase9(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'jnfj8ufjnfjn8uw44nnnjvui',
                       c.SESSION_TABLE_IP: '120.220.20.20',
                       c.SESSION_TABLE_INVALID: 'No',
                       c.SESSION_TABLE_USER_AGENT: None,
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                       }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)
        
#UserAgent is Blank
class MyTestCase10(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'jnfj8ufjnfjn8uw44nnnjvui',
                       c.SESSION_TABLE_IP: '120.220.20.20',
                       c.SESSION_TABLE_INVALID: 'No',
                       c.SESSION_TABLE_USER_AGENT: '',
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c")
                       }
        id = session1.add_session(sessionDict)
        self.assertEqual(None, id)              


               
####### Test case for get_session(id) ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        id = session1.get_session(sessionTableID)
        assert id is not None

        
        
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = '38a9ab90-ad9'
        id = session1.get_session(tableID)
        self.assertEqual(None, id)
        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = [sessionTableID]
        id = session1.get_session(tableID)
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = None
        id = session1.get_session(tableID)
        self.assertEqual(None, id)          
        
        
################### Test Case for update_session() #######################################

##All OK
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_INVALID: 'Yes',
                       c.SESSION_TABLE_DESTROYED_ON: time.strftime("%c")
                       }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(True, id)
        
##TableID is wrong
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac9'
        sessionDict = {
                       c.SESSION_TABLE_INVALID: 'Yes',
                       c.SESSION_TABLE_DESTROYED_ON: time.strftime("%c")
                       }
        id = session1.update_session(tableID, sessionDict)
        self.assertEqual(False, id)
        
    
##TableID is Blank
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = ''
        sessionDict = {
                       c.SESSION_TABLE_INVALID: 'Yes',
                       c.SESSION_TABLE_DESTROYED_ON: time.strftime("%c")
                       }
        id = session1.update_session(tableID, sessionDict)
        self.assertEqual(False, id)
        
##TableID is None
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = None
        sessionDict = {
                       c.SESSION_TABLE_INVALID: 'Yes',
                       c.SESSION_TABLE_DESTROYED_ON: time.strftime("%c")
                       }
        id = session1.update_session(tableID, sessionDict)
        self.assertEqual(False, id)


##TableID is List
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        tableID = [sessionTableID]
        sessionDict = {
                       c.SESSION_TABLE_INVALID: 'Yes',
                       c.SESSION_TABLE_DESTROYED_ON: time.strftime("%c")
                       }
        id = session1.update_session(tableID, sessionDict)
        self.assertEqual(False, id)
        
##updateDict is List
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = [{
                       c.SESSION_TABLE_INVALID: 'Yes',
                       c.SESSION_TABLE_DESTROYED_ON: time.strftime("%c")
                       }]
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)

##updateDict is Blank
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {}
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)


##updateDict is NULL
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = None
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
        
##Can't update USERID
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'abcxyz'
                      }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
        
##Can't update IP
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_IP: '120.220.20.21'
                      }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
        
##Can't update IP
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER_AGENT: 'Chrome'
                      }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
        
##Can't update CreatedON Time
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c") 
                      }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
        
        
##Can't update UserID, IP, UserAgent and CreatedON Time
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_USER: 'abcxyz',
                       c.SESSION_TABLE_IP: '120.220.20.21',
                       c.SESSION_TABLE_USER_AGENT: 'Chrome',
                       c.SESSION_TABLE_CREATED_ON: time.strftime("%c") 
                      }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
        
##Can't update CreatedON Time
class MyTestCase36(AsyncTestCase):
    def test_http_fetch(self):
        session1 = SessionDBHelper()
        sessionDict = {
                       c.SESSION_TABLE_ID: 'ghahhjiehfuba88ey6haih'
                      }
        id = session1.update_session(sessionTableID, sessionDict)
        self.assertEqual(False, id)
          
        
if __name__ == '__main__':
    unittest.main()  