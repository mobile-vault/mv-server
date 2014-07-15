from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.team import *
from toppatch_db.constants import Constants as c
import time

#     TEAM_TABLE = ''
#     TEAM_TABLE_ID = ''
#     TEAM_TABLE_NAME =''
#     TEAM_TABLE_COMPANY = ''
#     TEAM_TABLE_CREATED_ON = ''
#     TEAM_TABLE_POLICY = ''
#     TEAM_TABLE_LAST_MODIFIED = ''

tabID = 'any id field from Teams Table'

################# Test cases for add_team()  ###################################

#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: 'developement',
                    c.TEAM_TABLE_POLICY: '0',
                    c.TEAM_TABLE_COMPANY: '0',
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        assert id is not None
        print id
    
# Team name is blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: '',
                    c.TEAM_TABLE_POLICY: '0',
                    c.TEAM_TABLE_COMPANY: '0',
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        self.assertEqual(None, id) 
        
        
# Team name is NULL
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: None,
                    c.TEAM_TABLE_POLICY: '0',
                    c.TEAM_TABLE_COMPANY: '0',
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        self.assertEqual(None, id) 
        
# Company name is Blank
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: 'developement',
                    c.TEAM_TABLE_POLICY: '0',
                    c.TEAM_TABLE_COMPANY: '',
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        self.assertEqual(None, id) 
        
# Company name is NULL
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: 'developement',
                    c.TEAM_TABLE_POLICY: '0',
                    c.TEAM_TABLE_COMPANY: None,
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        self.assertEqual(None, id) 
        
        
# Policy is Blank
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: 'developement',
                    c.TEAM_TABLE_POLICY: '',
                    c.TEAM_TABLE_COMPANY: '0',
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        assert id is not None 
        
# Policy is NULL
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME: 'developement',
                    c.TEAM_TABLE_POLICY: None,
                    c.TEAM_TABLE_COMPANY: '0',
                    c.TEAM_TABLE_CREATED_ON: time.strftime("%c"),
                    c.TEAM_TABLE_LAST_MODIFIED: time.strftime("%c")
                    }
        id = team1.add_team(teamDict)
        assert id is not None 
        
        
################# Test cases for get_team(id,pluck) ################################
 
# All OK
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_team(tabID,[c.TEAM_TABLE_NAME])
        assert id is not None

         
#List not sent in pluck      
class MyTestCase9(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_team(tabID,c.TEAM_TABLE_NAME)
        self.assertEqual(None, id)  
         
         
#Wrong tableID       
class MyTestCase10(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        tableID = '38a9ab90-ad9'
        id = team1.get_team(tableID,[c.TEAM_TABLE_NAME])
        self.assertEqual(None, id)
         
# tableID is List       
class MyTestCase11(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        tableID = [tabID]
        id = team1.get_team(tableID,[c.TEAM_TABLE_NAME])
        self.assertEqual(None, id)
        
# tableID is NULL       
class MyTestCase12(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        tableID = None
        id = team1.get_team(tableID,[c.TEAM_TABLE_NAME])
        self.assertEqual(None, id)
         
# Pluck is None       
class MyTestCase13(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams(tabID,None)
        self.assertEqual(None, id)
         
# Pluck is Empty       
class MyTestCase14(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_team(tabID,'')
        self.assertEqual(None, id)
         
# Pluck is dict       
class MyTestCase15(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_team(tableID,{c.TEAM_TABLE_NAME})
        self.assertEqual(None, id) 
        
# ################# Test cases for get_role(name,company,pluck) ################################            
# # All OK
# class MyTestCase16(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer','0',[c.TEAM_TABLE_POLICY])
#         assert id is not None
# 
#          
# #List not sent in pluck      
# class MyTestCase17(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer','0',c.TEAM_TABLE_POLICY)
#         self.assertEqual(None, id)  
#          
#          
# #Wrong name       
# class MyTestCase18(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('devafjhbjfbajf','0',[c.TEAM_TABLE_POLICY])
#         self.assertEqual(None, id)
#          
# # name is blank      
# class MyTestCase19(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('','0',[c.TEAM_TABLE_POLICY])
#         self.assertEqual(None, id)
#         
# # name is NULL       
# class MyTestCase20(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         tableID = None
#         id = team1.get_team(None,'0',[c.TEAM_TABLE_POLICY])
#         self.assertEqual(None, id)
#          
# # Pluck is None       
# class MyTestCase21(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer','0',None)
#         self.assertEqual(None, id)
#          
# # Pluck is Empty       
# class MyTestCase22(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer','0','')
#         self.assertEqual(None, id)
#          
# # Pluck is dict       
# class MyTestCase23(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer','0',{c.TEAM_TABLE_POLICY})
#         self.assertEqual(None, id) 
#         
#         
# # Company is None       
# class MyTestCase24(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer',None,[c.TEAM_TABLE_POLICY])
#         self.assertEqual(None, id)
#          
# # Company is Empty       
# class MyTestCase25(AsyncTestCase):
#     def test_http_fetch(self):
#         team1 = TeamDBHelper()
#         id = team1.get_team('developer','',[c.TEAM_TABLE_POLICY])
#         self.assertEqual(None, id)

################# Test cases for update_team(id,team) ################################ 

# All OK       
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME : 'Management'
                   }
        id = team1.update_team(tabID, teamDict)
        self.assertEqual(True, id)
         
# tableID is Empty       
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME : 'Management'
                   }
        id = team1.update_team('', teamDict)
        self.assertEqual(False, id)
        
# tableID is None       
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                    c.TEAM_TABLE_NAME : 'Management'
                   }
        id = team1.update_team(None, teamDict)
        self.assertEqual(False, id)
        
# team is empty dict       
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = {
                   }
        id = team1.update_team(tabID, teamDict)
        self.assertEqual(False, id)
        
# team  is not dict       
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = [{
                    c.TEAM_TABLE_NAME : 'Management'
                   }]
        id = team1.update_team(tabID, teamDict)
        self.assertEqual(False, id)
        
# team  is NULL       
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        teamDict = None
        id = team1.update_team(tabID, teamDict)
        self.assertEqual(False, id)
        
        
################# Test cases for delete_team(id) ################################ 

# All OK       
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.delete_team(tabID)
        self.assertEqual(True, id)
        
# tableID is blank       
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.delete_team('')
        self.assertEqual(False, id)
        
# tableID is None       
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.delete_team(None)
        self.assertEqual(False, id)
        
# tableID is not string       
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.delete_team([tabID])
        self.assertEqual(False, id)
        

################# Test cases for get_roles(company,pluck) ################################ 

# All OK
class MyTestCase36(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams('0',[c.TEAM_TABLE_POLICY])
        assert id is not None

         
# List not sent in pluck      
class MyTestCase37(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams('0',c.TEAM_TABLE_POLICY)
        self.assertEqual(None, id) 
        
#Pluck List is empty    
class MyTestCase38(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams('0',[''])
        self.assertEqual(None, id)
        
#Pluck List is NULL    
class MyTestCase39(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams('0',None)
        self.assertEqual(None, id)
        
#Company is NULL    
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams(None,[c.TEAM_TABLE_POLICY])
        self.assertEqual(None, id)
        
#Company is empty    
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams('',[c.TEAM_TABLE_POLICY])
        self.assertEqual(None, id)
        
#Company is list    
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        team1 = TeamDBHelper()
        id = team1.get_teams(['0'],[c.TEAM_TABLE_POLICY])
        self.assertEqual(None, id)


if __name__ == '__main__':
    unittest.main()  
        
         
  



