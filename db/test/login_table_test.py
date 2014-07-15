from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.login import *
from toppatch_db.constants import Constants as c

#     LOGIN_TABLE = ''
#     LOGIN_TABLE_ID = ''
#     LOGIN_TABLE_USERNAME = ''
#     LOGIN_TABLE_PASSWORD = ''
#     LOGIN_TABLE_COMPANY = ''

userName = ''
password = ''
loginTableID = ''
################# Test cases for add_login()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: userName,
                    c.LOGIN_TABLE_PASSWORD: password,
                    c.LOGIN_TABLE_COMPANY: '0'
                    }
        id = login1.add_login(loginDIct)
        assert id is not None
        print id
        

#userName is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: '',
                    c.LOGIN_TABLE_PASSWORD: password,
                    c.LOGIN_TABLE_COMPANY: '0'
                    }
        id = login1.add_login(loginDIct)
        self.assertEqual(None, id)
        
#userName is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: None,
                    c.LOGIN_TABLE_PASSWORD: password,
                    c.LOGIN_TABLE_COMPANY: '0'
                    }
        id = login1.add_login(loginDIct)
        self.assertEqual(None, id)
        
        
#userName already present
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: 'abc',
                    c.LOGIN_TABLE_PASSWORD: password,
                    c.LOGIN_TABLE_COMPANY: '0'
                    }
        id = login1.add_login(loginDIct)
        assert id is not None
        id1 = login1.add_login(loginDict)
        self.assertEqual(None, id1)
        
        
#password is Blank
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: userName,
                    c.LOGIN_TABLE_PASSWORD: '',
                    c.LOGIN_TABLE_COMPANY: '0'
                    }
        id = login1.add_login(loginDIct)
        self.assertEqual(None, id)
        
#password is None
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: userName,
                    c.LOGIN_TABLE_PASSWORD: None,
                    c.LOGIN_TABLE_COMPANY: '0'
                    }
        id = login1.add_login(loginDIct)
        self.assertEqual(None, id)
        
#Company is None
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: userName,
                    c.LOGIN_TABLE_PASSWORD: password,
                    c.LOGIN_TABLE_COMPANY: None
                    }
        id = login1.add_login(loginDIct)
        self.assertEqual(None, id)
        
#Company is Blank
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                    c.LOGIN_TABLE_USERNAME: userName,
                    c.LOGIN_TABLE_PASSWORD: password,
                    c.LOGIN_TABLE_COMPANY: ''
                    }
        id = login1.add_login(loginDIct)
        self.assertEqual(None, id)            


        
# TODO: Check again for wrong parameters of pluck()        
####### Test case for get_login(id) ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        id = login1.get_login(loginTableID)
        assert id is not None
        
        
        
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = '38a9ab90-ad9'
        id = login1.get_login(tableID)
        self.assertEqual(None, id)
        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = [loginTableID]
        id = login1.get_login(tableID)
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = None
        id = login1.get_login(tableID)
        self.assertEqual(None, id)            
        
        
################### Test Case for update_login() #######################################

##All OK
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {
                     c.LOGIN_TABLE_PASSWORD: password
                    }
        id = login1.update_user(loginTableID, loginDIct)
        self.assertEqual(True, id)
        
##TableID is wrong
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac9'
        loginDIct = {
                     c.LOGIN_TABLE_PASSWORD: 'atul'
                    }
        id = login1.update_user(tableID, loginDIct)
        self.assertEqual(False, id)
        
    
##TableID is Blank
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = ''
        loginDIct = {
                    c.LOGIN_TABLE_PASSWORD: 'atul'
                    }
        id = login1.update_user(tableID, loginDIct)
        self.assertEqual(False, id)
        
##TableID is None
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = None
        loginDIct = {
                     c.LOGIN_TABLE_PASSWORD: 'atul'
                    }
        id = login1.update_user(tableID, loginDIct)
        self.assertEqual(False, id)


##TableID is List
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = ['38a9ab90-ad9c-46a7-ac94-9f984a4d93af']
        loginDIct = {
                    c.LOGIN_TABLE_PASSWORD: 'atul'
                    }
        id = login1.update_user(tableID, loginDIct)
        self.assertEqual(False, id)
        
##updateDict is List
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = [{
                    c.LOGIN_TABLE_PASSWORD: 'atul'
                    }]
        id = login1.update_user(loginTableID, loginDIct)
        self.assertEqual(False, id)

##updateDict is Blank
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = {}
        id = login1.update_user(loginTableID, loginDIct)
        self.assertEqual(False, id)


##updateDict is NULL
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        loginDIct = None
        id = login1.update_user(loginTableID, loginDIct)
        self.assertEqual(False, id)
        
##Can't update userName
class MyTestCase30a(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        loginDIct = {
                        c.LOGIN_TABLE_USERNAME: userName
                    }
        id = login1.update_user(loginTableID, loginDIct)
        self.assertEqual(False, id)
        
##Can't update Company
class MyTestCase30b(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        loginDIct = {
                        c.LOGIN_TABLE_COMPANY: 'development'
                    }
        id = login1.update_user(loginTableID, loginDIct)
        self.assertEqual(False, id)


############## Test cases for delete_user() ################################

# All OK
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        id = login1.delete_user(loginTableID)
        self.assertEqual(True, id)


# Incorrect tableID        
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = '38a9ab90-ad9c-46a7-a'
        id = login1.delete_user(tableID)
        self.assertEqual(False, id)
        
    
# Blank tableID        
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = ''
        id = login1.delete_user(tableID)
        self.assertEqual(False, id)
        
        
# NULL tableID        
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = None
        id = login1.delete_user(tableID)
        self.assertEqual(False, id)
        
#  tableID is list        
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        login1 = LoginDBHelper()
        tableID = [loginTableID]
        id = login1.delete_user(tableID)
        self.assertEqual(False, id)
        
        
# ################### Test cases for get_logins() ##############################
# 
# #All OK
# class MyTestCase36(AsyncTestCase):
#     def test_http_fetch(self):
#         login1 = LoginDBHelper()
#         filterDict = {
#                       c.LOGIN_TABLE_USERNAME: 'atuldhawan90@gmail.com',
#                       c.LOGIN_TABLE_COMPANY: 'development',
#                       c.USER_TABLE_ROLE: 'developer'
#                      }
#         id = login1.get_logins(filterDict)
#         print id
# 
# #Wrong details in the filter        
# class MyTestCase37(AsyncTestCase):
#     def test_http_fetch(self):
#         login1 = LoginDBHelper()
#         filterDict = {
#                       c.LOGIN_TABLE_USERNAME: 'fgdeagdghadefdegvdadea@gmail.com',
#                       c.LOGIN_TABLE_COMPANY: 'fsdzvvsgs',
#                       c.USER_TABLE_ROLE: 'develgagaeeagtertvddoper'
#                      }
#         id = login1.get_logins(filterDict)
#         self.assertEqual(False, id)
# 
# 
# #filter is a list        
# class MyTestCase38(AsyncTestCase):
#     def test_http_fetch(self):
#         login1 = LoginDBHelper()
#         filterDict = [{
#                       c.LOGIN_TABLE_USERNAME: 'atuldhawan90@gmail.com',
#                       c.LOGIN_TABLE_COMPANY: 'development',
#                       c.USER_TABLE_ROLE: 'developer'
#                      }]
#         id = login1.get_logins(filterDict)
#         self.assertEqual(False, id)
#         
# #filter is a empty        
# class MyTestCase39(AsyncTestCase):
#     def test_http_fetch(self):
#         login1 = LoginDBHelper()
#         filterDict = {}
#         id = login1.get_logins(filterDict)
#         self.assertEqual(False, id)
#  
# #filter is a NULL         
# class MyTestCase40(AsyncTestCase):
#     def test_http_fetch(self):
#         login1 = LoginDBHelper()
#         filterDict = None
#         id = login1.get_logins(filterDict)
#         self.assertEqual(False, id)
        
        
if __name__ == '__main__':
    unittest.main()  