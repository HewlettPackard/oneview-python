# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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

# Set api_version to 600, default is 300 and this API has been introduced since API 600.
CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 600
}

OPTIONS = {
    "type": "Users",
    "userName": "user1239",
    "securityLevel": "Authentication and privacy",
    "authenticationProtocol": "SHA512",
    "authenticationPassphrase": "authPass",
    "privacyProtocol": "AES-256",
    "privacyPassphrase": "1234567812345678"
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
appliance_device_SNMP_V3_USERS = oneview_client.appliance_device_SNMP_V3_USERS

# Add appliance device SNMP v3 users
SNMP_V3_USER = appliance_device_SNMP_V3_USERS.create(OPTIONS)
SNMP_V3_USER_URI = SNMP_V3_USER.data['uri']
print("\n## Create appliance SNMP v3 user successfully!")
pprint(SNMP_V3_USER.data)

# Lists the appliance SNMPv3 users
SNMP_V3_USERS_LIST = appliance_device_SNMP_V3_USERS.get_all()
print("\n## Got appliance SNMP v3 users successfully!")
pprint(SNMP_V3_USERS_LIST)

# Get first element of the List
SNMP_V3_USERS = SNMP_V3_USERS_LIST.pop()

# Get by name
print("\n## Find an SNMPv3 Users by username")
SNMP_V3_USER = appliance_device_SNMP_V3_USERS.get_by_name(SNMP_V3_USER.data['userName'])
pprint(SNMP_V3_USER.data)

# Get by URI
print("Find an SNMP v3 user by URI")
SNMP_V3_USER = appliance_device_SNMP_V3_USERS.get_by_uri(SNMP_V3_USER_URI)
pprint(SNMP_V3_USER.data)

# hange appliance device SNMP v3 Users
SNMPV3_DATA = {"authenticationPassphrase": "newAuthPass", "privacyPassphrase": "8765432187654321"}
SNMP_V3_USER = SNMP_V3_USER.update(SNMPV3_DATA)
print("\n## Update appliance SNMPv3 User successfully!")
pprint(SNMP_V3_USER.data)

# Delete Created Entry
SNMP_V3_USER.delete()
print("\n## Delete appliance SNMP v3 user successfully!")

# Add appliance device SNMP v3 users for Automation
SNMP_V3_USER = appliance_device_SNMP_V3_USERS.create(OPTIONS)
SNMP_V3_USER_URI = SNMP_V3_USER.data['uri']
print("\n## Created appliance SNMP v3 user")
pprint(SNMP_V3_USER.data)
