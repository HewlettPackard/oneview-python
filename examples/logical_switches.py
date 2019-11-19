# -*- coding: utf-8 -*-
###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# This resource is only available on C7000 enclosures

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# A Logical Switch Group, the Switches IP address/host name, and credentials must be set to run this example
logical_switch_group_name = '<lsg_name>'
switch_ip_1 = '<switch_ip_or_hostname>'
switch_ip_2 = '<switch_ip_or_hostname>'
ssh_username = '<user_name_for_switches>'
ssh_password = '<password_for_switches>'

# To run the scope patch operations in this example, a scope name is required.
scope_name = "<scope_name>"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Check for existance of Logical Switch Group specified, otherwise stops execution
logical_switch_group = oneview_client.logical_switch_groups.get_by('name', logical_switch_group_name)[0]
if logical_switch_group:
    print('Found logical switch group "%s" with uri: %s' % (logical_switch_group['name'], logical_switch_group['uri']))
else:
    raise Exception('Logical switch group "%s" was not found on the appliance.' % logical_switch_group_name)

switch_connection_properties = {
    "connectionProperties": [{
        "propertyName": "SshBasicAuthCredentialUser",
        "value": ssh_username,
        "valueFormat": "Unknown",
        "valueType": "String"
    }, {
        "propertyName": "SshBasicAuthCredentialPassword",
        "value": ssh_password,
        "valueFormat": "SecuritySensitive",
        "valueType": "String"
    }]
}

options = {
    "logicalSwitch": {
        "name": "Test Logical Switch",
        "logicalSwitchGroupUri": logical_switch_group['uri'],
        "switchCredentialConfiguration": [
            {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": switch_ip_1,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }, {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": switch_ip_2,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }
        ]
    },
    "logicalSwitchCredentials": [switch_connection_properties, switch_connection_properties]
}

# Create a Logical Switch
logical_switch = oneview_client.logical_switches.create(options)
print("\nCreated Logical Switch '{name}' successfully.\n  uri = '{uri}'".format(**logical_switch))

# Find the recently created Logical Switch by name
logical_switch = oneview_client.logical_switches.get_by('name', 'Test Logical Switch')[0]
print("\nFound Logical Switch by name: '{name}'.\n  uri = '{uri}'".format(**logical_switch))

# Update the name of the Logical Switch
options_update = {
    "logicalSwitch": {
        "name": "Renamed Logical Switch",
        "uri": logical_switch['uri'],
        "switchCredentialConfiguration": logical_switch['switchCredentialConfiguration'],
        "logicalSwitchGroupUri": logical_switch_group['uri'],
        "consistencyStatus": "CONSISTENT"
    },
    "logicalSwitchCredentials": [switch_connection_properties, switch_connection_properties]
}
logical_switch = oneview_client.logical_switches.update(options_update)
print("\nUpdated Logical Switch successfully.\n  uri = '{uri}'".format(**logical_switch))
print("  with attribute name = {name}".format(**logical_switch))

# Get scope to be added
print("\nGet the scope named '%s'." % scope_name)
scope = oneview_client.scopes.get_by_name(scope_name)

# Performs a patch operation on the Logical Switch
if scope:
    print("\nPatches the logical switch assigning the '%s' scope to it." % scope_name)
    logical_switch = oneview_client.logical_switches.patch(logical_switch['uri'],
                                                           'replace',
                                                           '/scopeUris',
                                                           [scope['uri']])
    pprint(logical_switch)

# Get all, with defaults
print("\nGet all Logical Switches")
logical_switches = oneview_client.logical_switches.get_all()
for logical_switch in logical_switches:
    print('  Name: %s' % logical_switch['name'])

# Get by URI
print("\nGet a Logical Switch by URI")
logical_switch = oneview_client.logical_switches.get(logical_switch['uri'])
pprint(logical_switch)

# Reclaim the top-of-rack switches in the logical switch
print("\nReclaim the top-of-rack switches in the logical switch")
logical_switch = oneview_client.logical_switches.refresh(logical_switch['uri'])
print("  Done.")

# Delete the Logical Switch
oneview_client.logical_switches.delete(logical_switch)
print("\nLogical switch deleted successfully.")
