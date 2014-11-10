"""
vpn constant to be needed from UI and formated by ios_policy
"""

vpn_dict = {
    'VpnType': "VPN Name (PPTP/L2TP/IPSec)",
    'OverridePrimary': "Send All Trafic(true/false)",
    'AuthMethod': "Machine Authentication (Certificate/SharedSecret)",
    'OnDemandEnabled': "Enable Vpn On Demand (true/false)",
    'PromptForVPNPIN': "Include user Pin (true/false)",
    'OnDemandEnabledDict': {
        'OnDemandAlways': ["Array of On demand always domain"],
        'OnDemandNever': ["Array of On demand never domain"],
        'OnDemandRetry': ["Array of On demand Establish if needed"]},
    'Hybrid': "Use hybrid Authentication (true/false)",
    'GroupName': "Group Name",
    'SharedSecret': "Shared Secret",
    'PromptPassword': "Prompt for Password (true/false)",
    'Server': "Server",
    'Account': "Account",
    'RSASecure': "User Authentication Type RSA SecureID (true/false)",
    'EncryptionLevel': "Encryption Level (EncryptionAutomatic/EncryptionMax/None)",
    'UserDefinedName': "Connection Name",
    'ManualProxy': {
        'HTTPProxy': "Hostname or IP address",
        'ProxyPassword': "Password",
        'ProxyUsername': "Authentication",
        'PortNumber': "Port"},
    'AutomaticProxy': {
        'ProxyServerUrl': "Proxy Server URL"}}
