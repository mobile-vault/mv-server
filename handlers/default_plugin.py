'''
This file contains default plugin mapping dictionary used for initialization of
plugins in the policy table
'''

plugin_mapping = {
    "applications": {
        "installed_apps": [],
        "removed_apps": [],
        "blacklisted_apps": [],
        "youtube_enable": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "playstore_enable": {
            "value": True,
            "android": True,
            "iOS": True
        },
        "itunes_enable": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "siri_enable": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "safari_enable": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "browser_settings": {
            "enable_autofill": True,
            "enable_javascript": True,
            "enable_cookies": True,
            "enable_popups": True,
            "force_fraud_warnings": True,
            "enable_http_proxy": False,
            "http_proxy_value": "",
            "android": True,
            "iOS": True
        },
        "enable_recording": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "allow_app_installation": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "allow_in_app_purchases": {
            "value": True,
            "android": True,
            "iOS": True
        }
    },
    "hardware": {
        "enable_camera": {
            "value": True,
            "android": True,
            "iOS": True
        },
        "enable_external_storage_encryption": {
            "value": False,
            "android": True,
            "iOS": False
        },
        "enable_internal_storage_encryption": {
            "value": False,
            "android": True,
            "iOS": False
        },
        "enable_microphone": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_android_beam": {
            "value": True,
            "android": True,
            "iOS": False
        }
    },
    "settings": {
        "enable_background_data": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_backup": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_clipboard": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_google_crash_report": {
            "value": True,
            "android": True,
            "iOS": True
        },
        "enable_data_roaming": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_push_roaming": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_sync_roaming": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_voice_roaming": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "allow_explicit_content": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_untrusted_tls_prompt": {
            "value": True,
            "android": False,
            "iOS": True
        }
    },
    "bluetooth": {
        "bluetooth_status": {
            "enable_bluetooth": True,
            "power_status": False,
            "android": True,
            "iOS": True
        },
        "white_listed_pairings": [],
        "black_listed_pairings": []
    },
    "access": {
        "enable_change_settings": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_screen_capture": {
            "value": True,
            "android": True,
            "iOS": True
        },
        "enable_factory_reset": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_usb_debugging": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "enable_admin_mode": {
            "value": True,
            "android": True,
            "iOS": False
        },
        "allow_cloud_backup": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_cloud_document_sync": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_adding_game_center_friends": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "force_encrypted_backups": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_global_background_fetch_when_roaming": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "force_itunes_store_password_entry": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_multi_player_gaming": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_photo_stream": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_voice_dialing": {
            "value": True,
            "android": False,
            "iOS": True
        },
        "allow_video_conferencing": {
            "value": True,
            "android": False,
            "iOS": True
        }
    },
    "wifi": {
        "installed_wifis": [

        ]
    },
    "vpn": {
        "installed_vpns": [

        ]
    }
}
