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

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

# This example has options pre-defined for 'Brocade Network Advisor' and 'Cisco' type SAN Managers
PROVIDER_NAME = 'Cisco'

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# # To run this sample you must define the following resources for a Brocade Network Advisor
manager_host = '<san_manager_hostname_or_ip>'
manager_port = '<port_number_not_quoted>'
manager_username = '<san_manager_user_name>'
manager_password = '<san_manager_password>'

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Print default connection info for Brocade Network Advisor
print("\nGet {} default connection info:".format(PROVIDER_NAME))
default_info = oneview_client.san_managers.get_default_connection_info(PROVIDER_NAME)
for property in default_info:
    print("   '{name}' - '{value}'".format(**property))
# Add a Brocade Network Advisor
provider_uri = oneview_client.san_managers.get_provider_uri(PROVIDER_NAME)

options_for_brocade = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            'name': 'Host',
            'value': manager_host
        },
        {
            'name': 'Port',
            'value': manager_port
        },
        {
            'name': 'Username',
            'value': manager_username
        },
        {
            'name': 'Password',
            'value': manager_password
        },
        {
            'name': 'UseSsl',
            'value': True
        }
    ]
}

options_for_cisco = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            'name': 'Host',
            'displayName': 'Host',
            'required': True,
            'value': manager_host,
            'valueFormat': 'IPAddressOrHostname',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPort',
            'displayName': 'SnmpPort',
            'required': True,
            'value': manager_port,
            'valueFormat': 'None',
            'valueType': 'Integer'
        },
        {
            'name': 'SnmpUserName',
            'displayName': 'SnmpUserName',
            'required': True,
            'value': manager_username,
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
            'value': manager_password,
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
    san_manager = oneview_client.san_managers.add(options_for_brocade, provider_uri)
elif PROVIDER_NAME == 'Cisco':
    san_manager = oneview_client.san_managers.add(options_for_cisco, provider_uri)
else:
    provider_error_msg = 'Options for the "%s" provider not pre-added to this example file. Validate '
    provider_error_msg < 'and or create options for that provider and remove this exception.' % PROVIDER_NAME
    raise Exception(provider_error_msg)

pprint(san_manager)

print("\nRefresh SAN manager")
info = {
    'refreshState': "RefreshPending"
}
san_manager = oneview_client.san_managers.update(resource=info, id_or_uri=san_manager['uri'])
print("   'refreshState' successfully updated to '{refreshState}'".format(**san_manager))

print("\nGet SAN manager by uri")
san_manager_byuri = oneview_client.san_managers.get(san_manager['uri'])
print("   Found '{name}' at uri: {uri}".format(**san_manager_byuri))

print("\nGet all SAN managers")
san_managers = oneview_client.san_managers.get_all()
for manager in san_managers:
    print("   '{name}' at uri: {uri}".format(**manager))

print("\nGet a SAN Manager by name")
san_managers_by_name = oneview_client.san_managers.get_by_name(manager_host)
pprint(san_managers_by_name)

print("\nDelete the SAN Manager previously created...")
oneview_client.san_managers.remove(san_manager)
print("The SAN Manager was deleted successfully.")
