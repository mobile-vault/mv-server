from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.role import *
from toppatch_db.constants import Constants as c
import time

#     ROLE_TABLE = 'roles'
#     ROLE_TABLE_ID = 'id'
#     ROLE_TABLE_NAME = 'name'
#     ROLE_TABLE_POLICY = 'policy'
#     ROLE_TABLE_CREATED_ON = 'created_on'
#     ROLE_TABLE_LAST_MODIFIED = 'modified_on'
#     ROLE_TABLE_COMPANY = 'company'

tabID = 'ehrihri'

################# Test cases for add_role()  ###################################

#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: 'developer',
                    c.ROLE_TABLE_POLICY: '0',
                    c.ROLE_TABLE_COMPANY: '0',
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        assert id is not None
        print id
    
# Role name is blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: '',
                    c.ROLE_TABLE_POLICY: '0',
                    c.ROLE_TABLE_COMPANY: '0',
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        self.assertEqual(None, id) 
        
        
# Role name is NULL
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: None,
                    c.ROLE_TABLE_POLICY: '0',
                    c.ROLE_TABLE_COMPANY: '0',
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        self.assertEqual(None, id) 
        
# Company name is Blank
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: 'developer',
                    c.ROLE_TABLE_POLICY: '0',
                    c.ROLE_TABLE_COMPANY: '',
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        self.assertEqual(None, id) 
        
# Company name is NULL
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: 'developer',
                    c.ROLE_TABLE_POLICY: '0',
                    c.ROLE_TABLE_COMPANY: None,
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        self.assertEqual(None, id) 
        
        
# Policy is Blank
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: 'developer',
                    c.ROLE_TABLE_POLICY: '',
                    c.ROLE_TABLE_COMPANY: '0',
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        assert id is not None 
        
# Policy is NULL
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME: 'developer',
                    c.ROLE_TABLE_POLICY: None,
                    c.ROLE_TABLE_COMPANY: '0',
                    c.ROLE_TABLE_CREATED_ON: time.strftime("%c"),
                    c.ROLE_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = role1.add_role(roleDict)
        assert id is not None 
        
        
################# Test cases for get_role(id,pluck) ################################
 
# All OK
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_user(tabID,[c.ROLE_TABLE_NAME])
        assert id is not None

         
#List not sent in pluck      
class MyTestCase9(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        id = role1.get_role(tabID,c.ROLE_TABLE_NAME)
        self.assertEqual(None, id)  
         
         
#Wrong tableID       
class MyTestCase10(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        tableID = '38a9ab90-ad9'
        id = role1.get_role(tableID,[c.ROLE_TABLE_NAME])
        self.assertEqual(None, id)
         
# tableID is List       
class MyTestCase11(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        tableID = [tabID]
        id = role1.get_role(tableID,[c.ROLE_TABLE_NAME])
        self.assertEqual(None, id)
        
# tableID is NULL       
class MyTestCase12(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        tableID = None
        id = role1.get_role(tableID,[c.ROLE_TABLE_NAME])
        self.assertEqual(None, id)
         
# Pluck is None       
class MyTestCase13(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role(tabID,None)
        self.assertEqual(None, id)
         
# Pluck is Empty       
class MyTestCase14(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role(tabID,'')
        self.assertEqual(None, id)
         
# Pluck is dict       
class MyTestCase15(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role(tableID,{c.ROLE_TABLE_NAME})
        self.assertEqual(None, id) 
        
################# Test cases for get_role(name,company,pluck) ################################            
# All OK
class MyTestCase16(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_user('developer','0',[c.ROLE_TABLE_POLICY])
        assert id is not None

         
#List not sent in pluck      
class MyTestCase17(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('developer','0',c.ROLE_TABLE_POLICY)
        self.assertEqual(None, id)  
         
         
#Wrong name       
class MyTestCase18(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('devafjhbjfbajf','0',[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)
         
# name is blank      
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('','0',[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)
        
# name is NULL       
class MyTestCase20(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        tableID = None
        id = role1.get_role(None,'0',[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)
         
# Pluck is None       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('developer','0',None)
        self.assertEqual(None, id)
         
# Pluck is Empty       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('developer','0','')
        self.assertEqual(None, id)
         
# Pluck is dict       
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('developer','0',{c.ROLE_TABLE_POLICY})
        self.assertEqual(None, id) 
        
        
# Company is None       
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('developer',None,[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)
         
# Company is Empty       
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_role('developer','',[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)

################# Test cases for update_role(id,role) ################################ 

# All OK       
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME : 'manager'
                   }
        id = role1.update_role(tabID, roleDict)
        self.assertEqual(True, id)
         
# tableID is Empty       
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME : 'manager'
                   }
        id = role1.update_role('', roleDict)
        self.assertEqual(False, id)
        
# tableID is None       
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                    c.ROLE_TABLE_NAME : 'manager'
                   }
        id = role1.update_role(None, roleDict)
        self.assertEqual(False, id)
        
# role  is empty dict       
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = {
                   }
        id = role1.update_role(tabID, roleDict)
        self.assertEqual(False, id)
        
# role  is not dict       
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = [{
                    c.ROLE_TABLE_NAME : 'manager'
                   }]
        id = role1.update_role(tabID, roleDict)
        self.assertEqual(False, id)
        
# role  is NULL       
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        roleDict = None
        id = role1.update_role(tabID, roleDict)
        self.assertEqual(False, id)
        
        
################# Test cases for delete_role(id) ################################ 

# All OK       
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.delete_role(tabID)
        self.assertEqual(True, id)
        
# tableID is blank       
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.delete_role('')
        self.assertEqual(False, id)
        
# tableID is None       
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.delete_role(None)
        self.assertEqual(False, id)
        
# tableID is not string       
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.delete_role([tabID])
        self.assertEqual(False, id)
        

################# Test cases for get_roles(company,pluck) ################################ 

# All OK
class MyTestCase36(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles('0',[c.ROLE_TABLE_POLICY])
        assert id is not None

         
# List not sent in pluck      
class MyTestCase37(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles('0',c.ROLE_TABLE_POLICY)
        self.assertEqual(None, id) 
        
#Pluck List is empty    
class MyTestCase38(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles('0',[''])
        self.assertEqual(None, id)
        
#Pluck List is NULL    
class MyTestCase39(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles('0',None)
        self.assertEqual(None, id)
        
#Company is NULL    
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles(None,[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)
        
#Company is empty    
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles('',[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)
        
#Company is list    
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        role1 = RoleDBHelper()
        id = role1.get_roles(['0'],[c.ROLE_TABLE_POLICY])
        self.assertEqual(None, id)


if __name__ == '__main__':
    unittest.main()  
        
         
  



