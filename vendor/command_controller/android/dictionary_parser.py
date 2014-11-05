# -*- coding: utf-8 -*-
import json
import copy
#import ipdb


class Parser(object):

    def parse_application(self, application):
        '''
        Parses the application dictionary returns another dictionary that only
        has the parameters required by the device to execute the commands.
        '''
        result = dict()

        # Installed Apps
        installed_apps = application.get('installed_apps')
        result['installed_apps'] = list()
        if installed_apps is not None:
            for installed_app in installed_apps:
                if 'android' in installed_app and installed_app['android']:
                    result['installed_apps'].append(
                        {'id': installed_app['id']})

        # Removed apps
        removed_apps = application.get('removed_apps')
        result['removed_apps'] = list()
        if removed_apps is not None:
            for removed_app in removed_apps:
                if 'android' in removed_app and removed_app['android']:
                    result['removed_apps'].append({'id': removed_app['id']})

        # Blacklisted apps
        blacklisted_apps = application.get('blacklisted_apps')
        result['blacklisted_apps'] = list()
        if blacklisted_apps is not None:
            for blacklisted_app in blacklisted_apps:
                if 'android' in blacklisted_app and blacklisted_app['android']:
                    result['blacklisted_apps'].append(
                        {'id': blacklisted_app['id']})
        # Now a generic loop to find all other things mentioned.
        for item in application:
            # ignore the ones which are list... Just go through the dicts
            if isinstance(application[item], dict):
                if 'android' in application[
                        item] and application[item]['android']:
                    result[item] = application[item]
                    del result[item]['android']
                    del result[item]['iOS']
        return result

    def parse_hardware(self, hardware):
        result = dict()
        for item in hardware:
            # ignore the ones which are list... Just go through the dicts
            if isinstance(hardware[item], dict):
                if 'android' in hardware[item] and hardware[item]['android']:
                    result[item] = hardware[item]
                    del hardware[item]['android']
                    del hardware[item]['iOS']
        return result

    def parse_settings(self, settings):
        result = dict()
        for item in settings:
            if isinstance(settings[item], dict):
                if 'android' in settings[item] and settings[item]['android']:
                    result[item] = settings[item]
                    del settings[item]['android']
                    del settings[item]['iOS']
        return result

    def parse_wifi(self, wifis):
        result = copy.deepcopy(wifis)
        if isinstance(result, dict) and 'installed_wifis' in result:
            for wifi in result['installed_wifis']:
                if 'android' in wifi and 'iOS' in wifi:
                    del wifi['android']
                    del wifi['iOS']
            return result

    def parse_vpn(self, vpns):
        result = copy.deepcopy(vpns)
        if isinstance(result, dict) and 'installed_vpns' in vpns:
            for vpn in result['installed_vpns']:
                if 'android' in vpn and 'iOS' in vpn:
                    del vpn['android']
                    del vpn['iOS']
            return result

    def parse_bluetooth(self, bluetooth):
        if bluetooth is not None:
            # ipdb.set_trace()
            if ('bluetooth_status' in bluetooth
                    and 'android' in bluetooth['bluetooth_status']
                    and 'iOS' in bluetooth['bluetooth_status']):
                del bluetooth['bluetooth_status']['android']
                del bluetooth['bluetooth_status']['iOS']
            if 'white_listed_pairings' in bluetooth:
                for pairing in bluetooth['white_listed_pairings']:
                    if 'android' in pairing and 'iOS' in pairing:
                        del pairing['android']
                        del pairing['iOS']
            if 'black_listed_pairings' in bluetooth:
                for pairing in bluetooth['black_listed_pairings']:
                    if 'android' in pairing and 'iOS' in pairing:
                        del pairing['android']
                        del pairing['iOS']
        return bluetooth

    def parse_access(self, access):
        if isinstance(access, dict):
            for item in access:
                if (isinstance(access[item], dict)
                        and 'android' in access[item]
                        and 'iOS' in access[item]):
                    del access[item]['android']
                    del access[item]['iOS']
        return access


if __name__ == "__main__":

    j = '''
    {"_id":1,"installed_apps":[{"description":" AdobeÂ® ReaderÂ® is the free, trusted leader for reliably viewing and interacting with PDF documents across platforms and devices. Install the free Adobe Reader mobile app to work with PDF documents","url":"https://play.google.com/store/apps/details?id=com.adobe.reader","id":"com.adobe.reader","source":"play-store","artistName":"Adobe Systems","thumbnail":"https://lh3.ggpht.com/4ZBFqbNFwegUbsJP5Em5kSGOeNn38ldJDVaVjrzpD58ScNghajRhFBUabeY8H8RP1hc=w170","name":"Adobe Reader","android":true,"iOS":false},{"description":"Streamline your workflow with the most cutting-edge scanning technology and robust PDF rendering engine. PDF Reader- iPhone Edition allows you to make notes and organize all annotated information with","url":"https://itunes.apple.com/us/app/pdf-reader-annotate-scan-sign/id368377690?mt=8&uo=4","id":"368377690","source":"app-store","artistName":"Kdan Mobile Software LTD","thumbnail":"http://a1987.phobos.apple.com/us/r30/Purple4/v4/4f/7b/29/4f7b29e7-8098-3c3c-da0b-4b3c6fca2362/Icon.png","name":"PDF Reader – Annotate, Scan, Sign, and Take Notes","iOS":true,"android":false}],"removed_apps":[{"description":" How about Mixing Faces into each other and creating a brand new Face!!!","url":"https://play.google.com/store/apps/details?id=com.face.swap.face.switcher","id":"com.face.swap.face.switcher","source":"play-store","artistName":"Axhunter","thumbnail":"https://lh4.ggpht.com/Veb16rJ99pPemiQP4veiEjmrx7YqcJecYJSVVhgu_NCUXFstaiKCOWAlQcV1k8xbc5A=w170","name":"Face Switch","android":true,"iOS":false},{"description":"The original FULLY AUTOMATIC Face Swap App. Face Juggler instantly and convincingly swaps all the faces in a photo for hilarious comedy effects. We've swapped MILLIONS of faces. Can we swap yours? ","url":"https://itunes.apple.com/us/app/face-juggler-free/id482473443?mt=8&uo=4","id":"482473443","source":"app-store","artistName":"I THINK & DO LTD","thumbnail":"http://a1799.phobos.apple.com/us/r30/Purple/v4/9c/af/e9/9cafe9b3-531c-edfb-9010-e24686d62e94/Icon.png","name":"Face Juggler FREE","android":false,"iOS":true}],"blacklisted_apps":[{"description":"★ BUY PerfectReader Pro 2 TODAY FOR ONLY 1.99$ INSTEAD OF 6.99$ - THE NORMAL PRICE ★ PerfectReader 2 Lite is the all-new version, redesigned to be the beautiful, fast and powerful PDF Reader & Annot","url":"https://itunes.apple.com/us/app/perfectreader-2-lite-fast/id436633759?mt=8&uo=4","id":"436633759","source":"app-store","artistName":"Truong Nguyen Ngoc","thumbnail":"http://a979.phobos.apple.com/us/r30/Purple/v4/df/fe/c7/dffec7a1-8c66-ad29-bd84-09cc42e23aaa/Icon.png","name":"PerfectReader 2 Lite - Fast, Beautiful PDF Reader & Annotator","android":false,"iOS":true},{"description":" + Other Unidocs Apps +","url":"https://play.google.com/store/apps/details?id=udk.android.reader","id":"udk.android.reader","source":"play-store","artistName":"Unidocs Inc.","thumbnail":"https://lh4.ggpht.com/2UY9O6b1SqXVaxJk59ceNSUJPteOf16Gj_EHGJUYi4L2slnLsZCkv50voAym2oaHsg=w170","name":"ezPDF Reader - Multimedia PDF","android":true,"iOS":false}],"youtube_enable":{"value":true,"android":true,"iOS":true},"playstore_enable":{"value":true,"android":true,"iOS":true},"browser_settings":{"disable_autofill":false,"disable_javascript":false,"disable_cookies":false,"disable_popups":true,"do_not_force_fraud_warnings":false,"enable_http_proxy":false,"http_proxy_value":"127.0.0.1","android":true,"iOS":true},"enable_recording":{"value":false,"android":true,"iOS":true}}
    '''
    d = json.loads(j)
    print Parser().parse_application(d)
