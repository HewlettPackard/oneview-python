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
logical_interconnect_groups = oneview_client.logical_interconnect_groups
interconnect_types = oneview_client.interconnect_types

# Define the scope name to add the logical interconnect group to it
scope_name = ""

interconnect_type_name = "Synergy 10Gb Interconnect Link Module"
# Get the interconnect type by name and using the uri in the values for the fields
# "permittedInterconnectTypeUri" and create a Logical Interconnect Group.
# Note: If this type does not exist, select another name
interconnect_type = oneview_client.interconnect_types.get_by_name(interconnect_type_name)
if interconnect_type:
    pprint(interconnect_type.data)
    interconnect_type_url = interconnect_type.data["uri"]

options = {
    "category": None,
    "created": None,
    "description": None,
    "eTag": None,
    "uplinkSets": [],
    "modified": None,
    "name": "OneView Test Logical Interconnect Group",
    "state": "Active",
    "status": None,
    "enclosureType": "C7000",
    "interconnectMapTemplate": {
        "interconnectMapEntryTemplates": [
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": "1",
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type_url
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": "2",
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type_url
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 3,
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": None
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 4,
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }]
                },
                "permittedInterconnectTypeUri": None
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 5,
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": None
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 6,
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": None
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 7,
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": None
            },
            {
                "logicalDownlinkUri": None,
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "relativeValue": 8,
                            "type": "Bay"
                        },
                        {
                            "relativeValue": 1,
                            "type": "Enclosure"
                        }
                    ]
                },
                "permittedInterconnectTypeUri": None
            }
        ]
    }
}

# Get all, with defaults
print("Get all Logical Interconnect Groups")
ligs = logical_interconnect_groups.get_all()
pprint(ligs)

# Get by uri
print("Get a Logical Interconnect Group by uri")
lig_byuri = logical_interconnect_groups.get_by_uri(ligs[0]["uri"])
pprint(lig_byuri.data)

# Get the first 10 records, sorting by name descending, filtering by name
print("Get the first Logical Interconnect Groups, sorting by name descending, filtering by name")
ligs = logical_interconnect_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Interconnect Group'\"")
pprint(ligs)

# Get Logical Interconnect Group by property
lig = logical_interconnect_groups.get_by('name', 'LIG')[0]
print("Found lig by name: '%s'.\n  uri = '%s'" % (lig['name'], lig['uri']))

# Get Logical Interconnect Group by scope_uris
if oneview_client.api_version >= 600:
    lig_by_scope_uris = logical_interconnect_groups.get_all(scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
    if len(lig_by_scope_uris) > 0:
        print("Found %d Logical Interconnect Groups" % (len(lig_by_scope_uris)))
        i = 0
        while i < len(lig_by_scope_uris):
            print("Found Logical Interconnect Group by scope_uris: '%s'.\n  uri = '%s'" % (lig_by_scope_uris[i]['name'], lig_by_scope_uris[i]['uri']))
            i += 1
        pprint(lig_by_scope_uris)
    else:
        print("No Logical Interconnect Group found.")

# Get logical interconnect group by name
lig = logical_interconnect_groups.get_by_name(options["name"])
if not lig:
    # Create a logical interconnect group
    print("Create a logical interconnect group")
    lig = logical_interconnect_groups.create(options)
    pprint(lig.data)

# Update a logical interconnect group
print("Update a logical interconnect group")
lig_to_update = lig.data.copy()
lig_to_update["name"] = "Renamed Logical Interconnect Group"
lig.update(lig_to_update)
pprint(lig.data)

# Performs a patch operation
if oneview_client.api_version <= 500:
    scope = oneview_client.scopes.get_by_name(scope_name)
    if scope:
        print("\nPatches the logical interconnect group adding one scope to it")
        updated_lig = lig.patch('replace',
                                '/scopeUris',
                                [scope['uri']])
        pprint(updated_lig.data)

# Get default settings
print("Get the default interconnect settings for a logical interconnect group")
lig_default_settings = lig.get_default_settings()
pprint(lig_default_settings)

# Get settings
print("Gets the interconnect settings for a logical interconnect group")
lig_settings = lig.get_settings()
pprint(lig_settings)

# Delete a logical interconnect group
print("Delete the created logical interconnect group")
lig.delete()
print("Successfully deleted logical interconnect group")
