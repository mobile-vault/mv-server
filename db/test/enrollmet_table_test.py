from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.enrollment import *
from toppatch_db.constants import Constants as c
import time

#     ENROLLMENT_TABLE = ''
#     ENROLLMENT_TABLE_ID =''
#     ENROLLMENT_TABLE_USER = ''
#     ENROLLMENT_TABLE_DEVICE = ''
#     ENROLLMENT_TABLE_PASSWORD = ''
#     ENROLLMENT_TABLE_ENROLLED_ON = ''
#     ENROLLMENT_TABLE_SENT_ON = ''

validUserTableID = '' #'38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
validDeviceTableID = ''
enrollmentTableID = ''

################# Test cases for add_enrollment()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'development',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                          }
        id = enrollment1.add_enrollment(enrollmentDict)
        assert id is not None
        print id
        

#UserTableID is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: '',
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'development',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
#UserTableID is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: None,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'development',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
        
#UserTableID is invalid
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: '95389389373983',
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'development',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
        
#DeviceTableID is Blank
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: '',
                          c.ENROLLMENT_TABLE_PASSWORD: 'development',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
#DeviceTableID is None
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: None,
                          c.ENROLLMENT_TABLE_PASSWORD: 'development',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
#Password is None
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: None,
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
#Password is Blank
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: '',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)            


#Sent_on Time is blank        
class MyTestCase9(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'developer',
                          c.ENROLLMENT_TABLE_SENT_ON: ''
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        assert id is not None
        print id
        
#SentON is NULL        
class MyTestCase10(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'developer',
                          c.ENROLLMENT_TABLE_SENT_ON: None
                         }
        id = enrollment1.add_enrollment(enrollmentDict)
        assert id is not None
        print id
        
        
#Dictionary not sent        
class MyTestCase18(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = [{
                          c.ENROLLMENT_TABLE_USER: validUserTableID,
                          c.ENROLLMENT_TABLE_DEVICE: validDeviceTableID,
                          c.ENROLLMENT_TABLE_PASSWORD: 'developer',
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                         }]
        id = enrollment1.add_enrollment(enrollmentDict)
        self.assertEqual(None, id)
        
# TODO: Check again for wrong parameters of pluck()        
####### Test case for get_enrollment(id) ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        id = enrollment1.get_enrollment(enrollmentTableID)
        assert id is not None
        
        
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = '38a9ab90-ad9'
        id = enrollment1.get_enrollment(tableID)
        self.assertEqual(None, id)
        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = [enrollmentTableID]
        id = enrollment1.get_enrollment(tableID)
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = None
        id = enrollment1.get_enrollment(tableID)
        self.assertEqual(None, id)
                 
        
        
################### Test Case for update_enrollment() #######################################

##All OK
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                          }
        id = enrollment1.update_enrollment(enrollmentTableID, enrollmentDict)
        self.assertEqual(True, id)
        
##TableID is wrong
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac9'
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                          }
        id = enrollment1.update_enrollment(tableID, enrollmentDict)
        self.assertEqual(False, id)
        
    
##TableID is Blank
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = ''
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                        }
        id = enrollment1.update_enrollment(tableID, enrollmentDict)
        self.assertEqual(False, id)
        
##TableID is None
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = None
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                          }
        id = enrollment1.update_enrollment(tableID, enrollmentDict)
        self.assertEqual(False, id)


##TableID is List
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = [enrollmentTableID]
        enrollmentDict = {
                          c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                          }
        id = enrollment1.update_enrollment(tableID, enrollmentDict)
        self.assertEqual(False, id)
        
##enrollmentDict is List
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        enrollmentDict = [{
                           c.ENROLLMENT_TABLE_SENT_ON: time.strftime("%c")
                           }]
        id = enrollment1.update_enrollment(tableID, enrollmentDict)
        self.assertEqual(False, id)

##enrollmentDict is Blank
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = {}
        id = enrollment1.update_enrollment(enrollmentTableID, enrollmentDict)
        self.assertEqual(False, id)


##enrollmentDict is NULL
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        enrollment1 = EnrollmentDBHelper()
        enrollmentDict = None
        id = enrollment1.update_enrollment(enrollmentTableID, enrollmentDict)
        self.assertEqual(False, id)
        


# ############## Test cases for delete_enrollment() ################################
# 
# # All OK
# class MyTestCase31(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
#         id = enrollment1.delete_enrollment(tableID)
#         self.assertEqual(True, id)
# 
# 
# # Incorrect tableID        
# class MyTestCase32(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         tableID = '38a9ab90-ad9c-46a7-a'
#         id = enrollment1.delete_enrollment(tableID)
#         self.assertEqual(False, id)
#         
#     
# # Blank tableID        
# class MyTestCase33(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         tableID = ''
#         id = enrollment1.delete_enrollment(tableID)
#         self.assertEqual(False, id)
#         
#         
# # NULL tableID        
# class MyTestCase34(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         tableID = None
#         id = enrollment1.delete_enrollment(tableID)
#         self.assertEqual(False, id)
#         
# #  tableID is list        
# class MyTestCase35(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         tableID = ['38a9ab90-ad9c-46a7-ac94-9f984a4d93af']
#         id = enrollment1.delete_enrollment(tableID)
#         self.assertEqual(False, id)
#         
#         
# ################### Test cases for get_enrollments() ##############################
# 
# #All OK
# class MyTestCase36(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         filterDict = {
#                       c.ENROLLMENT_TABLE_USER: 'atuldhawan90@gmail.com',
#                       c.ENROLLMENT_TABLE_PASSWORD: 'development',
#                       c.USER_TABLE_ROLE: 'developer'
#                      }
#         id = enrollment1.get_enrollments(filterDict)
#         print id
# 
# #Wrong details in the filter        
# class MyTestCase37(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         filterDict = {
#                       c.ENROLLMENT_TABLE_USER: 'fgdeagdghadefdegvdadea@gmail.com',
#                       c.ENROLLMENT_TABLE_PASSWORD: 'fsdzvvsgs',
#                       c.USER_TABLE_ROLE: 'develgagaeeagtertvddoper'
#                      }
#         id = enrollment1.get_enrollments(filterDict)
#         self.assertEqual(False, id)
# 
# 
# #filter is a list        
# class MyTestCase38(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         filterDict = [{
#                       c.ENROLLMENT_TABLE_USER: 'atuldhawan90@gmail.com',
#                       c.ENROLLMENT_TABLE_PASSWORD: 'development',
#                       c.USER_TABLE_ROLE: 'developer'
#                      }]
#         id = enrollment1.get_enrollments(filterDict)
#         self.assertEqual(False, id)
#         
# #filter is a empty        
# class MyTestCase39(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         filterDict = {}
#         id = enrollment1.get_enrollments(filterDict)
#         self.assertEqual(False, id)
#  
# #filter is a NULL         
# class MyTestCase40(AsyncTestCase):
#     def test_http_fetch(self):
#         enrollment1 = EnrollmentDBHelper()
#         filterDict = None
#         id = enrollment1.get_enrollments(filterDict)
#         self.assertEqual(False, id)
        
        
if __name__ == '__main__':
    unittest.main()  