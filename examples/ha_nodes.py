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
ha_nodes = oneview_client.ha_nodes

# Get all HA nodes from appliance
print("\nGet all HA nodes from appliance:\n ")
all_nodes = ha_nodes.get_all()
for node in all_nodes:
    print(" - {}".format(node['name']))

# Get HA node by uri from appliance
print("\nGet HA node by uri from appliance\n")
node_by_uri = ha_nodes.get_by_uri(all_nodes[0]['uri'])
pprint(node_by_uri.data)

# update role of HA node
data = {'role': 'Standby'}
ha_node = node_by_uri.update(data)
print("\n## Update HA node successfully!")
pprint(ha_node.data)

# Patch update role
print("\nUpdate the HA node using patch")
ha_node.patch(operation="replace", path="/role", value="Active")
pprint(ha_node.data)

# Delete HA node
ha_node.delete()
print("\n## Delete HA node successfully!")
