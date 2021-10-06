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
from config_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
ONEVIEW_CLIENT = OneViewClient(CONFIG)
HA_NODES = ONEVIEW_CLIENT.ha_nodes

# Get all HA nodes from appliance
print("\nGet all HA nodes from appliance:\n ")
ALL_NODES = HA_NODES.get_all()
for node in ALL_NODES:
    print(" - {}".format(node['name']))

# Get HA node by uri from appliance
print("\nGet HA node by uri from appliance\n")
NODE_BY_URI = HA_NODES.get_by_uri(ALL_NODES[0]['uri'])
pprint(NODE_BY_URI.DATA)

# update role of HA node
DATA = {'role': 'Standby'}
HA_NODE = NODE_BY_URI.update(DATA)
print("\n## Update HA node successfully!")
pprint(HA_NODE.DATA)

# Patch update role
print("\nUpdate the HA node using patch")
HA_NODE.patch(operation="replace", path="/role", value="Active")
pprint(HA_NODE.DATA)

# Delete HA node
HA_NODE.delete()
print("\n## Delete HA node successfully!")
