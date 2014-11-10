# -*- coding: utf-8 -*-
# import ipdb
import json
from db.helpers.user import UserDBHelper
from db.helpers.role import RoleDBHelper
from db.helpers.team import TeamDBHelper
from db.helpers.device import DeviceDBHelper
from db.helpers.policy import PolicyDBHelper
from db.helpers.company import CompanyDBHelper


class Merger:

    def merge(self, device_id):
        user_helper = UserDBHelper()
        device_helper = DeviceDBHelper()
        roles_helper = RoleDBHelper()
        teams_helper = TeamDBHelper()
        company_helper = CompanyDBHelper()
        policy_helper = PolicyDBHelper()

        if device_id is not None:
            device_details = device_helper.get_device(device_id)
            if device_details is not None and 'user_id' in device_details:
                user_details = user_helper.get_user(
                    str(device_details['user_id']))
                team_id = user_details['team_id']
                role_id = user_details['role_id']
                company_id = user_details['company_id']

                team_details = teams_helper.get_team(str(team_id))
                role_details = roles_helper.get_role(str(role_id))
                company_details = company_helper.get_company(str(company_id))

                if user_details is not None and 'policy_id' in user_details:
                    policy_id_user = user_details['policy_id']
                else:
                    print 'No user details found'

                if team_details is not None and 'policy_id' in team_details:
                    policy_id_team = team_details['policy_id']
                else:
                    print 'no team details found'

                if role_details is not None and 'policy_id' in role_details:
                    policy_id_role = role_details['policy_id']
                else:
                    print 'no role details found'

                if (company_details is not None
                        and 'policy_id' in company_details):
                    policy_id_company = company_details['policy_id']
                else:
                    print 'no company details found'

                if policy_id_company is not None:
                    print 'company policy id=', policy_id_company
                    policy_company = policy_helper.get_policy(
                        str(policy_id_company))
                else:
                    policy_company = None
                if policy_id_role is not None:
                    print 'role policy id=', policy_id_role
                    policy_role = policy_helper.get_policy(str(policy_id_role))
                else:
                    policy_role = None
                if policy_id_team is not None:
                    print 'team policy id=', policy_id_team
                    policy_team = policy_helper.get_policy(str(policy_id_team))
                else:
                    policy_team = None
                if policy_id_user is not None:
                    print 'user policy id=', policy_id_user
                    policy_user = policy_helper.get_policy(str(policy_id_user))
                else:
                    policy_user = None

                return self.merge_policies(
                    policy_company,
                    policy_role,
                    policy_team,
                    policy_user)
            else:
                print 'Invalid device id'

    def merge_policies(self, company, role, team, user):
        '''
        A per plugin implementation of merge_policies. A more generic
        solution is surely possible.
        But it's not a good time to do that, as it will need more testing.
        '''
        if company is not None and company.get('new_attributes'):
            p_company = company.get('new_attributes')
        else:
            p_company = None
        if role is not None and role.get('new_attributes'):
            p_role = role.get('new_attributes')
        else:
            p_role = None
        if team is not None and team.get('new_attributes'):
            p_team = team.get('new_attributes')
        else:
            p_team = None
        if user is not None and user.get('new_attributes'):
            p_user = user.get('new_attributes')
        else:
            p_user = None

        return self.get_merged_dict(
            self.get_merged_dict(
                self.get_merged_dict(
                    p_company,
                    p_role),
                p_team),
            p_user)

    def get_merged_dict(self, a, b):
        '''
        b has higher precedence
        '''
        if a is None:
            return b
        elif b is None:
            return a
        else:
            # both the dicts are not none. Merge them.
            #--------------------------------------
            # SETTINGS
            #--------------------------------------
            if 'settings' not in a:
                if 'settings' not in b:
                    settings = None
                else:
                    settings = b['settings']
            elif 'settings' not in b:
                if 'settings' not in a:
                    settings = None
                else:
                    settings = a
            else:
                settings = a['settings'].copy()
                settings.update(b['settings'])
            #--------------------------------------
            # WIFI
            #--------------------------------------
            if 'wifi' not in a and 'installed_wifis' not in a:
                if 'wifi' not in b and 'installed_wifis' not in b:
                    wifi = None
                else:
                    wifi = b['wifi']
            elif 'wifi' not in b and 'installed_wifis' not in b:
                if 'wifi' not in a and 'installed_wifis' not in a:
                    wifi = None
                else:
                    wifi = a
            else:
                # Add the installed wifis into a single list.
                a['wifi']['installed_wifis'].extend(
                    b['wifi']['installed_wifis'])
                wifi = dict()
                wifi['installed_wifis'] = a['wifi']['installed_wifis']
            #--------------------------------------
            # BLUETOOTH
            #--------------------------------------
            if 'bluetooth' not in a:
                if 'bluetooth' not in b:
                    bluetooth = None
                else:
                    bluetooth = b['bluetooth']
            elif 'bluetooth' not in b:
                if 'bluetooth' not in a:
                    bluetooth = None
                else:
                    bluetooth = a['bluetooth']
            else:
                bluetooth = dict()
                # Needs merging.
                try:
                    power_status = dict(
                        a['bluetooth']['bluetooth_status'].items() +
                        b['bluetooth']['bluetooth_status'].items())
                except Exception as err:
                    print repr(err) + 'power_status'
                    if 'bluetooth_status' in b['bluetooth']:
                        power_status = b['bluetooth']['bluetooth_status']
                    elif 'bluetooth_status' in a['bluetooth']:
                        power_status = a['bluetooth']['bluetooth_status']
                    else:
                        power_status = None
                bluetooth['bluetooth_status'] = power_status
                # Merge whitelisted.
                a_whitelisted = a['bluetooth'].get('white_listed_pairings')
                b_whitelisted = b['bluetooth'].get('white_listed_pairings')
                if a_whitelisted is not None and b_whitelisted is not None:
                    a_whitelisted.extend(b_whitelisted)
                    bt_whitelisted = a_whitelisted
                else:
                    if a_whitelisted is None and b_whitelisted is not None:
                        bt_whitelisted = b_whitelisted
                    elif a_whitelisted is not None and b_whitelisted is None:
                        bt_whitelisted = a_whitelisted
                    else:
                        bt_whitelisted = None
                bluetooth['white_listed_pairings'] = bt_whitelisted
                # Merge blacklisted
                a_blacklisted = a['bluetooth'].get('black_listed_pairings')
                b_blacklisted = b['bluetooth'].get('black_listed_pairings')
                if a_blacklisted is not None and b_blacklisted is not None:
                    a_blacklisted.extend(b_blacklisted)
                    bt_blacklisted = a_blacklisted
                else:
                    if a_blacklisted is None and b_blacklisted is not None:
                        bt_blacklisted = b_blacklisted
                    elif a_blacklisted is not None and b_blacklisted is None:
                        bt_blacklisted = a_blacklisted
                    else:
                        bt_blacklisted = None
                bluetooth['black_listed_pairings'] = bt_blacklisted
                # ipdb.set_trace()
                #--------------------------------------
                # HARDWARE
                #--------------------------------------
                a_hardware = a.get('hardware')
                b_hardware = b.get('hardware')
                if a_hardware is None:
                    a_hardware = dict()
                if b_hardware is None:
                    b_hardware = dict()
                hardware = a_hardware.copy()
                hardware.update(b_hardware)
                #--------------------------------------
                # APPLICATION
                #--------------------------------------
                a_apps = a.get('applications')
                b_apps = b.get('applications')
                if a_apps is None:
                    a_apps = dict()
                if b_apps is None:
                    b_apps = dict()

                a_apps_installed = a_apps.get('installed_apps')
                b_apps_installed = b_apps.get('installed_apps')

                if a_apps_installed is None:
                    a_apps_installed = []
                if b_apps_installed is None:
                    b_apps_installed = []
                a_apps_installed.extend(b_apps_installed)
                installed_apps = a_apps_installed

                a_apps_removed = a_apps.get('removed_apps')
                b_apps_removed = b_apps.get('removed_apps')
                if a_apps_installed is None:
                    a_apps_installed = []
                if b_apps_installed is None:
                    b_apps_installed = []
                # ipdb.set_trace()
                a_apps_removed.extend(b_apps_removed)
                removed_apps = a_apps_removed

                a_apps_blacklisted = a_apps.get('blacklisted_apps')
                b_apps_blacklisted = b_apps.get('blacklisted_apps')
                if a_apps_blacklisted is None:
                    a_apps_blacklisted = []
                if b_apps_blacklisted is None:
                    b_apps_blacklisted = []
                # ipdb.set_trace()
                a_apps_blacklisted.extend(b_apps_blacklisted)
                blacklisted_apps = a_apps_blacklisted
                application = dict()
                for item in a_apps:
                    if isinstance(a_apps[item], dict):
                        if item in b_apps and isinstance(b_apps[item], dict):
                            application[item] = b_apps[item]
                        else:
                            application[item] = a_apps[item]
                # ipdb.set_trace()
                application['installed_apps'] = installed_apps
                application['removed_apps'] = removed_apps
                application['blacklisted_apps'] = blacklisted_apps
                #--------------------------------------
                # VPN
                #--------------------------------------
                a_vpn = a.get('vpn')
                b_vpn = b.get('vpn')
                if a_vpn is None or 'installed_vpns' not in a_vpn:
                    a_vpn = {'installed_vpns': []}
                if b_vpn is None or 'installed_vpns' not in b_vpn:
                    b_vpn = {'installed_vpns': []}
                a_vpn['installed_vpns'].extend(b_vpn['installed_vpns'])

                vpn = {'installed_vpns': a_vpn['installed_vpns']}

                #--------------------------------------
                # ACCESS
                #--------------------------------------
                a_access = a.get('access')
                b_access = b.get('access')
                if a_access is None:
                    a_access = dict()
                if b_access is None:
                    b_access = dict()
                access = a_access.copy()
                access.update(b_access)

                result = dict()
                result['settings'] = settings
                result['wifi'] = wifi
                result['bluetooth'] = bluetooth
                result['hardware'] = hardware
                result['applications'] = application
                result['vpn'] = vpn
                result['access'] = access
                return result


if __name__ == '__main__':
    print json.dumps(Merger().merge('1'))
