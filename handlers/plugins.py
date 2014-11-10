'''
this script will handle the plugin based JSON data
'''
import json
from db.helpers.policy import PolicyDBHelper
from db.constants import Constants as C
from .default_plugin import plugin_mapping as pm


def get_individual_plugin(policy_id, plugin_name):
    '''
    It will get the data from the policy table against the given policy_id and
    return back the plugin passed.
    '''
    policy = PolicyDBHelper()

    policy_dict = policy.get_policy(str(policy_id))
    policy_json = policy_dict.get(C.POLICY_TABLE_NEW_ATTRIBUTES)
    plugin_policy = policy_json.get(str(plugin_name))
    if plugin_policy:
        return plugin_policy
    else:
        return json.dumps(pm.get(plugin_name))


def put_individual_plugin(policy_id, plugin_name, plugin_data):
    '''
    It will get the data from the UI and put them into the policy table.
    '''
    policy = PolicyDBHelper()
    policy_dict = policy.get_policy(str(policy_id))
    # assign current policy to old_policy
    policy_dict[
        C.POLICY_TABLE_OLD_ATTRIBUTES] = policy_dict[
        C.POLICY_TABLE_NEW_ATTRIBUTES]
    if '_id' in plugin_data:
        plugin_data.pop('_id')
    if 'name' in plugin_data:
        plugin_data.pop('name')
    if 'object_type' in plugin_data:
        plugin_data.pop('object_type')
    policy_dict[C.POLICY_TABLE_NEW_ATTRIBUTES][str(plugin_name)] = plugin_data
    policy_dict[C.POLICY_TABLE_OLD_ATTRIBUTES] = json.dumps(
        policy_dict[C.POLICY_TABLE_OLD_ATTRIBUTES])
    policy_dict[C.POLICY_TABLE_NEW_ATTRIBUTES] = json.dumps(
        policy_dict[C.POLICY_TABLE_NEW_ATTRIBUTES])
    policy_dict.pop('id')
    policy_dict.pop('modified_on')

    # Save the changes to the policy table
    status = policy.update_policy(str(policy_id), policy_dict)
    return status


def setup_default_policy():
    '''
    It will insert the default plugin value in the policy table and add
    corresponding policy_id and plugin json
    '''
    policy = PolicyDBHelper()
    policy_dict = {}
    # Convert plugin policy to json format
    policy_json = json.dumps(pm)
    # assign plugin json to new_attributes tuple
    policy_dict[C.POLICY_TABLE_NEW_ATTRIBUTES] = policy_json
    # insert policy dictionary to policy table which return id
    policy_id = policy.add_policy(policy_dict)
    if policy_id:
        return policy_id, pm
    else:
        print """
        Something went wrong with database policy not saved into policy table.
        """
