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
# Below example works till Oneview API Version 1600.

from pprint import pprint

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

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
scopes = oneview_client.scopes
ethernet_networks = oneview_client.ethernet_networks
fc_networks = oneview_client.fc_networks

# Define the scope name to add the logical interconnect group to it
iscsi_network = "iscsi_nw"  # iscsi network for image streamer uplinkset
mgmt_untagged = "mgmt_nw"  # untagged managament network
fc_fabric = "FC_fabric_nw"  # Fabric attach FC network
scope_name = "test_scope"
interconnect_type_name1 = "Virtual Connect SE 40Gb F8 Module for Synergy"
interconnect_type_name2 = "Synergy 20Gb Interconnect Link Module"

# Get the interconnect type by name and using the uri in the values for the fields
# "permittedInterconnectTypeUri" and create a Logical Interconnect Group.
# Note: If this type does not exist, select another name
interconnect_type_1 = interconnect_types.get_by_name(interconnect_type_name1)
interconnect_type_2 = interconnect_types.get_by_name(interconnect_type_name2)
interconnect_type1_uri = interconnect_type_1.data["uri"]
interconnect_type2_uri = interconnect_type_2.data["uri"]

# Get the ethernet network uri by name
eth_nw1 = ethernet_networks.get_by_name(iscsi_network)
iscsi_network_uri = eth_nw1.data['uri']
eth_nw2 = ethernet_networks.get_by_name(mgmt_untagged)
mgmt_untagged_uri = eth_nw2.data['uri']
fc_nw = fc_networks.get_by_name(fc_fabric)
fc_network_uri = fc_nw.data['uri']

# Create scope
scope_options = {
    "name": scope_name,
    "description": "Sample Scope description"
}
scope = scopes.get_by_name(scope_options["name"])
if scope:
    print("Scope '{}' already exists".format(scope_name))
else:
    print("Creating the scope '{}'".format(scope_name))
    scope = scopes.create(scope_options)

# LIG payload
options = {
    "name": "LIG",
    "interconnectMapTemplate": {
        "interconnectMapEntryTemplates": [
            {
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "type": "Bay",
                            "relativeValue": 3
                        },
                        {
                            "type": "Enclosure",
                            "relativeValue": 1
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type1_uri,
                "enclosureIndex": 1
            },
            {
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "type": "Bay",
                            "relativeValue": 6
                        },
                        {
                            "type": "Enclosure",
                            "relativeValue": 2
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type1_uri,
                "enclosureIndex": 2
            },
            {
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "type": "Bay",
                            "relativeValue": 6
                        },
                        {
                            "type": "Enclosure",
                            "relativeValue": 1
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type2_uri,
                "enclosureIndex": 1
            },
            {
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "type": "Bay",
                            "relativeValue": 3
                        },
                        {
                            "type": "Enclosure",
                            "relativeValue": 2
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type2_uri,
                "enclosureIndex": 2
            },
            {
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "type": "Bay",
                            "relativeValue": 3
                        },
                        {
                            "type": "Enclosure",
                            "relativeValue": 3
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type2_uri,
                "enclosureIndex": 3
            },
            {
                "logicalLocation": {
                    "locationEntries": [
                        {
                            "type": "Bay",
                            "relativeValue": 6
                        },
                        {
                            "type": "Enclosure",
                            "relativeValue": 3
                        }
                    ]
                },
                "permittedInterconnectTypeUri": interconnect_type2_uri,
                "enclosureIndex": 3
            }
        ]
    },
    "uplinkSets": [
        {
            "networkType": "FibreChannel",
            "networkUris": [fc_network_uri],
            "mode": "Auto",
            "name": "FC_fabric",
            "logicalPortConfigInfos": [
                {
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "type": "Bay",
                                "relativeValue": 3
                            },
                            {
                                "type": "Enclosure",
                                "relativeValue": 1
                            },
                            {
                                "type": "Port",
                                "relativeValue": 68
                            }
                        ]
                    },
                    "desiredSpeed": "Auto",
                    "desiredFecMode": "Auto"
                },
                {
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "type": "Bay",
                                "relativeValue": 3
                            },
                            {
                                "type": "Enclosure",
                                "relativeValue": 1
                            },
                            {
                                "type": "Port",
                                "relativeValue": 73
                            }
                        ]
                    },
                    "desiredSpeed": "Auto",
                    "desiredFecMode": "Auto"
                }
            ],
            "ethernetNetworkType": "NotApplicable",
        },
        {
            "networkUris": [iscsi_network_uri],
            "mode": "Auto",
            "logicalPortConfigInfos": [
                {
                    "desiredSpeed": "Auto",
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "relativeValue": 82,
                                "type": "Port"
                            },
                            {
                                "relativeValue": 3,
                                "type": "Bay"
                            },
                            {
                                "relativeValue": 1,
                                "type": "Enclosure"
                            }
                        ]
                    }
                },
                {
                    "desiredSpeed": "Auto",
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "relativeValue": 87,
                                "type": "Port"
                            },
                            {
                                "relativeValue": 3,
                                "type": "Bay"
                            },
                            {
                                "relativeValue": 1,
                                "type": "Enclosure"
                            }
                        ]
                    }
                },
                {
                    "desiredSpeed": "Auto",
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "relativeValue": 82,
                                "type": "Port"
                            },
                            {
                                "relativeValue": 6,
                                "type": "Bay"
                            },
                            {
                                "relativeValue": 2,
                                "type": "Enclosure"
                            }
                        ]
                    }
                },
                {
                    "desiredSpeed": "Auto",
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "relativeValue": 88,
                                "type": "Port"
                            },
                            {
                                "relativeValue": 6,
                                "type": "Bay"
                            },
                            {
                                "relativeValue": 2,
                                "type": "Enclosure"
                            }
                        ]
                    }
                }
            ],
            "networkType": "Ethernet",
            "ethernetNetworkType": "ImageStreamer",
            "name": "deploy"
        },
        {
            "networkUris": [mgmt_untagged_uri],
            "mode": "Auto",
            "logicalPortConfigInfos": [
                {
                    "desiredSpeed": "Auto",
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "type": "Bay",
                                "relativeValue": 3
                            },
                            {
                                "type": "Port",
                                "relativeValue": 62
                            },
                            {
                                "type": "Enclosure",
                                "relativeValue": 1
                            }
                        ]
                    }
                },
                {
                    "desiredSpeed": "Auto",
                    "logicalLocation": {
                        "locationEntries": [
                            {
                                "type": "Bay",
                                "relativeValue": 6
                            },
                            {
                                "type": "Port",
                                "relativeValue": 62
                            },
                            {
                                "type": "Enclosure",
                                "relativeValue": 2
                            }
                        ]
                    }
                }
            ],
            "networkType": "Ethernet",
            "ethernetNetworkType": "Untagged",
            "name": "mgmt"
        }
    ],
    "enclosureType": "SY12000",
    "enclosureIndexes": [1, 2, 3],
    "interconnectBaySet": "3",
    "redundancyType": "HighlyAvailable"
}

# Get logical interconnect group by name
lig = logical_interconnect_groups.get_by_name(options["name"])
if not lig:
    # Create a logical interconnect group
    print("Create a logical interconnect group")
    lig = logical_interconnect_groups.create(options)
    print("Created logical interconnect group with name - '{}' and uri - '{}'".format(lig.data['name'], lig.data['uri']))

# Get all, with defaults
print("Get all Logical Interconnect Groups")
ligs = logical_interconnect_groups.get_all()
for lig_each in ligs:
    print(" - {}".format(lig_each['name']))

# Get by uri
print("Get a Logical Interconnect Group by uri")
lig_by_uri = logical_interconnect_groups.get_by_uri(ligs[0]["uri"])
pprint(lig_by_uri.data)

# Get the first 10 records, sorting by name descending, filtering by name
print("Get the first Logical Interconnect Groups, sorting by name descending, filtering by name")
ligs = logical_interconnect_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Interconnect Group'\"")
for lig_each in ligs:
    print(" - {}".format(lig_each['name']))

# Get Logical Interconnect Group by property
lig_prop = logical_interconnect_groups.get_by('name', 'LIG')[0]
print("Found lig by name: '%s'.\n  uri = '%s'" % (lig_prop['name'], lig_prop['uri']))

# Get Logical Interconnect Group by scope_uris
if oneview_client.api_version >= 600:
    lig_by_scope_uris = logical_interconnect_groups.get_all(scope_uris=scope.data['uri'])
    if len(lig_by_scope_uris) > 0:
        print("Found {} Logical Interconnect Groups".format(len(lig_by_scope_uris)))
        for lig_scope in lig_by_scope_uris:
            print("Found Logical Interconnect Group by scope_uris: '{}'.\n  uri = '{}'".format(lig_scope['name'], lig_scope['uri']))
    else:
        print("No Logical Interconnect Group found.")

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
                                [scope.data['uri']])
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

# Create a logical interconnect group for automation
print("Create a logical interconnect group as a pre-requisite for LE creation")
lig = logical_interconnect_groups.create(options)
print("Created logical interconnect group with name - '{}' and uri - '{}'".format(lig.data['name'], lig.data['uri']))
