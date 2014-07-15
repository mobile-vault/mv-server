from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.device import *
from toppatch_db.constants import Constants as c


#     DEVICE_TABLE = ''
#     DEVICE_TABLE_ID = ''
#     DEVICE_TABLE_USER = ''
#     DEVICE_TABLE_NAME = ''
#     DEVICE_TABLE_COMPANY = ''
#     DEVICE_TABLE_UDID = ''  #May contain UDID or IMEI depending on the OS.
#     DEVICE_TABLE_OS = ''

userTableID = '' #'38a9ab90-ad9c-46a7-ac94-9f984a4d93af'
deviceTableID = ''
deviceUDID = ''

################# Test cases for add_device()  ###################################
#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: userTableID,
                      c.DEVICE_TABLE_NAME: 'abc-android',
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: '0'
                     }
        id = device1.add_device(deviceDict)
        assert id is not None
        print id
        

#userTableID is Blank
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: '',
                      c.DEVICE_TABLE_NAME: 'abc-android',
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: '0'
                     }
        id = device1.add_device(deviceDict)
        self.assertEqual(None, id)
        
#userTableID is None
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: None,
                      c.DEVICE_TABLE_NAME: 'abc-android',
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: '0'
                     }
        id = device1.add_device(deviceDict)
        self.assertEqual(None, id)
        
        
        
#deviceName is Blank
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: userTableID,
                      c.DEVICE_TABLE_NAME: '',
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: '0'
                     }
        id = device1.add_device(deviceDict)
        self.assertEqual(None, id)
        
#deviceName is None
class MyTestCase6(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: userTableID,
                      c.DEVICE_TABLE_NAME: None,
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: '0'
                     }
        id = device1.add_device(deviceDict)
        self.assertEqual(None, id)
        
#Company is None
class MyTestCase7(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: userTableID,
                      c.DEVICE_TABLE_NAME: 'abc-android',
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: None
                     }
        id = device1.add_device(deviceDict)
        self.assertEqual(None, id)
        
#Company is Blank
class MyTestCase8(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_USER: userTableID,
                      c.DEVICE_TABLE_NAME: 'abc-android',
                      c.DEVICE_TABLE_OS: 'Android',
                      c.DEVICE_TABLE_COMPANY: ''
                     }
        id = device1.add_device(deviceDict)
        self.assertEqual(None, id)            



        
# TODO: Check again for wrong parameters of pluck()        
####### Test case for get_device(id) ###################################

# All OK
class MyTestCase19(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        id = device1.get_device(deviceTableID)
        assert id is not None
        
        
#Wrong tableID       
class MyTestCase21(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = '38a9ab90-ad9'
        id = device1.get_device(tableID)
        self.assertEqual(None, id)
        
# tableID is List       
class MyTestCase22(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = [deviceTableID]
        id = device1.get_device(tableID)
        self.assertEqual(None, id)
        
# tableID is None       
class MyTestCase22ab(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = None
        id = device1.get_device(tableID)
        self.assertEqual(None, id)            
        
        
################### Test Case for update_device() #######################################

##All OK
class MyTestCase23(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_NAME: 'atul',
                      c.DEVICE_TABLE_UDID: 'uifahiue8fy83yf888',
                      c.DEVICE_TABLE_OS: 'iOS'
                     }
        id = device1.update_device(deviceTableID, deviceDict)
        self.assertEqual(True, id)
        
##TableID is wrong DEVICE_TABLE_ID
class MyTestCase24(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = '38a9ab90-ad9c-46a7-ac9'
        deviceDict = {
                      c.DEVICE_TABLE_NAME: 'ios abc',
                      c.DEVICE_TABLE_UDID: 'uifahiue8fy83yf888',
                      c.DEVICE_TABLE_OS: 'iOS'
                     }
        id = device1.update_device(tableID, deviceDict)
        self.assertEqual(False, id)
        
    
##TableID is Blank
class MyTestCase25(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = ''
        deviceDict = {
                      c.DEVICE_TABLE_NAME: 'ios abc',
                      c.DEVICE_TABLE_UDID: 'uifahiue8fy83yf888',
                      c.DEVICE_TABLE_OS: 'iOS'
                     }
        id = device1.update_device(tableID, deviceDict)
        self.assertEqual(False, id)
        
##TableID is None
class MyTestCase26(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = None
        deviceDict = {
                      c.DEVICE_TABLE_NAME: 'ajfh hajb',
                      c.DEVICE_TABLE_UDID: 'uifahiue8fy83yf888',
                      c.DEVICE_TABLE_OS: 'iOS'
                     }
        id = device1.update_device(tableID, deviceDict)
        self.assertEqual(False, id)


##TableID is List
class MyTestCase27(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = [deviceTableID]
        deviceDict = {
                      c.DEVICE_TABLE_NAME: 'uiafbh ab',
                      c.DEVICE_TABLE_UDID: 'uifahiue8fy83yf888',
                      c.DEVICE_TABLE_OS: 'iOS'
                     }
        id = device1.update_device(tableID, deviceDict)
        self.assertEqual(False, id)
        
##updateDict is List
class MyTestCase28(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = [{
                      c.DEVICE_TABLE_NAME: 'askjjkb',
                      c.DEVICE_TABLE_UDID: 'uifahiue8fy83yf888',
                      c.DEVICE_TABLE_OS: 'iOS'
                     }]
        id = device1.update_device(deviceTableID, deviceDict)
        self.assertEqual(False, id)

##updateDict is Blank
class MyTestCase29(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {}
        id = device1.update_device(deviceTableID, deviceDict)
        self.assertEqual(False, id)


##updateDict is NULL
class MyTestCase30(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = None
        id = device1.update_device(deviceTableID, deviceDict)
        self.assertEqual(False, id)
        
##Can't update deviceTableID
class MyTestCase30a(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_ID: 'ahjgjhjabkcjjk78yabjjb',
                    }
        id = device1.update_device(deviceTableID, deviceDict)
        self.assertEqual(False, id)
        
##Can't update company
class MyTestCase30b(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        deviceDict = {
                      c.DEVICE_TABLE_COMPANY: '1'
                     }
        id = device1.update_device(deviceTableID, deviceDict)
        self.assertEqual(False, id)



############## Test cases for delete_device() ################################

# All OK
class MyTestCase31(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        id = device1.delete_device(deviceTableID)
        self.assertEqual(True, id)


# Incorrect tableID        
class MyTestCase32(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = '38a9ab90-ad9c-46a7-a'
        id = device1.delete_device(tableID)
        self.assertEqual(False, id)
        
    
# Blank tableID        
class MyTestCase33(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = ''
        id = device1.delete_device(tableID)
        self.assertEqual(False, id)
        
        
# NULL tableID        
class MyTestCase34(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = None
        id = device1.delete_device(tableID)
        self.assertEqual(False, id)
        
#  tableID is list        
class MyTestCase35(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        tableID = [deviceTableID]
        id = device1.delete_device(tableID)
        self.assertEqual(False, id)
        

################### Test cases for get_devices() ##############################

#All OK
class MyTestCase36(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        filterDict = {
                      c.DEVICE_TABLE_COMPANY: '0',
                      c.DEVICE_TABLE_UDID: deviceUDID,
                      c.DEVICE_TABLE_OS: 'iOS'
                     }
        id = device1.get_devices(filterDict)
        assert id is not None
        print id

#Wrong details in the filter        
class MyTestCase37(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        filterDict = {
                      c.DEVICE_TABLE_COMPANY: 'fgdeagdghadefdegvdadea@gmail.com',
                      c.DEVICE_TABLE_UDID: 'fsdzvvsgs',
                      c.DEVICE_TABLE_OS: 'develgagaeeagtertvddoper'
                     }
        id = device1.get_devices(filterDict)
        self.assertEqual(None, id)


#filter is a list        
class MyTestCase38(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        filterDict = [{
                      c.DEVICE_TABLE_COMPANY: 'fgdeagdghadefdegvdadea@gmail.com',
                      c.DEVICE_TABLE_UDID: 'fsdzvvsgs',
                      c.DEVICE_TABLE_OS: 'develgagaeeagtertvddoper'
                     }]
        id = device1.get_devices(filterDict)
        self.assertEqual(None, id)
        
#filter is a empty        
class MyTestCase39(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        filterDict = {}
        id = device1.get_devices(filterDict)
        self.assertEqual(None, id)
 
#filter is a NULL         
class MyTestCase40(AsyncTestCase):
    def test_http_fetch(self):
        device1 = DeviceDBHelper()
        filterDict = None
        id = device1.get_devices(filterDict)
        self.assertEqual(None, id)


        
if __name__ == '__main__':
    unittest.main()  