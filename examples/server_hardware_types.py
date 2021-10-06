# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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
# Below example version works till Oneview API Version 1600.

from pprint import pprint
from hpeOneView.oneview_client import OneViewClient
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
SERVER_HARDWARE_TYPEs = oneview_client.SERVER_HARDWARE_TYPEs

# Get the first 10 records, sorting by name descending
print("\nGet the first 10 server hardware types, sorting by name descending, filtering by name")
SERVER_HARDWARE_TYPES_ALL = SERVER_HARDWARE_TYPEs.get_all(0, 10, sort='name:descending')
for sht in SERVER_HARDWARE_TYPES_ALL:
    print(" - {}".format(sht['name']))

# Get all, with defaults
print("\nGet all server hardware types")
SERVER_HARDWARE_TYPES_ALL = SERVER_HARDWARE_TYPEs.get_all()
for sht in SERVER_HARDWARE_TYPES_ALL:
    print(" - {}".format(sht['name']))

# Get by uri
print("\nGet a Server Hardware Type by uri")
SERVER_HARDWARE_TYPE_BY_URI = SERVER_HARDWARE_TYPEs.get_by_uri(SERVER_HARDWARE_TYPES_ALL[0]["uri"])
pprint(SERVER_HARDWARE_TYPE_BY_URI.data, depth=2)

# Get by name and UPDATE
print("\nGet a Server Hardware Type by name")
SERVER_HARDWARE_TYPE = SERVER_HARDWARE_TYPEs.get_by_name("SY 480 Gen9 2")
pprint(SERVER_HARDWARE_TYPE.data, depth=2)
UPDATE = {
    'description': "Updated Description"
}
if SERVER_HARDWARE_TYPE:
    SERVER_HARDWARE_TYPE.UPDATE(UPDATE)
    print("\nServer Hardware type '{}' UPDATEd: \n 'description': '{}'".format(
        SERVER_HARDWARE_TYPE.data['name'],
        SERVER_HARDWARE_TYPE.data['description']))
