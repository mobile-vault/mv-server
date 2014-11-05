#! /bin/python
'''
This script will map the policy to iOS actions and return the list of
appropriate actions with valid type and data fields.
'''

import json


def get_mapped_policy(policy_json):

    restrictions_data = {}
    final_action = {}
    policy = {}
    _restrictions = {}

    if isinstance(policy_json, str):
        policy_json = json.loads(policy_json)

    policy_keys = policy_json.keys()

    # start assigning relavant attributes to corresponding variables
    for key in policy_keys:
        if key == 'applications':
            application_dict = policy_json.pop('applications')
            install_apps = application_dict.get('installed_apps')
            remove_apps = application_dict.get('removed_apps')

            _restrictions['browser_settings'] = application_dict.get(
                'browser_settings')
            _restrictions['playstore_enable'] = application_dict.get(
                'playstore_enable')
            _restrictions['itunes_enable'] = application_dict.get(
                'itunes_enable')
            _restrictions['siri_enable'] = application_dict.get(
                'siri_enable')
            _restrictions['safari_enable'] = application_dict.get(
                'safari_enable')
            _restrictions['in_app_purchases'] = application_dict.get(
                'allow_in_app_purchases')

        if key == 'settings':
            settings_dict = policy_json.pop('settings')
            _restrictions['diagnostic_submission'] = settings_dict.get(
                'enable_google_crash_report')
            _restrictions['allow_explicit_content'] = settings_dict.get(
                'allow_explicit_content')
            _restrictions['allow_untrusted_tls_prompt'] = settings_dict.get(
                'allow_untrusted_tls_prompt')

        if key == 'wifi':
            wifi_dict = policy_json.pop('wifi')

            _restrictions['wifi'] = wifi_dict.get('installed_wifis')

        if key == 'access':
            access_dict = policy_json.pop('access')

            _restrictions['screenshot'] = access_dict.get(
                'enable_screen_capture')
            _restrictions['allow_cloud_backup'] = access_dict.get(
                'allow_cloud_backup')
            _restrictions['allow_cloud_document_sync'] = access_dict.get(
                'allow_cloud_document_sync')
            _restrictions['allow_adding_game_center_friends'] = (
                access_dict.get('allow_adding_game_center_friends'))
            #_restrictions['allow_assistant'] = access_dict.get(
            #                                                'allow_assistant')
            _restrictions['allow_multi_player_gaming'] = access_dict.get(
                'allow_multi_player_gaming')
            _restrictions['allow_photo_stream'] = access_dict.get(
                'allow_photo_stream')
            _restrictions['allow_voice_dialing'] = access_dict.get(
                'allow_voice_dialing')
            _restrictions['allow_video_conferencing'] = access_dict.get(
                'allow_video_conferencing')
            _restrictions['force_encrypted_backups'] = access_dict.get(
                'force_encrypted_backups')
            _restrictions['allow_global_background_fetch_when_roaming'] = (
                access_dict.get('allow_global_background_fetch_when_roaming'))
            _restrictions['force_itunes_store_password_entry'] = (
                access_dict.get('force_itunes_store_password_entry'))

        if key == 'hardware':
            hardware_dict = policy_json.pop('hardware')

            _restrictions['enable_camera'] = hardware_dict.get(
                'enable_camera')

        if key == 'vpn':
            vpn_dict = policy_json.pop('vpn')

            _restrictions['vpn'] = vpn_dict.get('installed_vpns')

        # assignments ends here

    if install_apps:
        install_application = []

        for apps in iter(install_apps):
            if apps.get('iOS'):
                install_application.append(
                    {'id': apps.get('id'),
                        'app_identifier': apps.get('app_identifier')})

        final_action['install_application'] = install_application

    if remove_apps:
        remove_application = []

        for apps in iter(remove_apps):
            if apps.get('iOS'):
                remove_application.append(apps.get('app_identifier'))

        final_action['remove_application'] = remove_application

    if _restrictions.get('browser_settings'):

        ios_flag = _restrictions['browser_settings'].get('iOS')

        browser_restriction = _restrictions.get(
            'browser_settings') if ios_flag else None

        if browser_restriction:
            restrictions_data['safariAllowPopups'] = browser_restriction.get(
                'enable_popups')
            restrictions_data['safariAllowJavaScript'] = (
                browser_restriction.get('enable_javascript'))
            restrictions_data['safariAllowAutoFill'] = browser_restriction.get(
                'enable_autofill')
            if browser_restriction.get('disable_cookies') is True:
                restrictions_data['safariAcceptCookies'] = 2
            else:
                restrictions_data['safariAcceptCookies'] = 0

            restrictions_data['safariForceFraudWarning'] = (
                browser_restriction.get('force_fraud_warnings'))

    if _restrictions.get('itunes_enable'):

        ios_flag = _restrictions['itunes_enable'].get('iOS')
        itune_restriction = _restrictions.get(
            'itunes_enable') if ios_flag else None

        if itune_restriction:
            restrictions_data['allowiTunes'] = itune_restriction.get('value')

    if _restrictions.get('playstore_enable'):

        ios_flag = _restrictions['playstore_enable'].get('iOS')
        playstore_restriction = _restrictions.get(
            'playstore_enable') if ios_flag else None

        if playstore_restriction:
            restrictions_data[
                'allowAppInstallation'] = playstore_restriction.get('value')

    if _restrictions.get('siri_enable'):

        ios_flag = _restrictions['siri_enable'].get('iOS')
        siri_restriction = _restrictions.get(
            'siri_enable') if ios_flag else None

        if siri_restriction:
            restrictions_data['allowAssistant'] = siri_restriction.get('value')

    if _restrictions.get('safari_enable'):

        ios_flag = _restrictions['safari_enable'].get('iOS')
        safari_restriction = _restrictions.get(
            'safari_enable') if ios_flag else None

        if safari_restriction:
            restrictions_data['allowSafari'] = safari_restriction.get('value')

    if _restrictions.get('in_app_purchases'):

        ios_flag = _restrictions['in_app_purchases'].get('iOS')
        in_app_purchases = _restrictions.get(
            'in_app_purchases') if ios_flag else None

        if in_app_purchases:
            restrictions_data['allowInAppPurchases'] = in_app_purchases.get(
                'value')

    if _restrictions.get('enable_camera'):

        ios_flag = _restrictions['enable_camera'].get('iOS')
        camera_restriction = _restrictions.get(
            'enable_camera') if ios_flag else None

        if camera_restriction:
            restrictions_data['allowCamera'] = camera_restriction.get('value')

    if _restrictions.get('diagnostic_submission'):

        ios_flag = _restrictions['diagnostic_submission'].get('iOS')
        report_restriction = _restrictions.get(
            'diagnostic_submission') if ios_flag else None

        if report_restriction:
            restrictions_data[
                'allowDiagnosticSubmission'] = report_restriction.get('value')

    if _restrictions.get('allow_explicit_content'):

        ios_flag = _restrictions['allow_explicit_content'].get('iOS')
        content_restriction = _restrictions.get(
            'allow_explicit_content') if ios_flag else None

        if content_restriction:
            restrictions_data[
                'allowExplicitContent'] = content_restriction.get('value')

    if _restrictions.get('allow_untrusted_tls_prompt'):

        ios_flag = _restrictions['allow_untrusted_tls_prompt'].get('iOS')
        tls_restriction = _restrictions.get(
            'allow_untrusted_tls_prompt') if ios_flag else None

        if tls_restriction:
            restrictions_data[
                'allowUntrustedTLSPrompt'] = tls_restriction.get('value')

    if _restrictions.get('screenshot'):

        ios_flag = _restrictions['screenshot'].get('iOS')
        screenshot_restriction = _restrictions.get(
            'screenshot') if ios_flag else None

        if screenshot_restriction:
            restrictions_data['allowScreenShot'] = screenshot_restriction.get(
                'value')

    if _restrictions.get('allow_cloud_backup'):

        ios_flag = _restrictions['allow_cloud_backup'].get('iOS')
        backup_restriction = _restrictions.get(
            'allow_cloud_backup') if ios_flag else None

        if backup_restriction:
            restrictions_data['allowCloudBackup'] = backup_restriction.get(
                'value')

    if _restrictions.get('allow_cloud_document_sync'):

        ios_flag = _restrictions['allow_cloud_document_sync'].get('iOS')
        sync_restriction = _restrictions.get(
            'allow_cloud_document_sync') if ios_flag else None

        if sync_restriction:
            restrictions_data['allowCloudDocumentSync'] = sync_restriction.get(
                'value')

    if _restrictions.get('allow_adding_game_center_friends'):

        ios_flag = _restrictions['allow_adding_game_center_friends'].get('iOS')
        game_center_restriction = _restrictions.get(
            'allow_adding_game_center_friends') if ios_flag else None

        if game_center_restriction:
            restrictions_data[
                'allowAddingGameCenterFriends'] = (
                game_center_restriction.get('value'))

    if _restrictions.get('allow_multi_player_gaming'):

        ios_flag = _restrictions['allow_multi_player_gaming'].get('iOS')
        multiplayer_restriction = _restrictions.get(
            'allow_multi_player_gaming') if ios_flag else None

        if multiplayer_restriction:
            restrictions_data['allowMultiplayerGaming'] = (
                multiplayer_restriction.get('value'))

    if _restrictions.get('allow_photo_stream'):

        ios_flag = _restrictions['allow_photo_stream'].get('iOS')
        photo_stream_restriction = _restrictions.get(
            'allow_photo_stream') if ios_flag else None

        if photo_stream_restriction:
            restrictions_data[
                'allowPhotoStream'] = photo_stream_restriction.get('value')

    if _restrictions.get('allow_voice_dialing'):

        ios_flag = _restrictions['allow_voice_dialing'].get('iOS')
        voice_dialing_restriction = _restrictions.get(
            'allow_voice_dialing') if ios_flag else None

        if voice_dialing_restriction:
            restrictions_data[
                'allowVoiceDialing'] = voice_dialing_restriction.get('value')

    if _restrictions.get('allow_video_conferencing'):

        ios_flag = _restrictions['allow_video_conferencing'].get('iOS')
        conferencing_restriction = _restrictions.get(
            'allow_video_conferencing') if ios_flag else None

        if conferencing_restriction:
            restrictions_data[
                'allowVideoConferencing'] = (
                conferencing_restriction.get('value'))

    if _restrictions.get('force_encrypted_backups'):

        ios_flag = _restrictions['force_encrypted_backups'].get('iOS')
        force_encrypted_backups = _restrictions.get(
            'force_encrypted_backups') if ios_flag else None

        if force_encrypted_backups:
            restrictions_data[
                'forceEncryptedBackup'] = force_encrypted_backups.get('value')

    if _restrictions.get('allow_global_background_fetch_when_roaming'):

        ios_flag = _restrictions[
            'allow_global_background_fetch_when_roaming'].get('iOS')
        global_background_fetch_when_roaming = _restrictions.get(
            'force_encrypted_backups') if ios_flag else None

        if global_background_fetch_when_roaming:
            restrictions_data['allowGlobalBackgroundFetchWhenRoaming'] = \
                global_background_fetch_when_roaming.get('value')

    if _restrictions.get('force_itunes_store_password_entry'):

        ios_flag = _restrictions[
            'force_itunes_store_password_entry'].get('iOS')
        force_itunes_store_password_entry = _restrictions.get(
            'force_itunes_store_password_entry') if ios_flag else None

        if force_itunes_store_password_entry:
            restrictions_data['forceITunesStorePasswordEntry'] = \
                force_itunes_store_password_entry.get('value')

    if _restrictions.get('wifi'):
        wifis = []
        wifi_tuple = ('AutoJoin', 'EncryptionType', 'HIDDEN_NETWORK',
                      'Password', 'SSID_STR', 'ProxyType')
        for setting in _restrictions['wifi']:
            wifi = []
            if setting.get('iOS'):
                wifi.append(setting.get('auto_join'))
                wifi.append('Any')
                wifi.append(setting.get('hidden_network'))
                wifi.append(setting.get('password'))
                wifi.append(setting.get('ssid'))
                wifi.append(None)
                wifis.append(dict(zip(wifi_tuple, wifi)))
    else:
        wifis = None

    if _restrictions.get('vpn'):
        vpns = []
        for setting in _restrictions['vpn']:
            if setting.get('iOS'):
                vpns.append(setting)
    else:
        vpns = None

    policy['restriction'] = restrictions_data

    if wifis is not None and len(wifis) == 0:
        wifis = None
    if vpns is not None and len(vpns) == 0:
        vpns = None

    policy['wifi'] = wifis
    policy['vpn'] = vpns
    final_action['policy'] = policy
    return final_action
