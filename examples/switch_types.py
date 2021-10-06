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
switch_types = oneview_client.switch_types

# Get all supported switch types
print("\nGet all supported switch types:")
SWITCH_TYPES_ALL = switch_types.get_all()
pprint(SWITCH_TYPES_ALL, depth=2)

# Get all sorting by name descending
print("\nGet all switch-types sorting by name:")
SWITCH_TYPES_SORTED = switch_types.get_all(
    sort='name:descending')
pprint(SWITCH_TYPES_SORTED, depth=2)

if SWITCH_TYPES_ALL:
    # Get by name
    print("\nGet a switch_types by name:")
    SWITCH_TYPE_BYNAME = switch_types.get_by_name(SWITCH_TYPES_ALL[0]['name'])
    pprint(SWITCH_TYPE_BYNAME.data, depth=1)
