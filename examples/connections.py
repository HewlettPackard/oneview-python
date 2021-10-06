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
from hpeOneView.exceptions import HPEOneViewException
from config_loader import try_load_from_file

# You can use username/password or sessionID for authentication.
# Be sure to inform a valid and active sessionID.
CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
        "sessionID": "<sessionID>"
    }
}


# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

# Get all connections
print("Get all connections")
CONS = ONEVIEW_CLIENT.connections.get_all()
pprint(CONS)

# Get all connections with interconnectUri FILTER
try:
    print("Get connections based on interconnect uri")
    FILTER = "interconnectUri='/rest/interconnects/794079a2-7eb4-4992-8027-e9743a40f5b0'"
    CONS = ONEVIEW_CLIENT.connections.get_all(FILTER=FILTER)
    pprint(CONS)
except HPEOneViewException as err:
    print(err.msg)

# Get first 10 connections, sorted by name
print("Get first 10 connections, sorting by name")
CONS_SORTED = ONEVIEW_CLIENT.connections.get_all(0, 10, sort='name:descending')
pprint(CONS_SORTED)

# Find connection by name
try:
    print("Get connection by name")
    CON_BYNAME = ONEVIEW_CLIENT.connections.get_by(
        'name', "name981375475-1465399560370")
    pprint(CON_BYNAME)
except HPEOneViewException as err:
    print(err.msg)


# Get by Uri
try:
    print("Get connection by uri")
    CON_BYURI = ONEVIEW_CLIENT.connections.get(
        '/rest/connections/58ffb307-3087-4c9d-8574-44e8a79e0d6e')
    pprint(CON_BYURI)
except HPEOneViewException as err:
    print(err.msg)
