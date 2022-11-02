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
PROVIDER_NAME = 'Brocade FOS Switch'

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# # To run this sample you must define the following resources for a Brocade Network Advisor
manager_host = '172.18.19.1'
manager_port = '<port_number_not_quoted>'
manager_username = 'dcs'
manager_password = 'dcs'
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
san_providers = oneview_client.san_providers

# Print default connection info for Brocade Network Advisor
print("\nGet {} default connection info:".format(PROVIDER_NAME))
default_info = san_providers.get_default_connection_info(PROVIDER_NAME)

for property in default_info:
    print("   '{name}' - '{value}'".format(**property))
# Add a Brocade Network Advisor

provider_uri = san_providers.get_provider_uri(PROVIDER_NAME)
print(provider_uri)


options_for_brocade = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            "name": "Host",
            "displayName": "Host",
            "required": True,
            "value": manager_host,
            "valueType": "String",
            "valueFormat": "IPAddressOrHostname"
        },
        {
            "name": "Username",
            "displayName": "Username",
            "required": True,
            "value": manager_username,
            "valueType": "String",
            "valueFormat": "None"
        },
        {
            "name": "Password",
            "displayName": "Password",
            "required": True,
            "value": manager_password,
            "valueType": "String",
            "valueFormat": "SecuritySensitive"
        },
        {
            "name": "UseHttps",
            "displayName": "UseHttps",
            "required": True,
            "value": True,
            "valueType": "Boolean",
            "valueFormat": "None"
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
print("nope")
print(provider_uri)
if PROVIDER_NAME == 'Brocade FOS Switch':
    san_manager = san_providers.add(options_for_brocade, provider_uri)
elif PROVIDER_NAME == 'Cisco':
    san_manager = san_providers.add(options_for_cisco, provider_uri)
else:
    provider_error_msg = 'Options for the "%s" provider not pre-added to this example file. Validate '
    provider_error_msg < 'and or create options for that provider and remove this exception.' % PROVIDER_NAME
    raise Exception(provider_error_msg)

pprint(san_manager)
