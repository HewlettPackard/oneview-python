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
switch_types = oneview_client.switch_types

# Get all supported switch types
print("\nGet all supported switch types:")
switch_types_all = switch_types.get_all()
pprint(switch_types_all, depth=2)

# Get all sorting by name descending
print("\nGet all switch-types sorting by name:")
switch_types_sorted = switch_types.get_all(
    sort='name:descending')
pprint(switch_types_sorted, depth=2)

if switch_types_all:
    # Get by name
    print("\nGet a switch_types by name:")
    switch_type_byname = switch_types.get_by_name(switch_types_all[0]['name'])
    pprint(switch_type_byname.data, depth=1)
