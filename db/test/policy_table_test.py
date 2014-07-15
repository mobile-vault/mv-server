from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.policy import *
from toppatch_db.constants import Constants as c

#     POLICY_TABLE = ''
#     POLICY_TABLE_ID = ''
#     POLICY_TABLE_ATTRIBUTES = ''

tabID = 'any id field from Teams Table'

################# Test cases for add_policy()  ###################################

#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {
                    c.POLICY_TABLE_ATTRIBUTES: [
                                                {'request': 'createPolicy',
                                                'details': [ 
                                                            {'passcode' : {
                                                                           'simpleValue': True,
                                                                           'alphnumericValue': False,
                                                                           'maxLength': '6',
                                                                           'maxComplexCharacters': '2',
                                                                           'maxAge':'365',
                                                                           'autoLock': '2',
                                                                           'history': 'none',
                                                                           'gracePeriod': '1',
                                                                           'failedAttempts': '4'
                                                                           }
                                                             }
                                                            ]
                                                }
                                                ]
                    }
        id = policy1.add_policy(policyDict)
        assert id is not None
        print id
    
# Attributes are blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {
                      c.POLICY_TABLE_ATTRIBUTES: ['']
                     }
        id = policy1.add_policy(policyDict)
        self.assertEqual(None, id) 
        
        
# Attributes are NULL
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {
                      c.POLICY_TABLE_ATTRIBUTES: None
                     }
        id = policy1.add_policy(policyDict)
        self.assertEqual(None, id) 
        
# Dictionary is Blank
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {}
        id = policy1.add_policy(policyDict)
        self.assertEqual(None, id) 
        
# Dictionary is NULL
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = None
        id = policy1.add_policy(policyDict)
        self.assertEqual(None, id) 
        
        

        
################# Test cases for get_policy(id) ################################
 
# All OK
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        id = policy1.get_policy(tabID)
        assert id is not None

         
         
#Wrong tableID       
class MyTestCase10(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        tableID = '38a9ab90-ad9'
        id = policy1.get_policy(tableID)
        self.assertEqual(None, id)
         
# tableID is List       
class MyTestCase11(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        tableID = [tabID]
        id = policy1.get_policy(tableID)
        self.assertEqual(None, id)
        
# tableID is NULL       
class MyTestCase12(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        tableID = None
        id = policy1.get_policy(tableID)
        self.assertEqual(None, id)
        
# tableID is blank       
class MyTestCase12a(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        tableID = ''
        id = policy1.get_policy(tableID)
        self.assertEqual(None, id)
         
        


################# Test cases for update_policy(id,team) ################################ 

# All OK       
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {
                    c.POLICY_TABLE_ATTRIBUTES: [
                                                {'request': 'createPolicy',
                                                'details': [ 
                                                            {'passcode' : {
                                                                           'simpleValue': True,
                                                                           'alphnumericValue': False,
                                                                           'maxLength': '6',
                                                                           'maxComplexCharacters': '2',
                                                                           'maxAge':'365',
                                                                           'autoLock': '2',
                                                                           'history': 'none',
                                                                           'gracePeriod': '1',
                                                                           'failedAttempts': '4'
                                                                           }
                                                             }
                                                            ]
                                                }
                                                ]
                    }
        id = policy1.update_policy(tabID, policyDict)
        self.assertEqual(True, id)
         
# tableID is Empty       
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {
                    c.POLICY_TABLE_ATTRIBUTES: [
                                                {'request': 'createPolicy',
                                                'details': [ 
                                                            {'passcode' : {
                                                                           'simpleValue': True,
                                                                           'alphnumericValue': False,
                                                                           'maxLength': '6',
                                                                           'maxComplexCharacters': '2',
                                                                           'maxAge':'365',
                                                                           'autoLock': '2',
                                                                           'history': 'none',
                                                                           'gracePeriod': '1',
                                                                           'failedAttempts': '4'
                                                                           }
                                                             }
                                                            ]
                                                }
                                                ]
                    }
        id = policy1.update_policy('', policyDict)
        self.assertEqual(False, id)
        
# tableID is None       
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {
                      c.POLICY_TABLE_ATTRIBUTES: [
                                                {'request': 'createPolicy',
                                                'details': [ 
                                                            {'passcode' : {
                                                                           'simpleValue': True,
                                                                           'alphnumericValue': False,
                                                                           'maxLength': '6',
                                                                           'maxComplexCharacters': '2',
                                                                           'maxAge':'365',
                                                                           'autoLock': '2',
                                                                           'history': 'none',
                                                                           'gracePeriod': '1',
                                                                           'failedAttempts': '4'
                                                                           }
                                                             }
                                                            ]
                                                }
                                                ]
                    }
        id = policy1.update_policy(None, policyDict)
        self.assertEqual(False, id)
        
# policy is empty dict       
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = {}
        id = policy1.update_policy(tabID, policyDict)
        self.assertEqual(False, id)
        
# policy is not dict       
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = [
                      {
                       c.POLICY_TABLE_ATTRIBUTES: [
                                                   {'request': 'createPolicy',
                                                    'details': [ 
                                                                {'passcode' : {
                                                                               'simpleValue': True,
                                                                               'alphnumericValue': False,
                                                                               'maxLength': '6',
                                                                               'maxComplexCharacters': '2',
                                                                               'maxAge':'365',
                                                                               'autoLock': '2',
                                                                               'history': 'none',
                                                                               'gracePeriod': '1',
                                                                               'failedAttempts': '4'
                                                                               }
                                                                 }
                                                                ]
                                                    }
                                                   ]
                       }
                      ]
        id = policy1.update_policy(tabID, policyDict)
        self.assertEqual(False, id)
        
# policy  is NULL       
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        policy1 = PolicyDBHelper()
        policyDict = None
        id = policy1.update_policy(tabID, policyDict)
        self.assertEqual(False, id)
        
        
# ################# Test cases for delete_policy(id) ################################ 
# 
# # All OK       
# class MyTestCase32(AsyncTestCase):
#     def test_http_fetch(self):
#         policy1 = PolicyDBHelper()
#         id = policy1.delete_team(tabID)
#         self.assertEqual(True, id)
#         
# # tableID is blank       
# class MyTestCase33(AsyncTestCase):
#     def test_http_fetch(self):
#         policy1 = PolicyDBHelper()
#         id = policy1.delete_team('')
#         self.assertEqual(False, id)
#         
# # tableID is None       
# class MyTestCase34(AsyncTestCase):
#     def test_http_fetch(self):
#         policy1 = PolicyDBHelper()
#         id = policy1.delete_team(None)
#         self.assertEqual(False, id)
#         
# # tableID is not string       
# class MyTestCase35(AsyncTestCase):
#     def test_http_fetch(self):
#         policy1 = PolicyDBHelper()
#         id = policy1.delete_team([tabID])
#         self.assertEqual(False, id)
        


if __name__ == '__main__':
    unittest.main()  
        
         
  



