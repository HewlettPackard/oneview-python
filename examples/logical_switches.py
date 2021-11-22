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
from hpeOneView.oneview_client import OneViewClient
from CONFIG_loader import try_load_from_file

# This resource is only available on C7000 enclosures

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# A Logical Switch Group, the Switches IP address/host name, and credentials must be set to run this
# example
LOGICAL_SWITCH_GROUP_NAME = '<lsg_name>'
SWITCH_IP_1 = '<switch_ip_or_hostname>'
SWITCH_IP_2 = '<switch_ip_or_hostname>'
SSH_USERNAME = '<user_name_for_switches>'
SSH_PASSWORD = '<password_for_switches>'

# To run the SCOPE patch operations in this example, a SCOPE name is required.
SCOPE_NAME = "<SCOPE_NAME>"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Check for existance of Logical Switch Group specified, otherwise stops execution
LOGICAL_SWITCH_GROUP = oneview_client.LOGICAL_SWITCH_GROUPs.get_by('name',
	 LOGICAL_SWITCH_GROUP_NAME)[0]
if LOGICAL_SWITCH_GROUP:
    print('Found logical switch group "%s" with uri: %s' % (LOGICAL_SWITCH_GROUP['name'],
	 LOGICAL_SWITCH_GROUP['uri']))
else:
    raise Exception('Logical switch group "%s" was not found on the appliance.' %
	 LOGICAL_SWITCH_GROUP_NAME)

SWITCH_CONNECTION_PROPERTIES = {
    "connectionProperties": [{
        "propertyName": "SshBasicAuthCredentialUser",
        "value": SSH_USERNAME,
        "valueFormat": "Unknown",
        "valueType": "String"
    }, {
        "propertyName": "SshBasicAuthCredentialPassword",
        "value": SSH_PASSWORD,
        "valueFormat": "SecuritySensitive",
        "valueType": "String"
    }]
}

OPTIONS = {
    "logicalSwitch": {
        "name": "Test Logical Switch",
        "logicalSwitchGroupUri": LOGICAL_SWITCH_GROUP['uri'],
        "switchCredentialConfiguration": [
            {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": SWITCH_IP_1,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }, {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": SWITCH_IP_2,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }
        ]
    },
    "logicalSwitchCredentials": [SWITCH_CONNECTION_PROPERTIES, SWITCH_CONNECTION_PROPERTIES]
}

# Create a Logical Switch
LOGICAL_SWITCH = oneview_client.LOGICAL_SWITCHes.create(OPTIONS)
print("\nCreated Logical Switch '{name}' successfully.\n  uri = '{uri}'".format(**LOGICAL_SWITCH))

# Find the recently created Logical Switch by name
LOGICAL_SWITCH = oneview_client.LOGICAL_SWITCHes.get_by('name', 'Test Logical Switch')[0]
print("\nFound Logical Switch by name: '{name}'.\n  uri = '{uri}'".format(**LOGICAL_SWITCH))

# Update the name of the Logical Switch
OPTIONS_UPDATE = {
    "logicalSwitch": {
        "name": "Renamed Logical Switch",
        "uri": LOGICAL_SWITCH['uri'],
        "switchCredentialConfiguration": LOGICAL_SWITCH['switchCredentialConfiguration'],
        "logicalSwitchGroupUri": LOGICAL_SWITCH_GROUP['uri'],
        "consistencyStatus": "CONSISTENT"
    },
    "logicalSwitchCredentials": [SWITCH_CONNECTION_PROPERTIES, SWITCH_CONNECTION_PROPERTIES]
}
LOGICAL_SWITCH = oneview_client.LOGICAL_SWITCHes.update(OPTIONS_UPDATE)
print("\nUpdated Logical Switch successfully.\n  uri = '{uri}'".format(**LOGICAL_SWITCH))
print("  with attribute name = {name}".format(**LOGICAL_SWITCH))

# Get SCOPE to be added
print("\nGet the SCOPE named '%s'." % SCOPE_NAME)
SCOPE = oneview_client.SCOPEs.get_by_name(SCOPE_NAME)

# Performs a patch operation on the Logical Switch
if SCOPE:
    print("\nPatches the logical switch assigning the '%s' SCOPE to it." % SCOPE_NAME)
    LOGICAL_SWITCH = oneview_client.LOGICAL_SWITCHes.patch(LOGICAL_SWITCH['uri'],
                                                           'replace',
                                                           '/SCOPEUris',
                                                           [SCOPE['uri']])
    pprint(LOGICAL_SWITCH)

# Get all, with defaults
print("\nGet all Logical Switches")
LOGICAL_SWITCHes = oneview_client.LOGICAL_SWITCHes.get_all()
for LOGICAL_SWITCH in LOGICAL_SWITCHes:
    print('  Name: %s' % LOGICAL_SWITCH['name'])

# Get by URI
print("\nGet a Logical Switch by URI")
LOGICAL_SWITCH = oneview_client.LOGICAL_SWITCHes.get(LOGICAL_SWITCH['uri'])
pprint(LOGICAL_SWITCH)

# Reclaim the top-of-rack switches in the logical switch
print("\nReclaim the top-of-rack switches in the logical switch")
LOGICAL_SWITCH = oneview_client.LOGICAL_SWITCHes.refresh(LOGICAL_SWITCH['uri'])
print("  Done.")

# Delete the Logical Switch
oneview_client.LOGICAL_SWITCHes.delete(LOGICAL_SWITCH)
print("\nLogical switch deleted successfully.")
