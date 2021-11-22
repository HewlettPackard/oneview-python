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
DATACENTER_ADDED = oneview_client.DATACENTERs.add(DATACENTER_INFORMATION)
print("\nAdded Datacenter '{name}' successfully\n".format(**DATACENTER_ADDED))

# Retrieve Datacenter by URI
DATACENTER = oneview_client.DATACENTERs.get(DATACENTER_ADDED['uri'])
print("\nGet Datacenter by URI: retrieved '{name}' successfully\n".format(**DATACENTER))

# Update the Datacenter
DATACENTER['name'] = "New Datacenter Name"
DATACENTER = oneview_client.DATACENTERs.update(DATACENTER)
print("\nDatacenter '{name}' updated successfully\n".format(**DATACENTER))

# Get the Datacenter by name
DATACENTER_list = oneview_client.DATACENTERs.get_by('name', "New Datacenter Name")
print("\nGet Datacenter device by name: '{name}'\n".format(**DATACENTER))

# Get the Datacenter visual content
print("Getting the Datacenter visual content...")
DATACENTER_visual_content = oneview_client.DATACENTERs.get_visual_content(DATACENTER['uri'])
pprint(DATACENTER_visual_content)

# Remove added Datacenter
oneview_client.DATACENTERs.remove(DATACENTER)
print("\nSuccessfully removed the DATACENTER")

# Add a DATACENTER again and call Remove All
DATACENTER_ADDED = oneview_client.DATACENTERs.add(DATACENTER_INFORMATION)
oneview_client.DATACENTERs.remove_all(filter="name matches '%'")
print("\nSuccessfully removed all DATACENTERs")
