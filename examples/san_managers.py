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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

# This example has options pre-defined for 'Brocade Network Advisor' and 'Cisco' type SAN Managers
PROVIDER_NAME = 'Cisco'

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# # To run this sample you must define the following resources for a Brocade Network Advisor
MANAGER_HOST = '<san_MANAGER_HOSTname_or_ip>'
MANAGER_PORT = '<port_number_not_quoted>'
MANAGER_USERNAME = '<san_manager_user_name>'
MANAGER_PASSWORD = '<san_MANAGER_PASSWORD>'

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Print default connection INFO for Brocade Network Advisor
print("\nGet {} default connection INFO:".format(PROVIDER_NAME))
default_INFO = oneview_client.san_managers.get_default_connection_INFO(PROVIDER_NAME)
for property in default_INFO:
    print("   '{name}' - '{value}'".format(**property))
# Add a Brocade Network Advisor
provider_uri = oneview_client.san_managers.get_provider_uri(PROVIDER_NAME)

OPTIONS_FOR_BROCADE = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            'name': 'Host',
            'value': MANAGER_HOST
        },
        {
            'name': 'Port',
            'value': MANAGER_PORT
        },
        {
            'name': 'Username',
            'value': MANAGER_USERNAME
        },
        {
            'name': 'Password',
            'value': MANAGER_PASSWORD
        },
        {
            'name': 'UseSsl',
            'value': True
        }
    ]
}

OPTIONS_FOR_CISCO = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            'name': 'Host',
            'displayName': 'Host',
            'required': True,
            'value': MANAGER_HOST,
            'valueFormat': 'IPAddressOrHostname',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPort',
            'displayName': 'SnmpPort',
            'required': True,
            'value': MANAGER_PORT,
            'valueFormat': 'None',
            'valueType': 'Integer'
        },
        {
            'name': 'SnmpUserName',
            'displayName': 'SnmpUserName',
            'required': True,
            'value': MANAGER_USERNAME,
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpAuthLevel',
            'displayName': 'SnmpAuthLevel',
            'required': True,
            'value': 'authnopriv',
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpAuthProtocol',
            'displayName': 'SnmpAuthProtocol',
            'required': False,
            'value': 'sha',
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpAuthString',
            'displayName': 'SnmpAuthString',
            'required': False,
            'value': MANAGER_PASSWORD,
            'valueFormat': 'SecuritySensitive',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPrivProtocol',
            'displayName': 'SnmpPrivProtocol',
            'required': False,
            'value': '',
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPrivString',
            'displayName': 'SnmpPrivString',
            'required': False,
            'value': '',
            'valueFormat': 'SecuritySensitive',
            'valueType': 'String'
        }
    ]
}

if PROVIDER_NAME == 'Brocade Network Advisor':
    san_manager = oneview_client.san_managers.add(OPTIONS_FOR_BROCADE, provider_uri)
elif PROVIDER_NAME == 'Cisco':
    san_manager = oneview_client.san_managers.add(OPTIONS_FOR_CISCO, provider_uri)
else:
    PROVIDER_ERROR_MSG = 'Options for the "%s" provider not pre-added to this example file. Validate
	 '
    PROVIDER_ERROR_MSG < 'and or create options for that provider and remove this exception.' % PROVIDER_NAME
    raise Exception(PROVIDER_ERROR_MSG)

pprint(san_manager)

print("\nRefresh SAN manager")
INFO = {
    'refreshState': "RefreshPending"
}
san_manager = oneview_client.san_managers.update(resource=INFO, id_or_uri=san_manager['uri'])
print("   'refreshState' successfully updated to '{refreshState}'".format(**san_manager))

print("\nGet SAN manager by uri")
san_manager_byuri = oneview_client.san_managers.get(san_manager['uri'])
print("   Found '{name}' at uri: {uri}".format(**san_manager_byuri))

print("\nGet all SAN managers")
san_managers = oneview_client.san_managers.get_all()
for manager in san_managers:
    print("   '{name}' at uri: {uri}".format(**manager))

print("\nGet a SAN Manager by name")
san_managers_by_name = oneview_client.san_managers.get_by_name(MANAGER_HOST)
pprint(san_managers_by_name)

print("\nDelete the SAN Manager previously created...")
oneview_client.san_managers.remove(san_manager)
print("The SAN Manager was deleted successfully.")
