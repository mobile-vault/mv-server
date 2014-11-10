import base64
import threading

from vendor.command_controller.ios.create_policy_with_dict import PolicyCreater
from db.constants import Constants as c
from db.helpers.device_details import DeviceDetailsDBHelper
from logger import Logger

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class IOSCommandCreatorThread(threading.Thread):
    log = 'log'
    command_profile = 'command_profile'

    def __init__(self, action, command_attributes, command_uuid, device_id):
        threading.Thread.__init__(self)
        print 'IN PolicyFinder\'s init'

        self.action = action
        self.command_attributes = command_attributes
        self.command_uuid = command_uuid
        self.device_id = device_id

#### Main function which will call other functions ###########################
    def run(self):
        self.log = Logger('IOSCommandCreatorThread')
        TAG = 'run'
        print 'action = ' + str(self.action)
        if self.action == 'policy':
            print 'In polcy condition'
            # print 'command attributes'
            # print self.command_attributes
            thread1 = PolicyCreater(self.command_attributes)
            thread1.start()
            thread1.join()
            # call the policy function

            finalProfile = thread1.profile
            print '\n\nfinalProfile in ios_command\n' + str(finalProfile)

            installProfile = ET.Element('plist')
            installProfile.attrib['version'] = '1.0'
            dict = ET.SubElement(installProfile, "dict")
            key = ET.SubElement(dict, "key")
            key.text = "Command"
            dict1 = ET.SubElement(dict, "dict")
            key1 = ET.SubElement(dict1, "key")
            key1.text = "RequestType"
            string1 = ET.SubElement(dict1, "string")
            string1.text = "InstallProfile"
            key2 = ET.SubElement(dict1, 'key')
            key2.text = 'Payload'
            data2 = ET.SubElement(dict1, 'data')

            encoded = base64.b64encode(finalProfile)
            data2.text = encoded
            key3 = ET.SubElement(dict, "key")
            key3.text = "CommandUUID"
            string2 = ET.SubElement(dict, "string")
            string2.text = str(self.command_uuid)

            # print ET.tostring(installProfile)
            self.command_profile = ET.tostring(installProfile)

        elif self.action == 'erase_device':
            # Create the Erase Device XML
            earseDevice = ET.Element('plist')
            earseDevice.attrib['version'] = '1.0'
            dict = ET.SubElement(earseDevice, "dict")
            key = ET.SubElement(dict, "key")
            key.text = "Command"
            dict1 = ET.SubElement(dict, "dict")
            key1 = ET.SubElement(dict1, "key")
            key1.text = "RequestType"
            string1 = ET.SubElement(dict1, "string")
            string1.text = "EraseDevice"
            key3 = ET.SubElement(dict, "key")
            key3.text = "CommandUUID"
            string2 = ET.SubElement(dict, "string")
            string2.text = str(self.command_uuid)
            self.command_profile = ET.tostring(earseDevice)

        elif self.action == 'device_lock':
            # Create the Device Lock XML
            deviceLock = ET.Element('plist')
            deviceLock.attrib['version'] = '1.0'
            dict = ET.SubElement(deviceLock, "dict")
            key = ET.SubElement(dict, "key")
            key.text = "Command"
            dict1 = ET.SubElement(dict, "dict")
            key1 = ET.SubElement(dict1, "key")
            key1.text = "RequestType"
            string1 = ET.SubElement(dict1, "string")
            string1.text = "DeviceLock"
            key2 = ET.SubElement(dict, "key")
            key2.text = "CommandUUID"
            string2 = ET.SubElement(dict, "string")
            string2.text = str(self.command_uuid)
            self.command_profile = ET.tostring(deviceLock)

        elif self.action == 'clear_passcode':
            # First find the unlock Token of the device
            if self.device_id is None:
                self.log.e(TAG, 'No device ID of UUID = ' + str(
                    self.command_uuid))
            else:
                device_id = str(self.device_id)
                device_detail = DeviceDetailsDBHelper()
                device_detail_dict = device_detail.get_device_details(
                    device_id)
                json_extras = device_detail_dict.get(
                    c.DEVICE_DETAILS_TABLE_EXTRAS)
                device_unlock_token = str(json_extras.get('unlock_token'))

                if device_unlock_token is None:
                    self.log.e(TAG, 'Device Does not have unlock token,\
                                            Device ID = ' + str(device_id))
                else:

                    # Create the Clear Passcode XML
                    clearPasscode = ET.Element('plist')
                    clearPasscode.attrib['version'] = '1.0'
                    dict = ET.SubElement(clearPasscode, "dict")
                    key = ET.SubElement(dict, "key")
                    key.text = "Command"
                    dict1 = ET.SubElement(dict, "dict")
                    key1 = ET.SubElement(dict1, "key")
                    key1.text = "RequestType"
                    string1 = ET.SubElement(dict1, "string")
                    string1.text = "ClearPasscode"
                    key2 = ET.SubElement(dict1, "key")
                    key2.text = "UnlockToken"
                    data = ET.SubElement(dict1, 'data')
                    data.text = device_unlock_token
                    key2 = ET.SubElement(dict, "key")
                    key2.text = "CommandUUID"
                    string2 = ET.SubElement(dict, "string")
                    string2.text = str(self.command_uuid)
                    self.command_profile = ET.tostring(clearPasscode)

        elif self.action == 'install_application':
            # First get the APP ID
            app_id = str(self.command_attributes[0].get('app_id'))
            if app_id is None:
                self.log.e(TAG, 'App ID is not sent with the command. \
                           CommandUUID = ' + str(self.command_uuid))
            else:
                # Create the Install Application XML
                installApplication = ET.Element('plist')
                installApplication.attrib['version'] = '1.0'
                dict = ET.SubElement(installApplication, "dict")
                key = ET.SubElement(dict, "key")
                key.text = "Command"
                dict1 = ET.SubElement(dict, "dict")
                key1 = ET.SubElement(dict1, "key")
                key1.text = "RequestType"
                string1 = ET.SubElement(dict1, "string")
                string1.text = "InstallApplication"
                key2 = ET.SubElement(dict1, 'key')
                key2.text = 'iTunesStoreID'
                integer2 = ET.SubElement(dict1, 'integer')
                integer2.text = str(app_id)
                key3 = ET.SubElement(dict, "key")
                key3.text = "CommandUUID"
                string2 = ET.SubElement(dict, "string")
                string2.text = str(self.command_uuid)
                self.command_profile = ET.tostring(installApplication)

        elif self.action == 'remove_application':
            # First get the APP ID
            app_identifier = str(self.command_attributes[0].get(
                'app_identifier'))
            if app_identifier is None:
                self.log.e(TAG, 'App Identifier is not sent with the command. \
                           CommandUUID = ' + str(self.command_uuid))
            else:
                removeApplication = ET.Element('plist')
                removeApplication.attrib['version'] = '1.0'
                dict = ET.SubElement(removeApplication, "dict")
                key = ET.SubElement(dict, "key")
                key.text = "Command"
                dict1 = ET.SubElement(dict, "dict")
                key1 = ET.SubElement(dict1, "key")
                key1.text = "RequestType"
                string1 = ET.SubElement(dict1, "string")
                string1.text = "RemoveApplication"
                key2 = ET.SubElement(dict1, 'key')
                key2.text = 'Identifier'
                data2 = ET.SubElement(dict1, 'string')
                data2.text = str(app_identifier)
                key3 = ET.SubElement(dict, "key")
                key3.text = "CommandUUID"
                string2 = ET.SubElement(dict, "string")
                string2.text = str(self.command_uuid)
                self.command_profile = ET.tostring(removeApplication)

        elif self.action == 'installed_application_list':
            # Create the Device Lock XML
            installed_app_list = ET.Element('plist')
            installed_app_list.attrib['version'] = '1.0'
            dict = ET.SubElement(installed_app_list, "dict")
            key = ET.SubElement(dict, "key")
            key.text = "Command"
            dict1 = ET.SubElement(dict, "dict")
            key1 = ET.SubElement(dict1, "key")
            key1.text = "RequestType"
            string1 = ET.SubElement(dict1, "string")
            string1.text = "InstalledApplicationList"
            key2 = ET.SubElement(dict, "key")
            key2.text = "CommandUUID"
            string2 = ET.SubElement(dict, "string")
            string2.text = str(self.command_uuid)
            self.command_profile = ET.tostring(installed_app_list)

        elif self.action == 'device_information':

            deviceInfo = ET.Element('plist')
            deviceInfo.attrib['version'] = '1.0'

            dict = ET.SubElement(deviceInfo, "dict")
            key = ET.SubElement(dict, "key")
            key.text = "Command"
            dict1 = ET.SubElement(dict, "dict")
            key1 = ET.SubElement(dict1, "key")
            key1.text = "RequestType"
            string1 = ET.SubElement(dict1, "string")
            string1.text = "DeviceInformation"

            query = ET.SubElement(dict1, "key")
            query.text = 'Queries'

            array = ET.SubElement(dict1, 'array')
            udid_string = ET.SubElement(array, 'string')
            udid_string.text = 'UDID'

            locale_string = ET.SubElement(array, 'string')
            locale_string.text = 'Locales'

            deviceID_string = ET.SubElement(array, 'string')
            deviceID_string.text = 'DeviceID'

            OrganizationInfo_string = ET.SubElement(array, 'string')
            OrganizationInfo_string.text = 'OrganizationInfo'

            DeviceName_string = ET.SubElement(array, 'string')
            DeviceName_string.text = 'DeviceName'

            OSVersion_string = ET.SubElement(array, 'string')
            OSVersion_string.text = 'OSVersion'

            BuildVersion_string = ET.SubElement(array, 'string')
            BuildVersion_string.text = 'BuildVersion'

            ModelName_string = ET.SubElement(array, 'string')
            ModelName_string.text = 'ModelName'

            Model_string = ET.SubElement(array, 'string')
            Model_string.text = 'Model'

            ProductName_string = ET.SubElement(array, 'string')
            ProductName_string.text = 'ProductName'

            SerialNumber_string = ET.SubElement(array, 'string')
            SerialNumber_string.text = 'SerialNumber'

            DeviceCapacity_number = ET.SubElement(array, 'string')
            DeviceCapacity_number.text = 'DeviceCapacity'

            itune_account = ET.SubElement(array, 'string')
            itune_account.text = 'iTunesStoreAccountIsActive'

            available_capacity = ET.SubElement(array, 'string')
            available_capacity.text = 'AvailableDeviceCapacity'

            BatteryLevel = ET.SubElement(array, 'string')
            BatteryLevel.text = 'BatteryLevel'

            CellularTechnology = ET.SubElement(array, 'string')
            CellularTechnology.text = 'CellularTechnology'

            IMEI = ET.SubElement(array, 'string')
            IMEI.text = 'IMEI'

            MEID = ET.SubElement(array, 'string')
            MEID.text = 'MEID'

            ModemFirmwareVersion = ET.SubElement(array, 'string')
            ModemFirmwareVersion.text = 'ModemFirmwareVersion'

            IsSupervised = ET.SubElement(array, 'string')
            IsSupervised.text = 'IsSupervised'

            IsDeviceLocatorServiceEnabled = ET.SubElement(array, 'string')
            IsDeviceLocatorServiceEnabled.text = (
                'IsDeviceLocatorServiceEnabled')

            IsDoNotDisturbInEffect = ET.SubElement(array, 'string')
            IsDoNotDisturbInEffect.text = 'IsDoNotDisturbInEffect'

            ICCID = ET.SubElement(array, 'string')
            ICCID.text = 'ICCID'

            BluetoothMAC = ET.SubElement(array, 'string')
            BluetoothMAC.text = 'BluetoothMAC'

            WiFiMAC = ET.SubElement(array, 'string')
            WiFiMAC.text = 'WiFiMAC'

            EthernetMACs = ET.SubElement(array, 'string')
            EthernetMACs.text = 'EthernetMACs'

            CurrentCarrierNetwork = ET.SubElement(array, 'string')
            CurrentCarrierNetwork.text = 'CurrentCarrierNetwork'

            SIMCarrierNetwork = ET.SubElement(array, 'string')
            SIMCarrierNetwork.text = 'SIMCarrierNetwork'

            SubscriberCarrierNetwork = ET.SubElement(array, 'string')
            SubscriberCarrierNetwork.text = 'SubscriberCarrierNetwork'

            CarrierSettingsVersion = ET.SubElement(array, 'string')
            CarrierSettingsVersion.text = 'CarrierSettingsVersion'

            PhoneNumber = ET.SubElement(array, 'string')
            PhoneNumber.text = 'PhoneNumber'

            VoiceRoamingEnabled = ET.SubElement(array, 'string')
            VoiceRoamingEnabled.text = 'VoiceRoamingEnabled'

            DataRoamingEnabled = ET.SubElement(array, 'string')
            DataRoamingEnabled.text = 'DataRoamingEnabled'

            IsRoaming = ET.SubElement(array, 'string')
            IsRoaming.text = 'IsRoaming'

            PersonalHotspotEnabled = ET.SubElement(array, 'string')
            PersonalHotspotEnabled.text = 'PersonalHotspotEnabled'

            SubscriberMCC = ET.SubElement(array, 'string')
            SubscriberMCC.text = 'SubscriberMCC'

            SubscriberMNC = ET.SubElement(array, 'string')
            SubscriberMNC.text = 'SubscriberMNC'

            CurrentMCC = ET.SubElement(array, 'string')
            CurrentMCC.text = 'CurrentMCC'

            CurrentMNC = ET.SubElement(array, 'string')
            CurrentMNC.text = 'CurrentMNC'

            key3 = ET.SubElement(dict, "key")
            key3.text = "CommandUUID"
            string2 = ET.SubElement(dict, "string")
            string2.text = str(self.command_uuid)

            self.command_profile = ET.tostring(deviceInfo)

        elif self.action == 'remove_profile':
            profile_identifier = str(self.command_attributes[0].get(
                'profile_identifier'))
            removeProfile = ET.Element('plist')
            removeProfile.attrib['version'] = '1.0'
            dict = ET.SubElement(removeProfile, "dict")
            key = ET.SubElement(dict, "key")
            key.text = "Command"
            dict1 = ET.SubElement(dict, "dict")
            key1 = ET.SubElement(dict1, "key")
            key1.text = "RequestType"
            string1 = ET.SubElement(dict1, "string")
            string1.text = "RemoveProfile"
            key2 = ET.SubElement(dict1, 'key')
            key2.text = 'Identifier'
            data2 = ET.SubElement(dict1, 'string')
            data2.text = '{0}'.format(profile_identifier)
            key3 = ET.SubElement(dict, "key")
            key3.text = "CommandUUID"
            string2 = ET.SubElement(dict, "string")
            string2.text = str(self.command_uuid)
            self.command_profile = ET.tostring(removeProfile)

        else:
            self.command_profile = None
            self.log.e(TAG, 'Wrong action in command table')
