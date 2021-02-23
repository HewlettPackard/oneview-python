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
from config_loader import try_load_from_file

# Set api_version to 600, default is 300 and this API has been introduced since API 600.
config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    },
    "api_version": 
}

options = {
    "type": "Users",
    "userName": "user123456",
    "securityLevel": "Authentication and privacy",
    "authenticationProtocol": "SHA512",
    "authenticationPassphrase": "authPass",
    "privacyProtocol": "AES-256",
    "privacyPassphrase": "1234567812345678"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Add appliance device SNMP v3 users
snmp_v3_user = oneview_client.appliance_device_snmp_v3_users.create(options)
snmp_v3_user_uri = snmp_v3_user.data['uri']
print("\n## Create appliance SNMP v3 user successfully!")
pprint(snmp_v3_user)

# Lists the appliance SNMPv3 users
snmp_v3_users_list = oneview_client.appliance_device_snmp_v3_users.get_all()
print("\n## Got appliance SNMP v3 users successfully!")
pprint(snmp_v3_users_list)

# Get first element of the List
snmp_v3_users = snmp_v3_users_list.pop()

# Get by URI
print("Find an SNMP v3 user by URI")
snmp_v3_user = oneview_client.appliance_device_snmp_v3_users.get_by_uri(snmp_v3_user_uri)
pprint(snmp_v3_user)


snmpv3_data = {"authenticationPassphrase": "newAuthPass", "privacyPassphrase": "8765432187654321"}
snmp_v3_user = snmp_v3_user.update(snmpv3_data)
print("\n## Update appliance SNMPv3 User successfully!")
pprint(snmp_v3_user.data)

# Delete Created Entry
snmp_v3_user.delete()
print("\n## Delete appliance SNMP v3 user successfully!")
