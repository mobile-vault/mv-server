import base64
import threading
# import uuid
from logger import Logger


# try:
#    import xml.etree.cElementTree as ET
# except ImportError:
#    import xml.etree.ElementTree as ET
from lxml import etree
from lxml import etree as ET

someDefaultEmail = 'abc@xyz.com'


class PolicyCreater(threading.Thread):
    profile = 'finalProfile'
    useSafari = True
    log = 'log'

    def __init__(self, json_array):
        threading.Thread.__init__(self)
        print 'IN PolicyCreater\'s init'

        self.json_array = json_array

    def run(self):
        self.log = Logger('PolicyCreater')
        print 'PolicyCreater'
        print self.json_array
        tag = 'run'
        self.profile = ET.Element('plist')
        self.profile.attrib['version'] = '1.0'

        rootDict = ET.SubElement(self.profile, 'dict')

        rootPayloadKey = ET.SubElement(rootDict, "key")
        rootPayloadKey.text = 'PayloadContent'

        arrayPayload = ET.SubElement(rootDict, 'array')
        payload_name_str = 'Sample Test profile'
        payload_identifier_str = 'com.toppatch.SampleTestProfile'
        payload_uuid_str = 'ED66B03F-99E3-4419-BA7F-F896B7F3AA38775'

        #### condition for restrictions and XML creation######
        for policy in self.json_array:
            if policy['type'] == 'restrictions':
                print 'Restrictions Found'
                restrictionDict = policy['data']
                dictSetting = ET.SubElement(arrayPayload, 'dict')

                descriptionKey = ET.SubElement(dictSetting, 'key')
                descriptionKey.text = 'PayloadDescription'
                descriptionString = ET.SubElement(dictSetting, 'string')
                descriptionString.text = 'Configures device restrictions.'

                payloadName = ET.SubElement(dictSetting, 'key')
                payloadName.text = 'PayloadDisplayName'
                payloadNameString = ET.SubElement(dictSetting, 'string')
                payloadNameString.text = 'Restrictions'

                payloadIdentifier = ET.SubElement(dictSetting, 'key')
                payloadIdentifier.text = 'PayloadIdentifier'
                payloadIdentifierString = ET.SubElement(dictSetting, 'string')
                payloadIdentifierString.text = (
                    'com.toppatch.testProfile.restrictions')

                payloadOrg = ET.SubElement(dictSetting, 'key')
                payloadOrg.text = 'PayloadOrganization'
                payloadOrgString = ET.SubElement(dictSetting, 'string')
                payloadOrgString.text = 'Toppatch'

                payloadType = ET.SubElement(dictSetting, 'key')
                payloadType.text = 'PayloadType'
                payloadTypeString = ET.SubElement(dictSetting, 'string')
                payloadTypeString.text = 'com.apple.applicationaccess'

                payloadUUID = ET.SubElement(dictSetting, 'key')
                payloadUUID.text = 'PayloadUUID'
                payloadUUIDString = ET.SubElement(dictSetting, 'string')
                payloadUUIDString.text = '2FB2EC1B-4230-4CCF-AEE6-77598A5E16E9'

                payloadVersion = ET.SubElement(dictSetting, 'key')
                payloadVersion.text = 'PayloadVersion'
                payloadVersionString = ET.SubElement(dictSetting, 'integer')
                payloadVersionString.text = str(1)

                allowGameCenter = ET.SubElement(dictSetting, 'key')
                allowGameCenter.text = 'allowAddingGameCenterFriends'
                if 'allowAddingGameCenterFriends' in restrictionDict:
                    allowGameCenterValue = ET.SubElement(dictSetting, str(
                        restrictionDict['allowAddingGameCenterFriends']).lower(
                        ))
                else:
                    allowGameCenterValue = ET.SubElement(dictSetting, 'true')

                allowAppInstall = ET.SubElement(dictSetting, 'key')
                allowAppInstall.text = 'allowAppInstallation'
                if 'allowAppInstallation' in restrictionDict:
                    allowAppInstallValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowAppInstallation']).lower())
                else:
                    allowAppInstallValue = ET.SubElement(dictSetting, 'true')

                allowAssistant = ET.SubElement(dictSetting, 'key')
                allowAssistant.text = 'allowAssistant'
                if 'allowAssistant' in restrictionDict:
                    allowAssistantValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowAssistant']).lower())
                else:
                    allowAssistantValue = ET.SubElement(dictSetting, 'true')

                allowAssistantWhileLocked = ET.SubElement(dictSetting, 'key')
                allowAssistantWhileLocked.text = 'allowAssistantWhileLocked'
                if 'allowAssistantWhileLocked' in restrictionDict:
                    allowAssistantWhileLockedValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowAssistantWhileLocked']).lower())
                else:
                    allowAssistantWhileLockedValue = ET.SubElement(
                        dictSetting,
                        'true')

                allowCamera = ET.SubElement(dictSetting, 'key')
                allowCamera.text = 'allowCamera'
                if 'allowCamera' in restrictionDict:
                    allowCameraValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowCamera']).lower())
                else:
                    allowCameraValue = ET.SubElement(dictSetting, 'true')

                allowCloudBackup = ET.SubElement(dictSetting, 'key')
                allowCloudBackup.text = 'allowCloudBackup'
                if 'allowCloudBackup' in restrictionDict:
                    allowCloudBackupValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowCloudBackup']).lower())
                else:
                    allowCloudBackupValue = ET.SubElement(dictSetting, 'true')

                allowDocSync = ET.SubElement(dictSetting, 'key')
                allowDocSync.text = 'allowCloudDocumentSync'
                if 'allowCloudDocumentSync' in restrictionDict:
                    allowDocSyncValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowCloudDocumentSync']).lower())
                else:
                    allowDocSyncValue = ET.SubElement(dictSetting, 'true')

                allowDiagnostic = ET.SubElement(dictSetting, 'key')
                allowDiagnostic.text = 'allowDiagnosticSubmission'
                if 'allowDiagnosticSubmission' in restrictionDict:
                    allowDiagnosticValue = ET.SubElement(dictSetting, str(
                        restrictionDict['allowDiagnosticSubmission']).lower())
                else:
                    allowDiagnosticValue = ET.SubElement(dictSetting, 'true')

                allowExplicit = ET.SubElement(dictSetting, 'key')
                allowExplicit.text = 'allowExplicitContent'
                if 'allowExplicitContent' in restrictionDict:
                    allowExplicitValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowExplicitContent']).lower())
                else:
                    allowExplicitValue = ET.SubElement(dictSetting, 'true')

                allowGlobalBckground = ET.SubElement(dictSetting, 'key')
                allowGlobalBckground.text = (
                    'allowGlobalBackgroundFetchWhenRoaming')
                if 'allowGlobalBackgroundFetchWhenRoaming' in restrictionDict:
                    allowGlobalBckgroundValue = ET.SubElement(dictSetting, str(
                        restrictionDict['allowGlobalBackgroundFetchWhenRoaming']).lower())
                else:
                    allowGlobalBckgroundValue = ET.SubElement(
                        dictSetting,
                        'true')

                allowInAppPurchase = ET.SubElement(dictSetting, 'key')
                allowInAppPurchase.text = 'allowInAppPurchases'
                if 'allowInAppPurchases' in restrictionDict:
                    allowInAppPurchaseValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowInAppPurchases']).lower())
                else:
                    allowInAppPurchaseValue = ET.SubElement(
                        dictSetting,
                        'true')

                allowMultiplayer = ET.SubElement(dictSetting, 'key')
                allowMultiplayer.text = 'allowMultiplayerGaming'
                if 'allowMultiplayerGaming' in restrictionDict:
                    allowMultiplayerValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowMultiplayerGaming']).lower())
                else:
                    allowMultiplayerValue = ET.SubElement(dictSetting, 'true')

                allowPhotoStream = ET.SubElement(dictSetting, 'key')
                allowPhotoStream.text = 'allowPhotoStream'
                if 'allowPhotoStream' in restrictionDict:
                    allowPhotoStreamValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowPhotoStream']).lower())
                else:
                    allowPhotoStreamValue = ET.SubElement(dictSetting, 'true')

                allowSafari = ET.SubElement(dictSetting, 'key')
                allowSafari.text = 'allowSafari'
                if 'allowSafari' in restrictionDict:
                    allowSafariValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowSafari']).lower())
                    if str(restrictionDict['allowSafari']).lower() == 'false':
                        self.useSafari = False
                    else:
                        self.useSafari = True
                else:
                    allowSafariValue = ET.SubElement(dictSetting, 'true')

                allowScreenshot = ET.SubElement(dictSetting, 'key')
                allowScreenshot.text = 'allowScreenShot'
                if 'allowScreenShot' in restrictionDict:
                    allowScreenshotValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowScreenShot']).lower())
                else:
                    allowScreenshotValue = ET.SubElement(dictSetting, 'true')

                allowUntrustedTLS = ET.SubElement(dictSetting, 'key')
                allowUntrustedTLS.text = 'allowUntrustedTLSPrompt'
                if 'allowUntrustedTLSPrompt' in restrictionDict:
                    allowUntrustedTLSValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowUntrustedTLSPrompt']).lower())
                else:
                    allowUntrustedTLSValue = ET.SubElement(dictSetting, 'true')

                allowVideoConf = ET.SubElement(dictSetting, 'key')
                allowVideoConf.text = 'allowVideoConferencing'
                if 'allowVideoConferencing' in restrictionDict:
                    allowVideoConfValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowVideoConferencing']).lower())
                else:
                    allowVideoConfValue = ET.SubElement(dictSetting, 'true')

                allowVoiceDial = ET.SubElement(dictSetting, 'key')
                allowVoiceDial.text = 'allowVoiceDialing'
                if 'allowVoiceDialing' in restrictionDict:
                    allowVoiceDialValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowVoiceDialing']).lower())
                else:
                    allowVoiceDialValue = ET.SubElement(dictSetting, 'true')

                allowYoutube = ET.SubElement(dictSetting, 'key')
                allowYoutube.text = 'allowYouTube'
                if 'allowYouTube' in restrictionDict:
                    allowYoutubeValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowYouTube']).lower())
                else:
                    allowYoutubeValue = ET.SubElement(dictSetting, 'true')

                allowiTunes = ET.SubElement(dictSetting, 'key')
                allowiTunes.text = 'allowiTunes'
                if 'allowiTunes' in restrictionDict:
                    allowiTunesValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['allowiTunes']).lower())
                else:
                    allowiTunesValue = ET.SubElement(dictSetting, 'true')

                allowForceEncrypt = ET.SubElement(dictSetting, 'key')
                allowForceEncrypt.text = 'forceEncryptedBackup'
                if 'forceEncryptedBackup' in restrictionDict:
                    allowForceEncryptValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['forceEncryptedBackup']).lower())
                else:
                    allowForceEncryptValue = ET.SubElement(dictSetting, 'true')

                allowForceiTunePass = ET.SubElement(dictSetting, 'key')
                allowForceiTunePass.text = 'forceITunesStorePasswordEntry'
                if 'forceITunesStorePasswordEntry' in restrictionDict:
                    allowForceiTunePassValue = ET.SubElement(
                        dictSetting, str(
                            restrictionDict['forceITunesStorePasswordEntry']).lower())
                else:
                    allowForceiTunePassValue = ET.SubElement(
                        dictSetting,
                        'true')

                rateApp = ET.SubElement(dictSetting, 'key')
                rateApp.text = 'ratingApps'
                rateAppString = ET.SubElement(dictSetting, 'integer')
                rateAppString.text = str(1000)

                rateMovies = ET.SubElement(dictSetting, 'key')
                rateMovies.text = 'ratingMovies'
                rateMoviesString = ET.SubElement(dictSetting, 'integer')
                rateMoviesString.text = str(1000)

                rateRegion = ET.SubElement(dictSetting, 'key')
                rateRegion.text = 'ratingRegion'
                rateRegionString = ET.SubElement(dictSetting, 'string')
                rateRegionString.text = 'us'

                rateTVShows = ET.SubElement(dictSetting, 'key')
                rateTVShows.text = 'ratingTVShows'
                rateTVShowsString = ET.SubElement(dictSetting, 'integer')
                rateTVShowsString.text = str(1000)

                if self.useSafari:
                    safariAcceptCookie = ET.SubElement(dictSetting, 'key')
                    safariAcceptCookie.text = 'safariAcceptCookies'
                    safariAcceptCookieString = ET.SubElement(
                        dictSetting,
                        'integer')
                    if 'safariAcceptCookies' in restrictionDict:
                        safariAcceptCookieString.text = str(
                            restrictionDict['safariAcceptCookies'])
                    else:
                        safariAcceptCookieString.text = str(2)

                    allowAutoFill = ET.SubElement(dictSetting, 'key')
                    allowAutoFill.text = 'safariAllowAutoFill'
                    if 'safariAllowAutoFill' in restrictionDict:
                        allowAutoFillValue = ET.SubElement(
                            dictSetting, str(
                                restrictionDict['safariAllowAutoFill']).lower())
                    else:
                        allowAutoFillValue = ET.SubElement(dictSetting, 'true')

                    allowJS = ET.SubElement(dictSetting, 'key')
                    allowJS.text = 'safariAllowJavaScript'
                    if 'safariAllowJavaScript' in restrictionDict:
                        allowJSValue = ET.SubElement(
                            dictSetting, str(
                                restrictionDict['safariAllowJavaScript']).lower())
                    else:
                        allowJSValue = ET.SubElement(dictSetting, 'true')

                    allowPopUps = ET.SubElement(dictSetting, 'key')
                    allowPopUps.text = 'safariAllowPopups'
                    if 'safariAllowPopups' in restrictionDict:
                        allowPopUpsValue = ET.SubElement(
                            dictSetting, str(
                                restrictionDict['safariAllowPopups']).lower())
                    else:
                        allowPopUpsValue = ET.SubElement(dictSetting, 'true')

                    allowFraudWarn = ET.SubElement(dictSetting, 'key')
                    allowFraudWarn.text = 'safariForceFraudWarning'
                    if 'safariForceFraudWarning' in restrictionDict:
                        allowFraudWarnValue = ET.SubElement(
                            dictSetting, str(
                                restrictionDict['safariForceFraudWarning']).lower())
                    else:
                        allowFraudWarnValue = ET.SubElement(
                            dictSetting,
                            'false')

        #### condition for passcode and XML creation######
#         if self.json_dict.has_key('passcode'):
            if policy['type'] == 'passcode':
                print 'innnnnnnnnnnnnnnnn passcode'
                passcodeDict = policy['data']

                dictSetting = ET.SubElement(arrayPayload, 'dict')

                descriptionKey = ET.SubElement(dictSetting, 'key')
                descriptionKey.text = 'PayloadDescription'
                descriptionString = ET.SubElement(dictSetting, 'string')
                descriptionString.text = 'Configures security-related items.'

                payloadName = ET.SubElement(dictSetting, 'key')
                payloadName.text = 'PayloadDisplayName'
                payloadNameString = ET.SubElement(dictSetting, 'string')
                payloadNameString.text = 'Passcode'

                payloadIdentifier = ET.SubElement(dictSetting, 'key')
                payloadIdentifier.text = 'PayloadIdentifier'
                payloadIdentifierString = ET.SubElement(dictSetting, 'string')
                payloadIdentifierString.text = 'com.toppatch.testProfile.passcodepolicy'

                payloadOrg = ET.SubElement(dictSetting, 'key')
                payloadOrg.text = 'PayloadOrganization'
                payloadOrgString = ET.SubElement(dictSetting, 'string')
                payloadOrgString.text = 'Toppatch'

                payloadType = ET.SubElement(dictSetting, 'key')
                payloadType.text = 'PayloadType'
                payloadTypeString = ET.SubElement(dictSetting, 'string')
                payloadTypeString.text = 'com.apple.mobiledevice.passwordpolicy'

                payloadUUID = ET.SubElement(dictSetting, 'key')
                payloadUUID.text = 'PayloadUUID'
                payloadUUIDString = ET.SubElement(dictSetting, 'string')
                payloadUUIDString.text = 'C7E14171-F4D6-414B-BBEA-F1472031740D'

                payloadVersion = ET.SubElement(dictSetting, 'key')
                payloadVersion.text = 'PayloadVersion'
                payloadVersionString = ET.SubElement(dictSetting, 'integer')
                payloadVersionString.text = str(1)

                if 'allowSimple' in passcodeDict:
                    allowSimple = ET.SubElement(dictSetting, 'key')
                    allowSimple.text = 'allowSimple'
                    allowSimpleValue = ET.SubElement(
                        dictSetting, str(
                            passcodeDict['allowSimple']).lower())
                else:
                    allowSimpleValue = ET.SubElement(dictSetting, 'true')

                    forcePIN = ET.SubElement(dictSetting, 'key')
                    forcePIN.text = 'forcePIN'
                    forcePINValue = ET.SubElement(dictSetting, 'true')

                if 'maxFailedAttempts' in passcodeDict:
                    maxFailedAttempts = ET.SubElement(dictSetting, 'key')
                    maxFailedAttempts.text = 'maxFailedAttempts'
                    maxFailedAttemptsString = ET.SubElement(
                        dictSetting,
                        'integer')
                    maxFailedAttemptsString.text = str(
                        passcodeDict['maxFailedAttempts'])

                if 'maxGracePeriod' in passcodeDict:
                    maxGracePeriod = ET.SubElement(dictSetting, 'key')
                    maxGracePeriod.text = 'maxGracePeriod'
                    maxGracePeriodString = ET.SubElement(
                        dictSetting,
                        'integer')
                    maxGracePeriodString.text = str(
                        passcodeDict['maxGracePeriod'])

                if 'maxInactivity' in passcodeDict:
                    maxInactivity = ET.SubElement(dictSetting, 'key')
                    maxInactivity.text = 'maxInactivity'
                    maxInactivityString = ET.SubElement(dictSetting, 'integer')
                    maxInactivityString.text = str(
                        passcodeDict['maxInactivity'])

                if 'maxPINAgeInDays' in passcodeDict:
                    maxPINAgeInDays = ET.SubElement(dictSetting, 'key')
                    maxPINAgeInDays.text = 'maxPINAgeInDays'
                    maxPINAgeInDaysString = ET.SubElement(
                        dictSetting,
                        'integer')
                    maxPINAgeInDaysString.text = str(
                        passcodeDict['maxPINAgeInDays'])

                if 'minComplexChars' in passcodeDict:
                    minComplexChars = ET.SubElement(dictSetting, 'key')
                    minComplexChars.text = 'minComplexChars'
                    minComplexCharsString = ET.SubElement(
                        dictSetting,
                        'integer')
                    minComplexCharsString.text = str(
                        passcodeDict['minComplexChars'])

                if 'minLength' in passcodeDict:
                    minLength = ET.SubElement(dictSetting, 'key')
                    minLength.text = 'minLength'
                    minLengthString = ET.SubElement(dictSetting, 'integer')
                    minLengthString.text = str(passcodeDict['minLength'])

                if 'pinHistory' in passcodeDict:
                    pinHistory = ET.SubElement(dictSetting, 'key')
                    pinHistory.text = 'pinHistory'
                    pinHistoryString = ET.SubElement(dictSetting, 'integer')
                    pinHistoryString.text = str(passcodeDict['pinHistory'])

                requireAlphanumeric = ET.SubElement(dictSetting, 'key')
                requireAlphanumeric.text = 'requireAlphanumeric'
                if 'requireAlphanumeric' in passcodeDict:
                    requireAlphanumericString = ET.SubElement(
                        dictSetting, str(
                            passcodeDict['requireAlphanumeric']).lower())
                else:
                    requireAlphanumericString = ET.SubElement(
                        dictSetting,
                        'true')

        #### condition for exchangeAccount and XML creation######
#         if self.json_dict.has_key('exchangeAccount'):
            if policy['type'] == 'exchangeAccount':
                print 'exchangeAccount Found'
                eaDict = policy['data']

                dictSetting = ET.SubElement(arrayPayload, 'dict')

                emailAddress = ET.SubElement(dictSetting, 'key')
                emailAddress.text = 'EmailAddress'
                emailAddressString = ET.SubElement(dictSetting, 'string')
                if 'EmailAddress' in eaDict:
                    emailAddressString.text = str(eaDict['EmailAddress'])
                else:
                    emailAddressString.text = someDefaultEmail
                    self.log.e(
                        tag,
                        'Email Address not sent in EmailField of Exachange Account')

                Host = ET.SubElement(dictSetting, 'key')
                Host.text = 'Host'
                HostString = ET.SubElement(dictSetting, 'string')
                if 'Host' in eaDict:
                    emailAddressString.text = str(eaDict['Host'])
                else:
                    HostString.text = someDefaultEmail
                    self.log.e(
                        tag,
                        'Host not sent in Host of Exachange Account')

                MailNumberOfPastDaysToSync = ET.SubElement(dictSetting, 'key')
                MailNumberOfPastDaysToSync.text = 'MailNumberOfPastDaysToSync'
                MailNumberOfPastDaysToSyncString = ET.SubElement(
                    dictSetting,
                    'integer')
                if 'MailNumberOfPastDaysToSync' in eaDict:
                    emailAddressString.text = str(
                        eaDict['MailNumberOfPastDaysToSync'])
                else:
                    MailNumberOfPastDaysToSyncString.text = str(0)

                Password = ET.SubElement(dictSetting, 'key')
                Password.text = 'Password'
                PasswordString = ET.SubElement(dictSetting, 'string')
                if 'Password' in eaDict:
                    emailAddressString.text = str(eaDict['Password'])
                else:
                    PasswordString.text = ''
                    self.log.e(
                        tag,
                        'Password not sent in Host of Exachange Account')

                descriptionKey = ET.SubElement(dictSetting, 'key')
                descriptionKey.text = 'PayloadDescription'
                descriptionString = ET.SubElement(dictSetting, 'string')
                descriptionString.text = 'Configures device for use with Microsoft Exchange ActiveSync services.'

                payloadName = ET.SubElement(dictSetting, 'key')
                payloadName.text = 'PayloadDisplayName'
                payloadNameString = ET.SubElement(dictSetting, 'string')
                if 'PayloadDisplayName' in eaDict:
                    payloadNameString.text = str(eaDict['PayloadDisplayName'])
                else:
                    payloadNameString.text = 'Exchange EAS Account'

                payloadIdentifier = ET.SubElement(dictSetting, 'key')
                payloadIdentifier.text = 'PayloadIdentifier'
                payloadIdentifierString = ET.SubElement(dictSetting, 'string')
                payloadIdentifierString.text = 'com.toppatch.testProfile.eas'

                payloadOrg = ET.SubElement(dictSetting, 'key')
                payloadOrg.text = 'PayloadOrganization'
                payloadOrgString = ET.SubElement(dictSetting, 'string')
                payloadOrgString.text = 'Toppatch'

                payloadType = ET.SubElement(dictSetting, 'key')
                payloadType.text = 'PayloadType'
                payloadTypeString = ET.SubElement(dictSetting, 'string')
                payloadTypeString.text = 'com.apple.eas.account'

                payloadUUID = ET.SubElement(dictSetting, 'key')
                payloadUUID.text = 'PayloadUUID'
                payloadUUIDString = ET.SubElement(dictSetting, 'string')
                payloadUUIDString.text = 'BD82568C-18E0-4D38-A500-56DDF8E08A08'

                payloadVersion = ET.SubElement(dictSetting, 'key')
                payloadVersion.text = 'PayloadVersion'
                payloadVersionString = ET.SubElement(dictSetting, 'integer')
                payloadVersionString.text = str(1)

                PreventAppSheet = ET.SubElement(dictSetting, 'key')
                PreventAppSheet.text = 'PreventAppSheet'
                if 'PreventAppSheet' in eaDict:
                    PreventAppSheetString = ET.SubElement(
                        dictSetting, str(
                            eaDict['PreventAppSheet']).lower())
                else:
                    PreventAppSheetString = ET.SubElement(dictSetting, 'true')

                PreventMove = ET.SubElement(dictSetting, 'key')
                PreventMove.text = 'PreventMove'
                if 'PreventMove' in eaDict:
                    PreventMoveString = ET.SubElement(
                        dictSetting, str(
                            eaDict['PreventMove']).lower())
                else:
                    PreventMoveString = ET.SubElement(dictSetting, 'true')

                SMIMEEnabled = ET.SubElement(dictSetting, 'key')
                SMIMEEnabled.text = 'SMIMEEnabled'
                if 'SMIMEEnabled' in eaDict:
                    SMIMEEnabledString = ET.SubElement(
                        dictSetting, str(
                            eaDict['SMIMEEnabled']).lower())
                else:
                    SMIMEEnabledString = ET.SubElement(dictSetting, 'true')

                UserName = ET.SubElement(dictSetting, 'key')
                UserName.text = 'UserName'
                UserNameString = ET.SubElement(dictSetting, 'string')
                if 'UserName' in eaDict:
                    UserNameString.text = ET.SubElement(
                        dictSetting,
                        eaDict['UserName'])
                else:
                    UserNameString.text = 'NO NAME'

        #### condition for webClip and XML creation######
#         if self.json_dict.has_key('webClip'):
            if policy['type'] == 'webClip':
                print 'Web Clip found'
                webClipDict = policy['data']
                dictSetting = ET.SubElement(arrayPayload, 'dict')

                FullScreen = ET.SubElement(dictSetting, 'key')
                FullScreen.text = 'FullScreen'
                if 'FullScreen' in webClipDict:
                    FullScreenValue = ET.SubElement(
                        dictSetting, str(
                            webClipDict['FullScreen']).lower())
                else:
                    FullScreenValue = ET.SubElement(dictSetting, 'true')

                FullScreen = ET.SubElement(dictSetting, 'key')
                FullScreen.text = 'FullScreen'
                if 'FullScreen' in webClipDict:
                    FullScreenValue = ET.SubElement(
                        dictSetting, str(
                            webClipDict['FullScreen']).lower())
                else:
                    FullScreenValue = ET.SubElement(dictSetting, 'true')

                if 'Icon' in webClipDict:
                    Icon = ET.SubElement(dictSetting, 'key')
                    Icon.text = 'Icon'
                    iconSentData = webClipDict['Icon']
                    encodedIcon = base64.b64encode(iconSentData)

                    IconData = ET.SubElement(dictSetting, 'data')
                    IconData.text = encodedIcon

                IsRemovable = ET.SubElement(dictSetting, 'key')
                IsRemovable.text = 'IsRemovable'

                if 'IsRemovable' in webClipDict:
                    IsRemovableValue = ET.SubElement(
                        dictSetting, str(
                            webClipDict['IsRemovable']).lower())
                else:
                    IsRemovableValue = ET.SubElement(dictSetting, 'true')

                Label = ET.SubElement(dictSetting, 'key')
                Label.text = 'Label'
                LabelString = ET.SubElement(dictSetting, 'string')
                if 'Label' in webClipDict:
                    LabelString.text = str(webClipDict['Label'])
                else:
                    LabelString.text = 'Default Web Clip'

                descriptionKey = ET.SubElement(dictSetting, 'key')
                descriptionKey.text = 'PayloadDescription'
                descriptionString = ET.SubElement(dictSetting, 'string')
                descriptionString.text = 'Configures Web Clip'

                payloadName = ET.SubElement(dictSetting, 'key')
                payloadName.text = 'PayloadDisplayName'
                payloadNameString = ET.SubElement(dictSetting, 'string')
                payloadNameString.text = 'Web Clip (' + LabelString + ')'

                payloadIdentifier = ET.SubElement(dictSetting, 'key')
                payloadIdentifier.text = 'PayloadIdentifier'
                payloadIdentifierString = ET.SubElement(dictSetting, 'string')
                payloadIdentifierString.text = 'com.toppatch.testProfile.WebClip'

                payloadOrg = ET.SubElement(dictSetting, 'key')
                payloadOrg.text = 'PayloadOrganization'
                payloadOrgString = ET.SubElement(dictSetting, 'string')
                payloadOrgString.text = 'Toppatch'

                payloadType = ET.SubElement(dictSetting, 'key')
                payloadType.text = 'PayloadType'
                payloadTypeString = ET.SubElement(dictSetting, 'string')
                payloadTypeString.text = 'com.apple.webClip.managed'

                payloadUUID = ET.SubElement(dictSetting, 'key')
                payloadUUID.text = 'PayloadUUID'
                payloadUUIDString = ET.SubElement(dictSetting, 'string')
                payloadUUIDString.text = 'E78EA14C-E214-46A2-A1A5-5C93F8B338C2'

                payloadVersion = ET.SubElement(dictSetting, 'key')
                payloadVersion.text = 'PayloadVersion'
                payloadVersionString = ET.SubElement(dictSetting, 'integer')
                payloadVersionString.text = str(1)

                Precomposed = ET.SubElement(dictSetting, 'key')
                Precomposed.text = 'Precomposed'
                if 'Precomposed' in webClipDict:
                    PrecomposedValue = ET.SubElement(
                        dictSetting, str(
                            webClipDict['Precomposed']).lower())
                else:
                    PrecomposedValue = ET.SubElement(dictSetting, 'true')

                URL = ET.SubElement(dictSetting, 'key')
                URL.text = 'URL'
                URLString = ET.SubElement(dictSetting, 'string')
                if 'URL' in webClipDict:
                    URLString.text = str(webClipDict['URL'])
                else:
                    URLString.text = 'http://www.toppatch.com'
                    self.log.e(tag, 'WebClip URL is not Sent')

        #### condition for WIFI and XML creation######
#         if self.json_dict.has_key('wifi'):
            if policy['type'] == 'wifi':
                print 'wifi found'
                payload_name_str = "WiFi Profile"
                payload_identifier_str = 'com.toppatch.wifiProfile'
                payload_uuid_str = 'C1A4F8F9-4506-49CE-89D6-70A5A45D5657'
                wifiDict_list = policy['data']
                for e, wifiDict in enumerate(wifiDict_list):
                    dictSetting = ET.SubElement(arrayPayload, 'dict')

                    AutoJoin = ET.SubElement(dictSetting, 'key')
                    AutoJoin.text = 'AutoJoin'
                    if 'AutoJoin' in wifiDict:
                        AutoJoinValue = ET.SubElement(
                            dictSetting, str(
                                wifiDict['AutoJoin']).lower())
                    else:
                        AutoJoinValue = ET.SubElement(dictSetting, 'true')

                    EncryptionType = ET.SubElement(dictSetting, 'key')
                    EncryptionType.text = 'EncryptionType'
                    EncryptionTypeString = ET.SubElement(dictSetting, 'string')
                    if 'EncryptionType' in wifiDict:
                        EncryptionTypeString.text = str(
                            wifiDict['EncryptionType'])
                    else:
                        EncryptionTypeString.text = 'Any'

                    HIDDEN_NETWORK = ET.SubElement(dictSetting, 'key')
                    HIDDEN_NETWORK.text = 'HIDDEN_NETWORK'
                    if 'HIDDEN_NETWORK' in wifiDict:
                        HIDDEN_NETWORKValue = ET.SubElement(
                            dictSetting, str(
                                wifiDict['HIDDEN_NETWORK']).lower())
                    else:
                        HIDDEN_NETWORKValue = ET.SubElement(
                            dictSetting,
                            'false')

                    Password = ET.SubElement(dictSetting, 'key')
                    Password.text = 'Password'
                    PasswordString = ET.SubElement(dictSetting, 'string')
                    if 'Password' in wifiDict:
                        PasswordString.text = str(wifiDict['Password'])
                    else:
                        PasswordString.text = ''
                        self.log.e(tag, 'Password for WIFI is not Sent')

                    descriptionKey = ET.SubElement(dictSetting, 'key')
                    descriptionKey.text = 'PayloadDescription'
                    descriptionString = ET.SubElement(dictSetting, 'string')
                    descriptionString.text = 'Configures wireless connectivity settings.'

                    payloadName = ET.SubElement(dictSetting, 'key')
                    payloadName.text = 'PayloadDisplayName'
                    payloadNameString = ET.SubElement(dictSetting, 'string')
                    if 'SSID_STR' in wifiDict:
                        payloadNameString.text = 'Wi-Fi (' + \
                            str(wifiDict['SSID_STR']) + ')'
                    else:
                        payloadNameString.text = 'Wi-Fi'
                        self.log.e(tag, 'WIFI SSID not sent is not Sent')

                    payloadIdentifier = ET.SubElement(dictSetting, 'key')
                    payloadIdentifier.text = 'PayloadIdentifier'
                    payloadIdentifierString = ET.SubElement(
                        dictSetting,
                        'string')
                    payloadIdentifierString.text = 'com.toppatch.wifiProfile.wifi{0}'.format(
                        e)

                    payloadOrg = ET.SubElement(dictSetting, 'key')
                    payloadOrg.text = 'PayloadOrganization'
                    payloadOrgString = ET.SubElement(dictSetting, 'string')
                    payloadOrgString.text = 'Toppatch'

                    payloadType = ET.SubElement(dictSetting, 'key')
                    payloadType.text = 'PayloadType'
                    payloadTypeString = ET.SubElement(dictSetting, 'string')
                    payloadTypeString.text = 'com.apple.wifi.managed'

                    payloadUUID = ET.SubElement(dictSetting, 'key')
                    payloadUUID.text = 'PayloadUUID'
                    payloadUUIDString = ET.SubElement(dictSetting, 'string')
                    payloadUUIDString.text = '50BB7AA6-2489-45FD-A82E-C6E5B5BEB552{0}'.format(
                        e)

                    payloadVersion = ET.SubElement(dictSetting, 'key')
                    payloadVersion.text = 'PayloadVersion'
                    payloadVersionString = ET.SubElement(
                        dictSetting,
                        'integer')
                    payloadVersionString.text = str(1)

                    ProxyType = ET.SubElement(dictSetting, 'key')
                    ProxyType.text = 'ProxyType'
                    ProxyTypeString = ET.SubElement(dictSetting, 'string')
                    ProxyTypeString.text = 'None'

                    SSID_STR = ET.SubElement(dictSetting, 'key')
                    SSID_STR.text = 'SSID_STR'
                    SSID_STRString = ET.SubElement(dictSetting, 'string')
                    if 'SSID_STR' in wifiDict:
                        SSID_STRString.text = str(wifiDict['SSID_STR'])
                    else:
                        SSID_STRString.text = 'HugoMinds'
                        self.log.e(tag, 'WIFI SSID not sent is not Sent')

        #### condition for VPN and XML creation######
#         if self.json_dict.has_key('vpn'):
            if policy['type'] == 'vpn':
                payload_name_str = 'VPN Profile'
                payload_identifier_str = 'com.toppatch.vpnProfile'
                payload_uuid_str = '9161ACC4-B0A8-4A28-92BC-6538B446C46B'

                vpnDict_list = policy['data']
                for e, vpnDict in enumerate(vpnDict_list):

                    dictSetting = etree.SubElement(arrayPayload, 'dict')
                    vpn_type = vpnDict.get('VpnType')
                    ### IPV4 DICT START HERE ####
                    IPV4 = etree.SubElement(dictSetting, 'key')
                    IPV4.text = 'IPv4'
                    ipv4_dict = etree.SubElement(dictSetting, 'dict')

                    override_primary = etree.SubElement(ipv4_dict, 'key')
                    override_primary.text = 'OverridePrimary'
                    override_primary_int = etree.SubElement(
                        ipv4_dict,
                        'integer')

                    if 'OverridePrimary' in vpnDict:
                        override_primary_int.text = str(1)
                    else:
                        override_primary_int = str(0)

                    ### IPV4 DICT END HERE ####

                    if vpn_type == 'IPSec':
                        # implement ipsec attributrs here except proxy and ipv4
                        IPSec = etree.SubElement(dictSetting, 'key')
                        IPSec.text = 'IPSec'

                        ipsec_dict = etree.SubElement(dictSetting, 'dict')

                        AuthenticationMethod = etree.SubElement(
                            ipsec_dict,
                            'key')
                        AuthenticationMethod.text = 'AuthenticationMethod'

                        auth_method = vpnDict.get('AuthMethod')
                        AuthenticationMethodString = etree.SubElement(
                            ipsec_dict,
                            'string')
                        AuthenticationMethodString.text = str(auth_method)

                        if auth_method == 'Certificate':

                            OnDemandEnabled = etree.SubElement(
                                ipsec_dict,
                                'key')
                            OnDemandEnabled.text = 'OnDemandEnabled'
                            OnDemandEnabledInteger = etree.SubElement(
                                ipsec_dict,
                                'integer')

                            if vpnDict.get('OnDemandEnabled'):
                                OnDemandEnabledInteger.text = str(1)
                            else:
                                OnDemandEnabledInteger.text = str(0)

                            PayloadCertificateUUID = etree.SubElement(
                                ipsec_dict,
                                'key')
                            PayloadCertificateUUID.text = 'PayloadCertificateUUID'
                            PayloadCertificateUUIDString = etree.SubElement(
                                ipsec_dict,
                                'string')
                            PayloadCertificateUUIDString.text = '1FC21597-A2ED-4907-8ED7-0B07FFDDABDF'

                            if vpnDict.get('PromptForVPNPIN'):
                                PromptForVPNPIN = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                PromptForVPNPIN.text = 'PromptForVPNPIN'
                                etree.SubElement(ipsec_dict, 'true')

                            if 'OnDemandEnabledDict' in vpnDict:

                                on_demand_dict = vpnDict.get(
                                    'OnDemandEnabledDict')
                                on_demand_always = on_demand_dict.get(
                                    'OnDemandAlways')
                                on_demand_never = on_demand_dict.get(
                                    'OnDemandNever')
                                on_demand_retry = on_demand_dict.get(
                                    'OnDemandRetry')

                                OnDemandMatchDomainsAlways = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                OnDemandMatchDomainsAlways.text = 'OnDemandMatchDomainsAlways'
                                on_demand_always_array = etree.SubElement(
                                    ipsec_dict,
                                    'array')

                                for e in on_demand_always:

                                    OnDemandMatchDomainsAlwaysArrayString = etree.SubElement(
                                        on_demand_always_array,
                                        'string')
                                    OnDemandMatchDomainsAlwaysArrayString.text = str(
                                        e)

                                OnDemandMatchDomainsNever = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                OnDemandMatchDomainsNever.text = 'OnDemandMatchDomainsNever'
                                on_demand_never_array = etree.SubElement(
                                    ipsec_dict,
                                    'array')

                                for e in on_demand_never:

                                    OnDemandMatchDomainsNeverArrayString = etree.SubElement(
                                        on_demand_never_array,
                                        'string')
                                    OnDemandMatchDomainsNeverArrayString.text = str(
                                        e)

                                OnDemandMatchDomainsOnRetry = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                OnDemandMatchDomainsOnRetry.text = 'OnDemandMatchDomainsOnRetry'
                                on_demand_retry_array = etree.SubElement(
                                    ipsec_dict,
                                    'array')

                                for e in on_demand_retry:

                                    OnDemandMatchDomainsRetryArrayString = etree.SubElement(
                                        on_demand_retry_array,
                                        'string')
                                    OnDemandMatchDomainsRetryArrayString.text = str(
                                        e)

                        if auth_method == 'SharedSecret':

                            LocalIdentifier = etree.SubElement(
                                ipsec_dict,
                                'key')
                            LocalIdentifier.text = 'LocalIdentifier'
                            LocalIdentifierString = etree.SubElement(
                                ipsec_dict,
                                'string')

                            if vpnDict.get('Hybrid'):
                                LocalIdentifierString.text = '{0}[hybrid]'.format(
                                    vpnDict.get('GroupName'))
                            else:
                                LocalIdentifierString.text = '{0}'.format(
                                    vpnDict.get('GroupName'))

                            LocalIdentifierType = etree.SubElement(
                                ipsec_dict,
                                'key')
                            LocalIdentifierType.text = 'LocalIdentifierType'
                            LocalIdentifierTypeString = etree.SubElement(
                                ipsec_dict, 'string')
                            LocalIdentifierTypeString.text = 'KeyID'

                            if 'SharedSecret' in vpnDict:

                                SharedSecret = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                SharedSecret.text = 'SharedSecret'
                                SharedSecretData = etree.SubElement(
                                    ipsec_dict,
                                    'data')
                                SharedSecretData.text = base64.b64encode(
                                    vpnDict.get('SharedSecret'))

                            if vpnDict.get('PromptPassword'):

                                XAuthPasswordEncryption = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                XAuthPasswordEncryption.text = 'XAuthPasswordEncryption'
                                XAuthPasswordEncryptionString = etree.SubElement(
                                    ipsec_dict,
                                    'string')
                                XAuthPasswordEncryptionString.text = str(
                                    'Prompt')

                        RemoteAddress = etree.SubElement(ipsec_dict, 'key')
                        RemoteAddress.text = 'RemoteAddress'
                        RemoteAddressString = etree.SubElement(
                            ipsec_dict,
                            'string')
                        RemoteAddressString.text = str(vpnDict.get('Server'))

                        XAuthEnabled = etree.SubElement(ipsec_dict, 'key')
                        XAuthEnabled.text = 'XAuthEnabled'
                        XAuthEnabledInteger = etree.SubElement(
                            ipsec_dict,
                            'integer')
                        XAuthEnabledInteger.text = str(1)

                        XAuthName = etree.SubElement(ipsec_dict, 'key')
                        XAuthName.text = 'XAuthName'
                        XAuthNameString = etree.SubElement(
                            ipsec_dict,
                            'string')
                        XAuthNameString.text = str(vpnDict.get('Account'))

                    else:
                        ### EAP DICT START HERE ###
                        EAP = etree.SubElement(dictSetting, 'key')
                        EAP.text = 'EAP'
                        etree.SubElement(dictSetting, 'dict')
                        ### EAP DICT END HERE ###

                        ### PPP DICT START HERE ###
                        PPP = etree.SubElement(dictSetting, 'key')
                        PPP.text = 'PPP'

                        ppp_dict = etree.SubElement(dictSetting, 'dict')

                        if 'RSASecure' in vpnDict and vpnDict.get('RSASecure'):
                            AuthEAPPlugins = etree.SubElement(ppp_dict, 'key')
                            AuthEAPPlugins.text = 'AuthEAPPlugins'
                            AuthEAPPlugins_array = etree.SubElement(
                                ppp_dict,
                                'array')
                            AuthEAP_RSAString = etree.SubElement(
                                AuthEAPPlugins_array,
                                'string')
                            AuthEAP_RSAString.text = 'EAP-RSA'

                        AuthName = etree.SubElement(ppp_dict, 'key')
                        AuthName.text = 'AuthName'

                        AuthNameString = etree.SubElement(ppp_dict, 'string')

                        if 'Account' in vpnDict:
                            AuthNameString.text = vpnDict.get('Account')
                        else:
                            AuthNameString.text = 'Default'
                            self.log.e(tag, 'Account is not provided in VPN')

                        if 'RSASecure' in vpnDict and vpnDict.get('RSASecure'):
                            AuthProtocol = etree.SubElement(ppp_dict, 'key')
                            AuthProtocol.text = 'AuthProtocol'
                            AuthProtocol_array = etree.SubElement(
                                ppp_dict,
                                'array')
                            EAPString = etree.SubElement(
                                AuthProtocol_array,
                                'string')
                            EAPString.text = 'EAP'

                        if vpn_type == 'PPTP':

                            CCPEnabled = etree.SubElement(ppp_dict, 'key')
                            CCPEnabled.text = 'CCPEnabled'
                            CCPEnabledInteger = etree.SubElement(
                                ppp_dict,
                                'integer')

                            CCPMPPE128Enabled = etree.SubElement(
                                ppp_dict,
                                'key')
                            CCPMPPE128Enabled.text = 'CCPMPPE128Enabled'
                            CCPMPPE128EnabledInteger = etree.SubElement(
                                ppp_dict,
                                'integer')

                            CCPMPPE40Enabled = etree.SubElement(
                                ppp_dict,
                                'key')
                            CCPMPPE40Enabled.text = 'CCPMPPE40Enabled'
                            CCPMPPE40EnabledInteger = etree.SubElement(
                                ppp_dict,
                                'integer')
                            CCPMPPE40EnabledInteger.text = str(0)
                            if 'EncryptionAutomatic' in vpnDict:
                                CCPEnabledInteger.text = str(1)
                                CCPMPPE128EnabledInteger.text = str(0)

                            elif 'EncryptionMax' in vpnDict:
                                CCPEnabledInteger.text = str(0)
                                CCPMPPE128EnabledInteger = str(1)
                            else:
                                CCPEnabledInteger.text = str(0)
                                CCPMPPE128EnabledInteger.text = str(0)

                        CommRemoteAddress = etree.SubElement(ppp_dict, 'key')
                        CommRemoteAddress.text = 'CommRemoteAddress'
                        CommRemoteAddressString = etree.SubElement(
                            ppp_dict,
                            'string')
                        CommRemoteAddressString.text = str(
                            vpnDict.get('Server'))

                        if 'RSASecure' in vpnDict and vpnDict.get('RSASecure'):
                            TokenCard = etree.SubElement(ppp_dict, 'key')
                            TokenCard.text = 'TokenCard'
                            TokenCardValue = etree.SubElement(ppp_dict, 'true')

                        ### PPP DICT END HERE ###

                        ### L2TP IPSEC DICT START HERE ###
                        if vpn_type == 'L2TP':

                            IPSec = etree.SubElement(dictSetting, 'key')
                            IPSec.text = 'IPSec'

                            ipsec_dict = etree.SubElement(dictSetting, 'dict')

                            AuthenticationMethod = etree.SubElement(
                                ipsec_dict,
                                'key')
                            AuthenticationMethod.text = 'AuthenticationMethod'
                            AuthenticationMethodString = etree.SubElement(
                                ipsec_dict,
                                'string')
                            AuthenticationMethodString.text = 'SharedSecret'

                            if 'SharedSecret' in vpnDict:

                                SharedSecret = etree.SubElement(
                                    ipsec_dict,
                                    'key')
                                SharedSecret.text = 'SharedSecret'
                                SharedSecretData = etree.SubElement(
                                    ipsec_dict,
                                    'data')
                                SharedSecretData.text = base64.b64encode(
                                    vpnDict.get('SharedSecret'))

                        ### L2TP IPSEC DICT END HERE ###

                    DescriptionKey = etree.SubElement(dictSetting, 'key')
                    DescriptionKey.text = 'PayloadDescription'

                    DescriptionString = etree.SubElement(dictSetting, 'string')
                    DescriptionString.text = 'Configures VPN settings, including authentication.'

                    PayloadDisplayName = etree.SubElement(dictSetting, 'key')
                    PayloadDisplayName.text = 'PayloadDisplayName'

                    PayloadDisplayNameString = etree.SubElement(
                        dictSetting,
                        'string')
                    PayloadDisplayNameString.text = 'VPN {0}'.format(
                        vpnDict.get('UserDefinedName'))

                    PayloadIdentifier = etree.SubElement(dictSetting, 'key')
                    PayloadIdentifier.text = 'PayloadIdentifier'

                    PayloadIdentifierString = etree.SubElement(
                        dictSetting,
                        'string')
                    PayloadIdentifierString.text = 'com.toppatch.vpnProfile.vpn{0}'.format(
                        e)

                    PayloadOrg = etree.SubElement(dictSetting, 'key')
                    PayloadOrg.text = 'PayloadOrganization'

                    PayloadOrgString = etree.SubElement(dictSetting, 'string')
                    PayloadOrgString.text = 'Toppatch'

                    PayloadType = etree.SubElement(dictSetting, 'key')
                    PayloadType.text = 'PayloadType'

                    PayloadTypeString = etree.SubElement(dictSetting, 'string')
                    PayloadTypeString.text = 'com.apple.vpn.managed'

                    PayloadUUID = etree.SubElement(dictSetting, 'key')
                    PayloadUUID.text = 'PayloadUUID'

                    PayloadUUIDString = etree.SubElement(dictSetting, 'string')
                    PayloadUUIDString.text = 'E41B3848-D2F9-4555-BBC3-F6EEFF71690D{0}'.format(
                        e)

                    PayloadVersion = etree.SubElement(dictSetting, 'key')
                    PayloadVersion.text = 'PayloadVersion'

                    PayloadVersionInteger = etree.SubElement(
                        dictSetting,
                        'integer')
                    PayloadVersionInteger.text = str(1)

                    Proxies = etree.SubElement(dictSetting, 'key')
                    Proxies.text = 'Proxies'

                    proxy_dict = etree.SubElement(dictSetting, 'dict')

                    if 'ManualProxy' in vpnDict:

                        manual_proxy_dict = vpnDict.get('ManualProxy')
                        HTTPEnable = etree.SubElement(proxy_dict, 'key')
                        HTTPEnable.text = 'HTTPEnable'
                        HTTPEnableInteger = etree.SubElement(
                            proxy_dict,
                            'integer')
                        HTTPEnableInteger.text = str(1)

                        HTTPPort = etree.SubElement(proxy_dict, 'key')
                        HTTPPort.text = 'HTTPPort'
                        HTTPPortInteger = etree.SubElement(
                            proxy_dict,
                            'integer')
                        HTTPPortInteger.text = str(
                            manual_proxy_dict.get('PortNumber'))

                        HTTPProxy = etree.SubElement(proxy_dict, 'key')
                        HTTPProxy.text = 'HTTPProxy'
                        HTTPProxyString = etree.SubElement(
                            proxy_dict,
                            'string')
                        HTTPProxyString.text = str(
                            manual_proxy_dict.get('HTTPProxy'))

                        HTTPProxyPassword = etree.SubElement(proxy_dict, 'key')
                        HTTPProxyPassword.text = 'HTTPProxyPassword'
                        HTTPProxyPasswordString = etree.SubElement(
                            proxy_dict,
                            'string')
                        HTTPProxyPasswordString.text = str(
                            manual_proxy_dict.get('ProxyPassword'))

                        HTTPProxyUsername = etree.SubElement(proxy_dict, 'key')
                        HTTPProxyUsername.text = 'HTTPProxyUsername'
                        HTTPProxyUsernameString = etree.SubElement(
                            proxy_dict,
                            'string')
                        HTTPProxyUsernameString.text = str(
                            manual_proxy_dict.get('ProxyUsername'))

                        HTTPSEnable = etree.SubElement(proxy_dict, 'key')
                        HTTPSEnable.text = 'HTTPSEnable'
                        HTTPSEnableInteger = etree.SubElement(
                            proxy_dict,
                            'integer')
                        HTTPSEnableInteger.text = str(1)

                        HTTPSPort = etree.SubElement(proxy_dict, 'key')
                        HTTPSPort.text = 'HTTPSPort'
                        HTTPSPortInteger = etree.SubElement(
                            proxy_dict,
                            'integer')
                        HTTPSPortInteger.text = str(
                            manual_proxy_dict.get('PortNumber'))

                        HTTPSProxy = etree.SubElement(proxy_dict, 'key')
                        HTTPSProxy.text = 'HTTPSProxy'
                        HTTPSProxyString = etree.SubElement(
                            proxy_dict,
                            'string')
                        HTTPSProxyString.text = str(
                            manual_proxy_dict.get('HTTPProxy'))

                        # pass
                    elif 'AutomaticProxy' in vpnDict:
                        auto_proxy_dict = vpnDict.get('AutomaticProxy')

                        if 'ProxyServerUrl' in auto_proxy_dict:

                            ProxyAutoConfigEnable = etree.SubElement(
                                proxy_dict,
                                'key')
                            ProxyAutoConfigEnable.text = 'ProxyAutoConfigEnable'
                            ProxyAutoConfigEnableInteger = etree.SubElement(
                                proxy_dict,
                                'integer')
                            ProxyAutoConfigEnableInteger.text = str(1)

                            ProxyAutoConfigURL = etree.SubElement(
                                proxy_dict,
                                'key')
                            ProxyAutoConfigURL.text = 'ProxyAutoConfigURLString'
                            ProxyAutoConfigURLString = etree.SubElement(
                                proxy_dict,
                                'string')
                            ProxyAutoConfigURLString.text = str(
                                auto_proxy_dict.get('ProxyServerUrl'))

                        else:

                            ProxyAutoDiscoveryEnable = etree.SubElement(
                                proxy_dict,
                                'key')
                            ProxyAutoDiscoveryEnable.text = 'ProxyAutoDiscoveryEnable'
                            ProxyAutoDiscoveryEnableInteger = etree.SubElement(
                                proxy_dict,
                                'integer')
                            ProxyAutoDiscoveryEnableInteger.text = str(1)

                    UserDefinedName = etree.SubElement(dictSetting, 'key')
                    UserDefinedName.text = 'UserDefinedName'
                    UserDefinedNameString = etree.SubElement(
                        dictSetting,
                        'string')
                    UserDefinedNameString.text = str(
                        vpnDict.get('UserDefinedName'))

                    VPNType = etree.SubElement(dictSetting, 'key')
                    VPNType.text = 'VPNType'
                    VPNTypeString = etree.SubElement(dictSetting, 'string')
                    VPNTypeString.text = str(vpn_type)

        descriptionKey = ET.SubElement(rootDict, 'key')
        descriptionKey.text = 'PayloadDescription'
        descriptionString = ET.SubElement(rootDict, 'string')
        descriptionString.text = 'Testing the Profile'

        payloadName = ET.SubElement(rootDict, 'key')
        payloadName.text = 'PayloadDisplayName'
        payloadNameString = ET.SubElement(rootDict, 'string')
        payloadNameString.text = payload_name_str

        payloadIdentifier = ET.SubElement(rootDict, 'key')
        payloadIdentifier.text = 'PayloadIdentifier'
        payloadIdentifierString = ET.SubElement(rootDict, 'string')
        payloadIdentifierString.text = payload_identifier_str

        payloadOrg = ET.SubElement(rootDict, 'key')
        payloadOrg.text = 'PayloadOrganization'
        payloadOrgString = ET.SubElement(rootDict, 'string')
        payloadOrgString.text = 'Toppatch'

        PayloadRemovalDisallowed = ET.SubElement(rootDict, 'key')
        PayloadRemovalDisallowed.text = 'PayloadRemovalDisallowed'
        payloadOrgValue = ET.SubElement(rootDict, 'true')

        PayloadType = ET.SubElement(rootDict, 'key')
        PayloadType.text = 'PayloadType'
        PayloadTypeString = ET.SubElement(rootDict, 'string')
        PayloadTypeString.text = 'Configuration'

        payloadUUID = ET.SubElement(rootDict, 'key')
        payloadUUID.text = 'PayloadUUID'
        payloadUUIDString = ET.SubElement(rootDict, 'string')
        payloadUUIDString.text = payload_uuid_str

        payloadVersion = ET.SubElement(rootDict, 'key')
        payloadVersion.text = 'PayloadVersion'
        payloadVersionString = ET.SubElement(rootDict, 'integer')
        payloadVersionString.text = str(1)

        self.profile = ET.tostring(self.profile)
#         print self.profile
