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
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
        "sessionID": "<sessionID>"
    }
}


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all connections
print("Get all connections")
cons = oneview_client.connections.get_all()
pprint(cons)

# Get all connections with interconnectUri filter
try:
    print("Get connections based on interconnect uri")
    filter = "interconnectUri='/rest/interconnects/794079a2-7eb4-4992-8027-e9743a40f5b0'"
    cons_interconnectUri = oneview_client.connections.get_all(filter=filter)
    pprint(cons_interconnectUri)
except HPEOneViewException as e:
    print(e.msg)

# Get first 10 connections, sorted by name
print("Get first 10 connections, sorting by name")
cons_sorted = oneview_client.connections.get_all(0, 10, sort='name:descending')
pprint(cons_sorted)

# Find connection by name
try:
    print("Get connection by name")
    con_byName = oneview_client.connections.get_by(
        'name', "name981375475-1465399560370")
    pprint(con_byName)
except HPEOneViewException as e:
    print(e.msg)


# Get by Uri
try:
    print("Get connection by uri")
    con_byUri = oneview_client.connections.get(
        '/rest/connections/58ffb307-3087-4c9d-8574-44e8a79e0d6e')
    pprint(con_byUri)
except HPEOneViewException as e:
    print(e.msg)
