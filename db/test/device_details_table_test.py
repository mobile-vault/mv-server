from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.devicedetail import *
from toppatch_db.constants import Constants as c

#     #Device details table. Add single table
#     DEVICE_DETAILS_TABLE = ''
#     DEVICE_DETAILS_TABLE_ID = ''
#     DEVICE_DETAILS_TABLE_DEVICE = ''
#     DEVICE_DETAILS_TABLE_PUSH_MAGIC = ''
#     DEVICE_DETAILS_TABLE_DEVICE_TOCKEN = ''
#     DEVICE_DETAILS_TABLE_UNLOCK_TOKEN = ''
#     DEVICE_DETAILS_TABLE_GCM_REG_NO = ''

deviceDetailTableID = ''
deviceTableID = ''

################# Test cases for add_devicedetails()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE: deviceTableID,
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.add_devicedetails(deviceDetailDict)
        assert id is not None
        print id
        

#deviceTableID is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE: '',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.add_devicedetails(deviceDetailDict)
        self.assertEqual(None, id)
        
#deviceTableID is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE: None,
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.add_devicedetails(deviceDetailDict)
        self.assertEqual(None, id)
        
        
#GCM_REG_NO is blank
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE: deviceTableID,
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: ''
                           }
        id = deviceDetail1.add_devicedetails(deviceDetailDict)
        self.assertEqual(None, id)
        
        
#GCM_REG_NO is None
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE: deviceTableID,
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: None
                           }
        id = deviceDetail1.add_devicedetails(deviceDetailDict)
        self.assertEqual(None, id)
        
        

        
# TODO: Check again for wrong parameters of pluck()        
####### Test case for get_devicedetails() ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        id = deviceDetail1.get_devicedetail(deviceTableID)
        assert id is not None
        
# tableID is blank      
class MyTestCase20(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = ''
        id = deviceDetail1.get_devicedetail(tableID)
        self.assertEqual(None, id)            
        
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = '38a9ab90-ad9'
        id = deviceDetail1.get_devicedetail(tableID)
        self.assertEqual(None, id)
        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = [deviceTableID]
        id = deviceDetail1.get_devicedetail(tableID)
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = None
        id = deviceDetail1.get_devicedetail(tableID)
        self.assertEqual(None, id)
        
          
        
        
################### Test Case for update_devicedetails() #######################################

##All OK update only iOS details
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(True, id)
 
 
# All OK update only ANdroid details       
class MyTestCase23a(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(True, id)
        
##TableID is wrong
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac9'
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }
        id = deviceDetail1.update_devicedetails(tableID, deviceDetailDict)
        self.assertEqual(False, id)
        
    
##TableID is Blank
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = ''
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }
        id = deviceDetail1.update_devicedetails(tableID, deviceDetailDict)
        self.assertEqual(False, id)
        
##TableID is None
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = None
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }
        id = deviceDetail1.update_devicedetails(tableID, deviceDetailDict)
        self.assertEqual(False, id)


##TableID is List
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = [deviceDetailTableID]
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }
        id = deviceDetail1.update_devicedetails(tableID, deviceDetailDict)
        self.assertEqual(False, id)
        
##updateDict is List
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = [{
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken'
                            }]
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)

##updateDict is Blank
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {}
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)


##updateDict is NULL
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = None
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)
        
##Can't updating iOS and Android both
class MyTestCase30a(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE: deviceTableID,
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)
        
##Can't updating iOS and Android both
class MyTestCase30b(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)
        

##Can't updating iOS and Android both
class MyTestCase30c(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)
        
        
##Can't updating iOS and Android both
class MyTestCase30d(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)


##Can't updating iOS and Android both
class MyTestCase30e(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)
        
##Can't updating iOS and Android both
class MyTestCase30f(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_UNLOCK_TOKEN: 'unlockToken',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)
        
##Can't updating iOS and Android both
class MyTestCase30g(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        deviceDetailDict = {
                            c.DEVICE_DETAILS_TABLE_DEVICE_TOCKEN: 'deviceToken',
                            c.DEVICE_DETAILS_TABLE_PUSH_MAGIC: 'pushMagic',
                            c.DEVICE_DETAILS_TABLE_GCM_REG_NO: 'GCMRegNo'
                           }
        id = deviceDetail1.update_devicedetails(deviceDetailTableID, deviceDetailDict)
        self.assertEqual(False, id)


############## Test cases for delete_devicedetails() ################################

# All OK
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        id = deviceDetail1.delete_devicedetails(deviceDetailTableID)
        self.assertEqual(True, id)


# Incorrect tableID        
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = '38a9ab90-ad9c-46a7-a'
        id = deviceDetail1.delete_devicedetails(tableID)
        self.assertEqual(False, id)
        
    
# Blank tableID        
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = ''
        id = deviceDetail1.delete_devicedetails(tableID)
        self.assertEqual(False, id)
        
        
# NULL tableID        
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = None
        id = deviceDetail1.delete_devicedetails(tableID)
        self.assertEqual(False, id)
        
#  tableID is list        
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        tableID = [deviceDetailTableID]
        id = deviceDetail1.delete_devicedetails(tableID)
        self.assertEqual(False, id)
        
################### Test cases for get_devicedetails() ##############################

#All OK
class MyTestCase36(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        filterDict = {
                      c.DEVICE_DETAILS_TABLE_DEVICE: deviceTableID
                     }
        id = deviceDetail1.get_devicedetails(filterDict)
        assert id is not None
        print id

#Wrong details in the filter        
class MyTestCase37(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        filterDict = {
                      c.DEVICE_DETAILS_TABLE_DEVICE: 'fgdeagdghadefdegvdadea@gmail.com'
                     }
        id = deviceDetail1.get_devicedetails(filterDict)
        self.assertEqual(None, id)


#filter is a list        
class MyTestCase38(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        filterDict = [{
                      c.DEVICE_DETAILS_TABLE_DEVICE: deviceTableID
                     }]
        id = deviceDetail1.get_devicedetails(filterDict)
        self.assertEqual(None, id)
        
#filter is a empty        
class MyTestCase39(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        filterDict = {}
        id = deviceDetail1.get_devicedetails(filterDict)
        self.assertEqual(None, id)
 
#filter is a NULL         
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        deviceDetail1 = DeviceDetailsDBHelper()
        filterDict = None
        id = deviceDetail1.get_devicedetails(filterDict)
        self.assertEqual(None, id)
        
        
if __name__ == '__main__':
    unittest.main()  
