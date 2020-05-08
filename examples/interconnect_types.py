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
# Below example works till Oneview API version 1600.

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
interconnect_types = oneview_client.interconnect_types

# Get all supported interconnect types
print("Get all supported interconnect types")
interconnect_types = interconnect_types.get_all()
pprint(interconnect_types, depth=2)

# Get all sorting by name descending
print("Get all interconnect-types sorting by name")
interconnect_types_sorted = oneview_client.interconnect_types.get_all(sort='name:descending')
pprint(interconnect_types_sorted, depth=2)

# Get by name
print("Get an interconnect_type by name")
name = interconnect_types_sorted[0]["name"]
interconnect_type_byname = oneview_client.interconnect_types.get_by_name(name)
pprint(interconnect_type_byname.data, depth=1)
