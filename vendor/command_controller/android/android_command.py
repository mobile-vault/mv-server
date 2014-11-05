# -*- coding: utf-8 -*-
from vendor.command_controller.engine import Engine
from db.helpers.device_details import DeviceDetailsDBHelper
from db.constants import Constants as C
from logger import Logger
import json
from gcm import GCM
from gcm.gcm import *
import config
from db.helpers.samsung_command import SamsungCommandsDBHelper
import uuid


class AndroidCommand(Engine):

    '''
    Send Commands to Samsung
    '''

    def __init__(self):
        self.log = Logger('AndroidCommand')

    def execute(self, json_dict, device_id, *args, **kwargs):
        TAG = 'execute'
        '''
        Call the function to send the command to Samsung
        '''
        special_uuid = '1717171717-17171717-1717117-1717'

        action_mapper = {'shutdown': 'power_off'}
        print 'sending to android' + str(device_id)

        device_details_helper = DeviceDetailsDBHelper()
        # Get the details of device from device_details table
        details = device_details_helper.get_device_details(str(device_id))
        if details is not None:
            # load the extras field. This is important here that the extras
            # field should be of dict type (and not json string)
            extras = details[C.DEVICE_DETAILS_TABLE_EXTRAS]
            if C.DEVICE_DETAILS_TABLE_GCM_REG_NO not in extras:
                self.log.e(TAG, 'gcm details not specified in ' + str(extras))
            else:
                # GCM Key for sending commands to GCM server
                gcm = GCM(config.GCM_KEY)
                reg_id = [
                    extras[
                        C.DEVICE_DETAILS_TABLE_GCM_REG_NO]]  # reg id of device

                # Now create a dict to be sent to the device
                data = dict()
                data['attributes'] = self.get_payload(json_dict)
                if 'action_command' in json_dict:
                    ui_action = json_dict['action_command']
                    if ui_action in action_mapper:
                        data['action'] = action_mapper.get(ui_action)
                    elif ui_action == 'device_lock':
                        data['attributes'][
                            'passcode'] = json_dict.get('passcode')
                        data['action'] = ui_action
                    else:
                        data['action'] = ui_action
                elif 'broadcast_command' in json_dict:
                    data['action'] = 'notification'
                    data['attributes']['data'] = {}
                    data['attributes']['data']['message'] = json_dict.get(
                        'broadcast_command')
                    data['attributes']['data'][
                        'title'] = 'Its Your GodFather!!!'
                else:
                    data['action'] = 'policy'

                if data['action'] == 'device_information':
                    command_uuid = special_uuid + str(device_id)
                else:
                    command_uuid = str(uuid.uuid4())
                data['attributes']['command_uuid'] = command_uuid
                print 'sending data as ', json.dumps(data)
                # print 'sending gcm command to device'
                print reg_id, data
                response = gcm.json_request(reg_id, data)
                print '\n \n response is \n', response
                if 'errors' in response:
                    for error, reg_ids in response['errors'].items():
                        if error == 'MalformedJson':
                            self.log.e(TAG, error)
                        elif error == 'Connection':
                            self.log.e(TAG, error)
                        elif error == 'Authentication':
                            self.log.e(TAG, error)
                        elif error == 'TooManyRegIds':
                            self.log.e(TAG, error)
                        elif error == 'NoCollapseKey':
                            self.log.e(TAG, error)
                        elif error == 'InvalidTtl':
                            self.log.e(TAG, error)
                        elif error == 'MissingRegistration':
                            self.log.e(TAG, error)
                        elif error == 'NotRegistered':
                            self.log.e(TAG, error)
                        elif error == 'MessageTooBig':
                            # Divide the message in smaller dependent chunks
                            # and send it to device.
                            gcm.json_request(reg_id, data)
                            self.log.e(TAG, error)
                        elif error == 'InvalidRegistration':
                            self.log.e(TAG, error)
                        elif error == 'Unavailable':
                            self.log.e(TAG, error)
                        elif error == 'MismatchSenderId':
                            self.log.e(TAG, error)
                        else:
                            self.log.e(TAG, 'New Error Type: ' + error)
                else:
                    print response
                    samsung = SamsungCommandsDBHelper()
                    cmd = dict()
                    cmd[C.SAMSUNG_COMMANDS_TABLE_ACTION] = data.get('action')
                    cmd[C.SAMSUNG_COMMANDS_TABLE_ATTRIBUTE] = json.dumps(
                        json_dict)
                    cmd[C.SAMSUNG_COMMANDS_TABLE_DEVICE] = device_id
                    cmd[C.SAMSUNG_COMMANDS_TABLE_UUID] = command_uuid
                    status = samsung.add_command(cmd)
                    # print "\n\n command to send is \n\n", cmd
                    print "\n printing status of adding command into \
                            samung command table\n", status

#             except Exception,err:
#                 self.log.e(TAG,"Exception "+repr(err))
        else:
            self.log.e(
                TAG,
                'No details found for device id = ' +
                str(device_id))

    def get_payload(self, raw_data):
        payload = dict()
        from vendor.command_controller.android.dictionary_parser import Parser
        parser = Parser()

        applications = raw_data.get('applications')
        if applications is not None:
            payload['application'] = parser.parse_application(applications)

        hardwares = raw_data.get('hardware')
        if hardwares is not None:
            payload['hardware'] = parser.parse_hardware(hardwares)

        settings = raw_data.get('settings')
        if settings is not None:
            payload['settings'] = parser.parse_settings(settings)

        wifis = raw_data.get('wifi')
        if wifis is not None:
            payload['wifi'] = parser.parse_wifi(wifis)

        vpns = raw_data.get('vpn')
        if vpns is not None:
            payload['vpn'] = parser.parse_vpn(vpns)

        bluetooths = raw_data.get('bluetooth')
        if bluetooths is not None:
            payload['bluetooth'] = parser.parse_bluetooth(bluetooths)

        access = raw_data.get('access')
        if access is not None:
            payload['access'] = parser.parse_access(access)

        attributes = raw_data.get('data')
        if attributes is not None:
            payload['data'] = raw_data.get('data')

        return payload

if __name__ == '__main__':
    '''
    Write code to test the Android Engine.
    '''

    app = '''
    {"_id":1,
    "installed_apps":[{"id":"com.resoundspot.guitartuner.lite","android":true,"iOS":false},{"description":" AdobeÂ® ReaderÂ® is the free, trusted leader for reliably viewing and interacting with PDF documents across platforms and devices. Install the free Adobe Reader mobile app to work with PDF documents","url":"https://play.google.com/store/apps/details?id=com.adobe.reader","id":"com.adobe.reader","source":"play-store","artistName":"Adobe Systems","thumbnail":"https://lh3.ggpht.com/4ZBFqbNFwegUbsJP5Em5kSGOeNn38ldJDVaVjrzpD58ScNghajRhFBUabeY8H8RP1hc=w170","name":"Adobe Reader","android":true,"iOS":false},{"description":"Streamline your workflow with the most cutting-edge scanning technology and robust PDF rendering engine. PDF Reader- iPhone Edition allows you to make notes and organize all annotated information with","url":"https://itunes.apple.com/us/app/pdf-reader-annotate-scan-sign/id368377690?mt=8&uo=4","id":"368377690","source":"app-store","artistName":"Kdan Mobile Software LTD","thumbnail":"http://a1987.phobos.apple.com/us/r30/Purple4/v4/4f/7b/29/4f7b29e7-8098-3c3c-da0b-4b3c6fca2362/Icon.png","name":"PDF Reader – Annotate, Scan, Sign, and Take Notes","iOS":true,"android":false}],
    "removed_apps":[{"description":" How about Mixing Faces into each other and creating a brand new Face!!!","url":"https://play.google.com/store/apps/details?id=com.face.swap.face.switcher","id":"com.sec.chaton","source":"play-store","artistName":"Axhunter","thumbnail":"https://lh4.ggpht.com/Veb16rJ99pPemiQP4veiEjmrx7YqcJecYJSVVhgu_NCUXFstaiKCOWAlQcV1k8xbc5A=w170","name":"Face Switch","android":true,"iOS":false},{"description":"The original FULLY AUTOMATIC Face Swap App. Face Juggler instantly and convincingly swaps all the faces in a photo for hilarious comedy effects. We've swapped MILLIONS of faces. Can we swap yours? ","url":"https://itunes.apple.com/us/app/face-juggler-free/id482473443?mt=8&uo=4","id":"482473443","source":"app-store","artistName":"I THINK & DO LTD","thumbnail":"http://a1799.phobos.apple.com/us/r30/Purple/v4/9c/af/e9/9cafe9b3-531c-edfb-9010-e24686d62e94/Icon.png","name":"Face Juggler FREE","android":false,"iOS":true}],
    "blacklisted_apps":[{"description":"★ BUY PerfectReader Pro 2 TODAY FOR ONLY 1.99$ INSTEAD OF 6.99$ - THE NORMAL PRICE ★ PerfectReader 2 Lite is the all-new version, redesigned to be the beautiful, fast and powerful PDF Reader & Annot","url":"https://itunes.apple.com/us/app/perfectreader-2-lite-fast/id436633759?mt=8&uo=4","id":"436633759","source":"app-store","artistName":"Truong Nguyen Ngoc","thumbnail":"http://a979.phobos.apple.com/us/r30/Purple/v4/df/fe/c7/dffec7a1-8c66-ad29-bd84-09cc42e23aaa/Icon.png","name":"PerfectReader 2 Lite - Fast, Beautiful PDF Reader & Annotator","android":false,"iOS":true},{"description":" + Other Unidocs Apps +","url":"https://play.google.com/store/apps/details?id=udk.android.reader","id":"com.carexpertsindia.android","source":"play-store","artistName":"Unidocs Inc.","thumbnail":"https://lh4.ggpht.com/2UY9O6b1SqXVaxJk59ceNSUJPteOf16Gj_EHGJUYi4L2slnLsZCkv50voAym2oaHsg=w170","name":"ezPDF Reader - Multimedia PDF","android":true,"iOS":false}],"youtube_enable":{"value":true,"android":true,"iOS":true},
    "playstore_enable":{"value":true,"android":true,"iOS":true},
    "browser_settings":{"enable_autofill":true,"enable_javascript":true,"enable_cookies":true,"enable_popups":true,"force_fraud_warnings":true,"enable_http_proxy":true,"http_proxy_value":"127.0.0.1","android":true,"iOS":true},
    "enable_recording":{"value":true,"android":true,"iOS":true}}
    '''
    app_json = json.loads(app)

    wifi = '''
    { "installed_wifis": [
                    {
                        "ssid": "Atul",
                        "wifi_security": "WEP",
                        "password": "AtulDhawan",
                        "auto_join": false,
                        "hidden_network": false,
                        "android": true,
                        "iOS": true
                    },
                    {
                        "ssid": "Popli",
                        "wifi_security": "WPA",
                        "password": "abcdsadase",
                        "auto_join": false,
                        "hidden_network": false,
                        "android": true,
                        "iOS": true
                    },
                    {
                        "ssid": "HugoMindsInternal",
                        "wifi_security": "PSK",
                        "password": "!HugoMinds@Tech!",
                        "auto_join": true,
                        "hidden_network": false,
                        "android": true,
                        "iOS": true
                    }
                ]
        }

    '''
    wifi_json = json.loads(wifi)

    vpn = '''
    {
    "installed_vpns": [
        {
            "vpn_name": "Type1",
            "vpn_type": "PPTP",
            "server_address": "192.168.1.2",
            "ppp_encryption": "",
            "advanced_options": true,
            "dns_search_domains": "google.com",
            "dns_servers": "192.136.2.1",
            "forwarding_routes": "10.0.0.1/8",
            "android": true,
            "iOS": true
        },
        {
            "vpn_name": "Type2",
            "vpn_type": "L2TP/IPSecPSK",
            "server_address": "192.168.2.3",
            "l2tp_secret": "abcdef",
            "ipsec_id": "",
            "ipsec_key": "abcdef",
            "advanced_options": false,
            "dns_search_domains": "",
            "dns_servers": "",
            "forwarding_routes": "",
            "android": true,
            "iOS": true
        },
        {
            "vpn_name": "Type3",
            "vpn_type": "L2TP/IPSecRSA",
            "server_address": "10.2.36.2",
            "l2tp_secret": "abcde",
            "ipsec_user_certificate": "",
            "ipsec_ca_certificate": "",
            "ipsec_server_certificate": "",
            "advanced_options": false,
            "dns_search_domains": "",
            "dns_servers": "",
            "forwarding_routes": "",
            "android": true,
            "iOS": true
        },
        {
            "vpn_name": "Type4",
            "vpn_type": "IPSecXauthPSK",
            "server_address": "",
            "ipsec_id": "",
            "ipsec_key": "",
            "advanced_options": false,
            "dns_search_domains": "",
            "dns_servers": "",
            "forwarding_routes": "",
            "android": true,
            "iOS": true
        },
        {
            "vpn_name": "Type5",
            "vpn_type": "IPSecXauthRSA",
            "server_address": "10.56.69.98",
            "ipsec_user_certificate": "",
            "ipsec_ca_certificate": "",
            "ipsec_server_certificate": "",
            "advanced_options": true,
            "dns_search_domains": "google.com",
            "dns_servers": "192.136.2.1",
            "forwarding_routes": "10.0.0.1/8",
            "android": true,
            "iOS": true
        },
        {
            "vpn_name": "Type6",
            "vpn_type": "IPSecHybridRSA",
            "server_address": "10.23.69.58",
            "ipsec_ca_certificate": "",
            "ipsec_server_certificate": "",
            "advanced_options": true,
            "dns_search_domains": "google.com",
            "dns_servers": "192.136.2.1",
            "forwarding_routes": "10.0.0.1/8",
            "android": true,
            "iOS": true
        }
    ]
}
    '''
    vpn_json = json.loads(vpn)

    hardware = '''
    {
        "enable_camera": {
            "value": true,
            "android": true,
            "iOS": true
        },
        "enable_external_storage_encryption": {
            "value": true,
            "android": true,
            "iOS": true
        },
        "enable_internal_storage_encryption": {
            "value": true,
            "android": true,
            "iOS": true
        },
        "enable_microphone": {
            "value": true,
            "android": true,
            "iOS": true
        },
        "enable_android_beam": {
            "value": true,
            "android": true,
            "iOS": true
        }
    }
    '''
    hardware_json = json.loads(hardware)

    settings = '''
    {
    "enable_background_data": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_backup": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_clipboard": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_google_crash_report": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_data_roaming": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_push_roaming": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_sync_roaming": {
        "value": true,
        "android": true,
        "iOS": true
    },
    "enable_voice_calls_roaming": {
        "value": true,
        "android": true,
        "iOS": true
    },

    "enable_wifi":{
        "value": true,
        "android": true,
        "iOS" : true
    }
}
    '''
    settings_json = json.loads(settings)

    bluetooth = '''
    {
   "bluetooth_status": {
      "enable_bluetooth": true,
      "power_status": true,
      "android": true,
      "iOS": true
   },
   "white_listed_pairings": [
      {
         "bluetooth_name": "ravi",
         "bluetooth_cod": 1,
         "bluetooth_uuid": "00001101-0000-1000-8000-00805f9b34fb",
         "bluetooth_pairing": true,
         "android": true,
         "iOS": true
      },
      {
         "bluetooth_name": "popli",
         "bluetooth_cod": 3,
         "bluetooth_uuid": "00001101-0000-1000-8000-00805f9b34f9",
         "bluetooth_pairing": true,
         "android": true,
         "iOS": true
      },
      {
         "bluetooth_name": "aman",
         "bluetooth_cod": 5,
         "bluetooth_uuid": "00001101-0000-1000-8000-00805f9b34fd",
         "bluetooth_pairing": true,
         "android": true,
         "iOS": true
      }
   ],
   "black_listed_pairings": [
      {
         "bluetooth_name": "jkjdg",
         "bluetooth_cod": 3,
         "bluetooth_uuid": "00001101-0000-1000-8000-00805f9b34fc",
         "bluetooth_pairing": true,
         "android": true,
         "iOS": true
      }
   ]
}
    '''
    bluetooth_json = json.loads(bluetooth)

    access = '''
    {
        "change_settings_enable": {
            "value": false,
            "android": true,
            "iOS": true
        },
        "capture_screen_enable": {
            "value": true,
            "android": true,
            "iOS": true
        },
        "enable_factory_reset": {
            "value": false,
            "android": true,
            "iOS": true
        },
        "enable_usb_debugging": {
            "value": true,
            "android": true,
            "iOS": true
        },
        "enable_admin_mode": {
            "value": true,
            "andgroid": true,
            "iOS": true
        }
    }
    '''
    access_json = json.loads(access)

    eng = AndroidCommand()
    json_dict = dict()
    json_dict['action'] = 'notification'
    json_dict['data'] = 'Good morning company!'
#     json_dict['application']= app_json
#     json_dict['wifi']= wifi_json
#     json_dict['vpn']= vpn_json
#     json_dict['hardware']= hardware_json
#     json_dict['settings']=settings_json
#     json_dict['bluetooth']= bluetooth_json
#     json_dict['access']= access_json
    # print json.dumps(json_dict)
    eng.execute(json_dict, 1)
