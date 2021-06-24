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

# Get node status information from appliance
print("\nGet node status information from appliance:\n ")
node_status = oneview_client.appliance_node_information.get_status()
pprint(node_status)

# Get node version information from appliance
print("\nGet node version information from appliance\n")
node_version = oneview_client.appliance_node_information.get_version()
pprint(node_version)

print("Get appliances High Availability information\n")
ha_info = oneview_client.appliance_node_information.get_ha_info()

print("Get appliance node health status\n")
health_status = oneview_client.appliance_node_information.get_health_status()
