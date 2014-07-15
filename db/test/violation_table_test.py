from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.login import *
from toppatch_db.constants import Constants as c
import time

#     VIOLATION_TABLE =''
#     VIOLATION_TABLE_ID =''
#     VIOLATION_TABLE_USER =''
#     VIOLATION_TABLE_TIMESTAMP =''

userID = ''
violationTableID = ''

################# Test cases for add_violation()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        violationDict = {
                    c.VIOLATION_TABLE_USER: userID,
                    c.VIOLATION_TABLE_TIMESTAMP: time.strftime("%c")
                    }
        id = violation1.add_violation(violationDict)
        assert id is not None
        print id
        

#userID is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        violationDict = {
                         c.VIOLATION_TABLE_USER: '',
                         c.VIOLATION_TABLE_TIMESTAMP: time.strftime("%c")
                    }
        id = violation1.add_violation(violationDict)
        self.assertEqual(None, id)
        
#userID is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        violationDict = {
                         c.VIOLATION_TABLE_USER: None,
                         c.VIOLATION_TABLE_TIMESTAMP: time.strftime("%c")
                         }
        id = violation1.add_violation(violationDict)
        self.assertEqual(None, id)
        
        
#TimeStamp is blank
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        violationDict = {
                    c.VIOLATION_TABLE_USER: userID,
                    c.VIOLATION_TABLE_TIMESTAMP: ''
                    }
        id = violation1.add_violation(violationDict)
        self.assertEqual(None, id)
        
        
#TimeStamp is NULL
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        violationDict = {
                    c.VIOLATION_TABLE_USER: userID,
                    c.VIOLATION_TABLE_TIMESTAMP: None
                    }
        id = violation1.add_violation(violationDict)
        self.assertEqual(None, id)
        
        
# TODO: Check again for wrong parameters of pluck()        
####### Test case for get_violations() ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        id = violation1.get_violations(violationTableID)
        assert id is not None
        
            
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        tableID = '38a9ab90-ad9'
        id = violation1.get_violations(tableID)
        self.assertEqual(None, id)

        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        tableID = [violationTableID]
        id = violation1.get_violations(tableID)
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        violation1 = ViolationDBHelper()
        tableID = None
        id = violation1.get_violations(tableID)
        self.assertEqual(None, id)            
        
        
if __name__ == '__main__':
    unittest.main()  