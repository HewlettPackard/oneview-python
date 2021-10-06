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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

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

DATACENTER_INFORMATION = {
    "name": "MyDatacenter",
    "width": 5000, "depth": 5000
}

# Add a Datacenter
datacenter_added = oneview_client.datacenters.add(DATACENTER_INFORMATION)
print("\nAdded Datacenter '{name}' successfully\n".format(**datacenter_added))

# Retrieve Datacenter by URI
datacenter = oneview_client.datacenters.get(datacenter_added['uri'])
print("\nGet Datacenter by URI: retrieved '{name}' successfully\n".format(**datacenter))

# Update the Datacenter
datacenter['name'] = "New Datacenter Name"
datacenter = oneview_client.datacenters.update(datacenter)
print("\nDatacenter '{name}' updated successfully\n".format(**datacenter))

# Get the Datacenter by name
datacenter_list = oneview_client.datacenters.get_by('name', "New Datacenter Name")
print("\nGet Datacenter device by name: '{name}'\n".format(**datacenter))

# Get the Datacenter visual content
print("Getting the Datacenter visual content...")
datacenter_visual_content = oneview_client.datacenters.get_visual_content(datacenter['uri'])
pprint(datacenter_visual_content)

# Remove added Datacenter
oneview_client.datacenters.remove(datacenter)
print("\nSuccessfully removed the datacenter")

# Add a datacenter again and call Remove All
datacenter_added = oneview_client.datacenters.add(DATACENTER_INFORMATION)
oneview_client.datacenters.remove_all(filter="name matches '%'")
print("\nSuccessfully removed all datacenters")
