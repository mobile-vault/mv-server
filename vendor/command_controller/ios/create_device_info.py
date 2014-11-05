import threading

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class DeviceInfoCreaterThread(threading.Thread):
    profile = 'finalProfile'

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print 'PolicyCreater'
        print self.json_array

        self.profile = ET.Element('plist')
        self.profile.attrib['version'] = '1.0'

#         deviceInfo = ET.Element('plist')
#         deviceInfo.attrib['version'] = '1.0'

        dict = ET.SubElement(self.profile, "dict")
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
        IsDeviceLocatorServiceEnabled.text = 'IsDeviceLocatorServiceEnabled'

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
        string2.text = '11111111-1111-1111-1111-111111111111'

        self.profile = ET.tostring(self.profile)
