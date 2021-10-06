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

# This resource is only available on C7000 enclosures

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run the scope patch operations in this example, a scope name is required.
SCOPE_NAME = "test"

OPTIONS = {
    "name": "OneView Test Logical Switch Group",
    "switchMapTemplate": {
        "switchMapEntryTemplates": [{
            "logicalLocation": {
                "locationEntries": [{
                    "relativeValue": 1,
                    "type": "StackingMemberId"
                }]
            },
            "permittedSwitchTypeUri": ""
        }]
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
logical_switch_groups = oneview_client.logical_switch_groups
SWITCH_TYPEs = oneview_client.SWITCH_TYPEs

# Get all, with defaults
print("\nGet all Logical Switch Groups")
LSGS = logical_switch_groups.get_all()
for LSG in LSGS:
    print("   '{name}' at uri: '{uri}'".format(**LSG))

# Get the first 10 records, sorting by name descending, filtering by name
print("\nGet the first Logical Switch Groups, sorting by name descending, filtering by name")
LSGS = logical_switch_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Switch Group'\"")
for LSG in LSGS:
    print("   '{name}' at uri: '{uri}'".format(**LSG))

# Get Logical Switch by property
LSG_GETBY = logical_switch_groups.get_by('name', 'OneView Test Logical Switch Group')
if LSG_GETBY:
    print("\nFound logical switch group by name: '{name}' at uri = '{uri}'".format(**LSG_GETBY[0]))

    print("\nGet a Logical Switch Group by uri")
    LSG_BYURI = logical_switch_groups.get_by_uri(LSG_GETBY[0]["uri"])
    print("   Found logical switch group '{name}' by uri '{uri}'".format(**LSG_BYURI.data))

# Get switch type to use in creation of logical switch group
print("\nGet switch type to use in creation of logical switch group")
SWITCH_TYPE = SWITCH_TYPEs.get_by_name("Arista 7060X")
print("   Found switch type at uri: '{}'".format(SWITCH_TYPE.data['uri']))

LSG = logical_switch_groups.get_by_name(OPTIONS["name"])
if not LSG:
    # Create a logical switch group
    print("\nCreate a logical switch group")
    OPTIONS['switchMapTemplate']['switchMapEntryTemplates'][0]['permittedSwitchTypeUri'] =
	 SWITCH_TYPE.data['uri']
    LSG = oneview_client.logical_switch_groups.create(OPTIONS)
    print("   Created logical switch group '{name}' at uri: '{uri}'".format(**LSG.data))

# Update a logical switch group
print("\nUpdate the name of a logical switch group")
LSG_TO_UPDATE = LSG.data.copy()
LSG_TO_UPDATE["name"] = "Renamed Logical Switch Group"
LSG.update(LSG_TO_UPDATE)
print("   Successfully updated logical switch group with name '{name}'".format(**LSG.data))

# Update a logical switch group by adding another switch with a relative value of 2
print("\nUpdate a logical switch group by adding another switch with a relative value of 2")
LSG_TO_UPDATE = LSG.data.copy()
SWITCH_OPTIONS = {
    "logicalLocation": {
        "locationEntries": [{
            "relativeValue": 2,
            "type": "StackingMemberId",
        }]
    },
    "permittedSwitchTypeUri": SWITCH_TYPE.data['uri']
}
LSG_TO_UPDATE['switchMapTemplate']['switchMapEntryTemplates'].append(SWITCH_OPTIONS)
LSG.update(LSG_TO_UPDATE)
pprint(LSG.data)

# Get scope to be added
print("\nGet the scope named '%s'." % SCOPE_NAME)
scope = oneview_client.scopes.get_by_name(SCOPE_NAME)

# Performs a patch operation on the Logical Switch Group
if scope and oneview_client.api_version <= 500:
    print("\nPatches the logical switch group assigning the '%s' scope to it." % SCOPE_NAME)
    LSG.patch('replace',
              '/scopeUris',
              [scope['uri']])
    pprint(LSG.data)

# Delete a logical switch group
print("\nDelete the created logical switch group")
LSG.delete()
print("   Successfully deleted logical switch group")
