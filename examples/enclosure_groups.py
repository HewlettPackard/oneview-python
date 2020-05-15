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


from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

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
enclosure_groups = oneview_client.enclosure_groups

data = {
    "name": "Enclosure Group 1",
    "ipAddressingMode": "External",
    "interconnectBayMappings":
        [
            {
                "interconnectBay": 1,
            },
            {
                "interconnectBay": 2,
            },
            {
                "interconnectBay": 3,
            },
            {
                "interconnectBay": 4,
            },
            {
                "interconnectBay": 5,
            },
            {
                "interconnectBay": 6,
            }
        ]
}

# Get the first 10 records, sorting by name descending
print("Get the ten first Enclosure Groups, sorting by name descending")
egs = enclosure_groups.get_all(0, 10, sort='name:descending')
pprint(egs)

# Get Enclosure Group by scope_uris
if oneview_client.api_version >= 600:
    eg_by_scope_uris = enclosure_groups.get_all(scope_uris="\"'/rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'\"")
    if len(eg_by_scope_uris) > 0:
        print("Found Enclosure Group by scope_uris: '%s'.\n  uri = '%s'" % (eg_by_scope_uris[0]['name'], eg_by_scope_uris[0]['uri']))
        pprint(eg_by_scope_uris)
    else:
        print("No Enclosure Group found.")

# Get all, with default
print("Get all Enclosure Groups")
egs = enclosure_groups.get_all()
pprint(egs)

# Get by uri
print("Get an Enclosure Group by uri")
eg_byuri = enclosure_groups.get_by_uri(egs[0]["uri"])
pprint(eg_byuri.data)

# Get by name
enclosure_group = enclosure_groups.get_by_name(data["name"])
if not enclosure_group:
    # Create a Enclosure Group
    print("Create a Enclosure Group")
    if oneview_client.api_version <= 500:
        options = {"stackingMode": "Enclosure"}
        options.update(data)
        enclosure_group = enclosure_groups.create(options)
    else:
        enclosure_group = enclosure_groups.create(data)
pprint(enclosure_group.data)

# Update an Enclosure Group
resource = enclosure_group.data.copy()
resource["name"] = "Renamed Enclosure Group"
enclosure_group.update(resource)
pprint(enclosure_group.data)

# Update an Enclosure Group Script
# update_script is available for API version 300 in Synery and in all versions in C7000
print("Update an Enclosure Group Script")
script = "#TEST COMMAND"
update_script_result = enclosure_group.update_script(script)
pprint(update_script_result)

# Gets the configuration script of a Enclosure Group
# get_script is available for API version 300 in Synery and in all versions in C7000
print("Gets the configuration script of an Enclosure Group")
script = enclosure_group.get_script()
print(script)

# Delete an Enclosure Group
print("Delete the created Enclosure Group")
enclosure_group.delete()
print("Successfully deleted Enclosure Group")
