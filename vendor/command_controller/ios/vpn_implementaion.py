from lxml import etree
import base64

def create_vpn(vpn_dict):

	array_payload = etree.Element('array')
	#vpn_root_dict = etree.SubElement(arrayPayload, 'dict')
	dictSetting = etree.SubElement(array_payload, 'dict')
	vpn_type = vpn_dict.get('VpnType')
	vpnDict = vpn_dict
	### IPV4 DICT START HERE ####
	IPV4 = etree.SubElement(dictSetting, 'key')
	IPV4.text = 'IPv4'
	ipv4_dict = etree.SubElement(dictSetting, 'dict')
	
	override_primary = etree.SubElement(ipv4_dict, 'key')
	override_primary.text = 'OverridePrimary'
	override_primary_int = etree.SubElement(ipv4_dict, 'integer')
	
	if vpnDict.has_key('OverridePrimary'):
		override_primary_int.text = str(1)
	else:
		override_primary_int = str(0)

	### IPV4 DICT END HERE ####


	if vpn_type == 'IPSec':
		# implement ipsec attributrs here except proxy and ipv4
		IPSec = etree.SubElement(dictSetting, 'key')
		IPSec.text = 'IPSec'

		ipsec_dict = etree.SubElement(dictSetting, 'dict')

		AuthenticationMethod = etree.SubElement(ipsec_dict, 'key')
		AuthenticationMethod.text = 'AuthenticationMethod'

		auth_method = vpnDict.get('AuthMethod')
		AuthenticationMethodString = etree.SubElement(ipsec_dict, 'string')
		AuthenticationMethodString.text = str(auth_method)

		if auth_method == 'Certificate':

			OnDemandEnabled = etree.SubElement(ipsec_dict, 'key')
			OnDemandEnabled.text = 'OnDemandEnabled'
			OnDemandEnabledInteger = etree.SubElement(ipsec_dict, 'integer')
			
			if vpnDict.get('OnDemandEnabled'):
				OnDemandEnabledInteger.text = str(1)
			else:
				OnDemandEnabledInteger.text = str(0)

			PayloadCertificateUUID = etree.SubElement(ipsec_dict, 'key')
			PayloadCertificateUUID.text = 'PayloadCertificateUUID'
			PayloadCertificateUUIDString = etree.SubElement(ipsec_dict, 'string')
			PayloadCertificateUUIDString.text = '1FC21597-A2ED-4907-8ED7-0B07FFDDABDF'

			if vpnDict.get('PromptForVPNPIN'):
				PromptForVPNPIN = etree.SubElement(ipsec_dict, 'key')
				PromptForVPNPIN.text = 'PromptForVPNPIN'
				etree.SubElement(ipsec_dict, 'true')

			if vpnDict.has_key('OnDemandEnabledDict'):
				
				on_demand_dict = vpnDict.get('OnDemandEnabledDict')
				on_demand_always = on_demand_dict.get('OnDemandAlways')
				on_demand_never = on_demand_dict.get('OnDemandNever')
				on_demand_retry = on_demand_dict.get('OnDemandRetry')

				OnDemandMatchDomainsAlways = etree.SubElement(ipsec_dict, 'key')
				OnDemandMatchDomainsAlways.text = 'OnDemandMatchDomainsAlways'
				on_demand_always_array = etree.SubElement(ipsec_dict, 'array')

				for e in on_demand_always:
					
					OnDemandMatchDomainsAlwaysArrayString = etree.SubElement(
										on_demand_always_array, 'string')
					OnDemandMatchDomainsAlwaysArrayString.text = str(e)

				
				OnDemandMatchDomainsNever = etree.SubElement(ipsec_dict, 'key')
				OnDemandMatchDomainsNever.text = 'OnDemandMatchDomainsNever'
				on_demand_never_array = etree.SubElement(ipsec_dict, 'array')

				for e in on_demand_never:
					
					OnDemandMatchDomainsNeverArrayString = etree.SubElement(
									on_demand_never_array, 'string')
					OnDemandMatchDomainsNeverArrayString.text = str(e)


				OnDemandMatchDomainsOnRetry = etree.SubElement(ipsec_dict, 'key')
				OnDemandMatchDomainsOnRetry.text = 'OnDemandMatchDomainsOnRetry'		
				on_demand_retry_array = etree.SubElement(ipsec_dict, 'array')

				for e in on_demand_retry:

					OnDemandMatchDomainsRetryArrayString = etree.SubElement(
							on_demand_retry_array, 'string')
					OnDemandMatchDomainsRetryArrayString.text = str(e)

		if auth_method == 'SharedSecret':

			LocalIdentifier = etree.SubElement(ipsec_dict, 'key')
			LocalIdentifier.text = 'LocalIdentifier'
			LocalIdentifierString = etree.SubElement(ipsec_dict, 'string')

			if vpnDict.get('Hybrid'):
				LocalIdentifierString.text = '{0}[hybrid]'.format(
												vpnDict.get('GroupName'))
			else:
				LocalIdentifierString.text = '{0}'.format(
												vpnDict.get('GroupName'))

			LocalIdentifierType = etree.SubElement(ipsec_dict, 'key')
			LocalIdentifierType.text = 'LocalIdentifierType'
			LocalIdentifierTypeString = etree.SubElement(
													ipsec_dict, 'string')
			LocalIdentifierTypeString.text = 'KeyID'

			if vpnDict.has_key('SharedSecret'):

				SharedSecret = etree.SubElement(ipsec_dict, 'key')
				SharedSecret.text = 'SharedSecret'
				SharedSecretData = etree.SubElement(ipsec_dict, 'data')
				SharedSecretData.text = base64.b64encode(vpnDict.get('SharedSecret'))

			if vpnDict.get('PromptPassword'):
				
				XAuthPasswordEncryption = etree.SubElement(ipsec_dict, 'key')
				XAuthPasswordEncryption.text = 'XAuthPasswordEncryption'
				XAuthPasswordEncryptionString = etree.SubElement(ipsec_dict,
															'string')
				XAuthPasswordEncryptionString.text = str('Prompt')
				
			
		RemoteAddress = etree.SubElement(ipsec_dict, 'key')
		RemoteAddress.text = 'RemoteAddress'
		RemoteAddressString = etree.SubElement(ipsec_dict, 'string')
		RemoteAddressString.text = str(vpnDict.get('Server'))

		XAuthEnabled = etree.SubElement(ipsec_dict, 'key')
		XAuthEnabled.text = 'XAuthEnabled'
		XAuthEnabledInteger = etree.SubElement(ipsec_dict, 'integer')
		XAuthEnabledInteger.text = str(1)

		XAuthName = etree.SubElement(ipsec_dict, 'key')
		XAuthName.text = 'XAuthName'
		XAuthNameString = etree.SubElement(ipsec_dict, 'string')
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

		if vpnDict.has_key('RSASecure'):
			AuthEAPPlugins = etree.SubElement(ppp_dict, 'key')
			AuthEAPPlugins.text = 'AuthEAPPlugins'
			AuthEAPPlugins_array = etree.SubElement(ppp_dict, 'array')
			AuthEAP_RSAString = etree.SubElement(AuthEAPPlugins_array, 'string')
			AuthEAP_RSAString.text = 'EAP-RSA'

		AuthName = etree.SubElement(ppp_dict, 'key')
		AuthName.text = 'AuthName'

		AuthNameString = etree.SubElement(ppp_dict, 'string')

		if vpnDict.has_key('Account'):
			AuthNameString.text = vpnDict.get('Account')
		else:
			AuthNameString.text = 'Default'
			self.log.e(tag,'Account is not provided in VPN')

		if vpnDict.has_key('RSASecure'):
			AuthProtocol = etree.SubElement(ppp_dict, 'key')
			AuthProtocol.text = 'AuthProtocol'
			AuthProtocol_array = etree.SubElement(ppp_dict, 'array')
			EAPString = etree.SubElement(AuthProtocol_array, 'string')
			EAPString.text = 'EAP'

		if vpn_type == 'PPTP':

			CCPEnabled = etree.SubElement(ppp_dict, 'key')
			CCPEnabled.text = 'CCPEnabled'
			CCPEnabledInteger = etree.SubElement(ppp_dict, 'integer')
			
			CCPMPPE128Enabled = etree.SubElement(ppp_dict, 'key')
			CCPMPPE128Enabled.text = 'CCPMPPE128Enabled'
			CCPMPPE128EnabledInteger = etree.SubElement(ppp_dict, 'integer')

			CCPMPPE40Enabled = etree.SubElement(ppp_dict, 'key')
			CCPMPPE40Enabled.text = 'CCPMPPE40Enabled'
			CCPMPPE40EnabledInteger = etree.SubElement(ppp_dict, 'integer')
			CCPMPPE40EnabledInteger.text = str(0)	
			if vpnDict.has_key('EncryptionAutomatic'):
				CCPEnabledInteger.text = str(1)
				CCPMPPE128EnabledInteger.text = str(0)

			elif vpnDict.has_key('EncryptionMax'):
				CCPEnabledInteger.text = str(0)
				CCPMPPE128EnabledInteger = str(1)	
			else:
				CCPEnabledInteger.text = str(0)

		CommRemoteAddress = etree.SubElement(ppp_dict, 'key')
		CommRemoteAddress.text = 'CommRemoteAddress'
		CommRemoteAddressString = etree.SubElement(ppp_dict, 'string')
		CommRemoteAddressString.text = str(vpnDict.get('Server'))

		if vpnDict.has_key('RSASecure'):
			TokenCard = etree.SubElement(ppp_dict, 'key')
			TokenCard.text = 'TokenCard'
			TokenCardValue = etree.SubElement(ppp_dict, 'true')

		### PPP DICT END HERE ###

		### L2TP IPSEC DICT START HERE ###
		if vpn_type == 'L2TP':

			IPSec = etree.SubElement(dictSetting, 'key')
			IPSec.text = 'IPSec'

			ipsec_dict = etree.SubElement(dictSetting, 'dict')

			AuthenticationMethod = etree.SubElement(ipsec_dict, 'key')
			AuthenticationMethod.text = 'AuthenticationMethod'
			AuthenticationMethodString = etree.SubElement(ipsec_dict, 'string')
			AuthenticationMethodString.text = 'SharedSecret'

			if vpnDict.has_key('SharedSecret'):

				SharedSecret = etree.SubElement(ipsec_dict, 'key')
				SharedSecret.text = 'SharedSecret'
				SharedSecretData = etree.SubElement(ipsec_dict, 'data')
				SharedSecretData.text = base64.b64encode(vpnDict.get('SharedSecret'))

		### L2TP IPSEC DICT END HERE ###


	DescriptionKey = etree.SubElement(dictSetting, 'key')
	DescriptionKey.text = 'PayloadDescription'

	DescriptionString = etree.SubElement(dictSetting, 'string')
	DescriptionString.text = 'Configures VPN settings, including authentication.'

	PayloadDisplayName = etree.SubElement(dictSetting, 'key')
	PayloadDisplayName.text = 'PayloadDisplayName'

	PayloadDisplayNameString = etree.SubElement(dictSetting, 'string')
	PayloadDisplayNameString.text = 'VPN {0}'.format(vpnDict.get('UserDefinedName'))

	PayloadIdentifier = etree.SubElement(dictSetting, 'key')
	PayloadIdentifier.text = 'PayloadIdentifier'

	PayloadIdentifierString = etree.SubElement(dictSetting, 'string')
	PayloadIdentifierString.text = 'com.toppatch.testProfile.vpn'

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
	PayloadUUIDString.text = 'E41B3848-D2F9-4555-BBC3-F6EEFF71690D'

	PayloadVersion = etree.SubElement(dictSetting, 'key')
	PayloadVersion.text = 'PayloadVersion'

	PayloadVersionString = etree.SubElement(dictSetting, 'string')
	PayloadVersionString.text = str(1)

	Proxies = etree.SubElement(dictSetting, 'key')
	Proxies.text = 'Proxies'

	proxy_dict = etree.SubElement(dictSetting, 'dict')

	if vpnDict.has_key('ManualProxy'):
		
		manual_proxy_dict = vpnDict.get('ManualProxy')
		HTTPEnable = etree.SubElement(proxy_dict, 'key')
		HTTPEnable.text = 'HTTPEnable'
		HTTPEnableInteger = etree.SubElement(proxy_dict, 'integer')
		HTTPEnableInteger.text = str(1)

		HTTPPort = etree.SubElement(proxy_dict, 'key')
		HTTPPort.text = 'HTTPPort'
		HTTPPortInteger = etree.SubElement(proxy_dict, 'integer')
		HTTPPortInteger.text = str(manual_proxy_dict.get('PortNumber'))

		HTTPProxy = etree.SubElement(proxy_dict, 'key')
		HTTPProxy.text = 'HTTPProxy'
		HTTPProxyString = etree.SubElement(proxy_dict, 'string')
		HTTPProxyString.text = str(manual_proxy_dict.get('HTTPProxy'))

		HTTPProxyPassword = etree.SubElement(proxy_dict, 'key')
		HTTPProxyPassword.text = 'HTTPProxyPassword'
		HTTPProxyPasswordString = etree.SubElement(proxy_dict, 'string')
		HTTPProxyPasswordString.text = str(manual_proxy_dict.get('ProxyPassword'))

		HTTPProxyUsername = etree.SubElement(proxy_dict, 'key')
		HTTPProxyUsername.text = 'HTTPProxyUsername'
		HTTPProxyUsernameString = etree.SubElement(proxy_dict, 'string')
		HTTPProxyUsernameString.text = str(manual_proxy_dict.get('ProxyUsername'))

		HTTPSEnable = etree.SubElement(proxy_dict, 'key')
		HTTPSEnable.text = 'HTTPSEnable'
		HTTPSEnableInteger = etree.SubElement(proxy_dict, 'integer')
		HTTPSEnableInteger.text = str(1)

		HTTPSPort = etree.SubElement(proxy_dict, 'key')
		HTTPSPort.text = 'HTTPSPort'
		HTTPSPortInteger = etree.SubElement(proxy_dict, 'integer')
		HTTPSPortInteger.text = str(manual_proxy_dict.get('PortNumber'))

		HTTPSProxy = etree.SubElement(proxy_dict, 'key')
		HTTPSProxy.text = 'HTTPSProxy'
		HTTPSProxyString = etree.SubElement(proxy_dict, 'string')
		HTTPSProxyString.text = str(manual_proxy_dict.get('HTTPProxy'))

		#pass
	elif vpnDict.has_key('AutomaticProxy'):
		auto_proxy_dict = vpnDict.get('AutomaticProxy')

		if auto_proxy_dict.has_key('ProxyServerUrl'):
			
			ProxyAutoConfigEnable = etree.SubElement(proxy_dict, 'key')
			ProxyAutoConfigEnable.text = 'ProxyAutoConfigEnable'
			ProxyAutoConfigEnableInteger = etree.SubElement(proxy_dict, 'integer')
			ProxyAutoConfigEnableInteger.text = str(1)

			ProxyAutoConfigURL = etree.SubElement(proxy_dict, 'key')
			ProxyAutoConfigURL.text = 'ProxyAutoConfigURLString'
			ProxyAutoConfigURLString = etree.SubElement(proxy_dict, 'string')
			ProxyAutoConfigURLString.text = str(auto_proxy_dict.get('ProxyServerUrl'))

		else:
			
			ProxyAutoDiscoveryEnable = etree.SubElement(proxy_dict, 'key')
			ProxyAutoDiscoveryEnable.text = 'ProxyAutoDiscoveryEnable'
			ProxyAutoDiscoveryEnableInteger = etree.SubElement(proxy_dict, 'integer')
			ProxyAutoDiscoveryEnableInteger.text = str(1)


	UserDefinedName = etree.SubElement(dictSetting, 'key')
	UserDefinedName.text = 'UserDefinedName'
	UserDefinedNameString = etree.SubElement(dictSetting, 'string')
	UserDefinedNameString.text = str(vpnDict.get('UserDefinedName'))

	VPNType = etree.SubElement(dictSetting, 'key')
	VPNType.text = 'VPNType'
	VPNTypeString = etree.SubElement(dictSetting, 'string')
	VPNTypeString.text = str(vpn_type)
	
	return array_payload