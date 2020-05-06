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
# Below example version works till Oneview API Version 1600.

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
server_hardware_types = oneview_client.server_hardware_types

# Get the first 10 records, sorting by name descending
print("\nGet the first 10 server hardware types, sorting by name descending, filtering by name")
server_hardware_types_all = server_hardware_types.get_all(0, 10, sort='name:descending')
pprint(server_hardware_types_all, depth=2)

# Get all, with defaults
print("\nGet all server hardware types")
server_hardware_types_all = server_hardware_types.get_all()
pprint(server_hardware_types_all, depth=3)

# Get by uri
print("\nGet a Server Hardware Type by uri")
server_hardware_type_by_uri = server_hardware_types.get_by_uri(server_hardware_types_all[0]["uri"])
pprint(server_hardware_type_by_uri.data, depth=2)

# Get by name and update
print("\nGet a Server Hardware Type by name")
server_hardware_type = server_hardware_types.get_by_name("SY 480 Gen9 2")
pprint(server_hardware_type.data, depth=2)
update = {
    'description': "Updated Description"
}
server_hardware_type.update(update)
print("\nServer Hardware type '{}' updated: \n 'description': '{}'".format(
    server_hardware_type.data['name'],
    server_hardware_type.data['description']))
