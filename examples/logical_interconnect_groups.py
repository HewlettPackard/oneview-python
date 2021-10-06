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
# Below example works till Oneview API Version 1600.

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
logical_interconnect_groups = oneview_client.logical_interconnect_groups
interconnect_types = oneview_client.interconnect_types
SCOPEs = oneview_client.SCOPEs
ethernet_networks = oneview_client.ethernet_networks
fc_networks = oneview_client.fc_networks

# Define the SCOPE name to add the logical interconnect group to it
ISCSI_NETWORK = "iscsi_nw"  # iscsi network for image streamer uplinkset
MGMT_UNTAGGED = "mgmt_nw"  # untagged managament network
FC_FABRIC = "FC_fabric_nw"  # Fabric attach FC network
SCOPE_NAME = "test_SCOPE"
INTERCONNECT_TYPE_NAME1 = "Virtual Connect SE 40Gb F8 Module for Synergy"
INTERCONNECT_TYPE_NAME2 = "Synergy 20Gb Interconnect Link Module"

# Get the interconnect type by name and using the uri in the values for the fields
# "permittedInterconnectTypeUri" and create a Logical Interconnect Group.
# Note: If this type does not exist, select another name
INTERCONNECT_TYPE_1 = interconnect_types.get_by_name(INTERCONNECT_TYPE_NAME1)
INTERCONNECT_TYPE_2 = interconnect_types.get_by_name(INTERCONNECT_TYPE_NAME2)
INTERCONNECT_TYPE1_URI = INTERCONNECT_TYPE_1.data["uri"]
INTERCONNECT_TYPE2_URI = INTERCONNECT_TYPE_2.data["uri"]

# Get the ethernet network uri by name
ETH_NW1 = ethernet_networks.get_by_name(ISCSI_NETWORK)
ISCSI_NETWORK_URI = ETH_NW1.data['uri']
ETH_NW2 = ethernet_networks.get_by_name(MGMT_UNTAGGED)
MGMT_UNTAGGED_URI = ETH_NW2.data['uri']
FC_NW = fc_networks.get_by_name(FC_FABRIC)
FC_NETWORK_URI = FC_NW.data['uri']

# Create SCOPE
SCOPE_OPTIONS = {
    "name": SCOPE_NAME,
    "description": "Sample Scope description"
}
SCOPE = SCOPEs.get_by_name(SCOPE_OPTIONS["name"])
if SCOPE:
    print("Scope '{}' already exists".format(SCOPE_NAME))
else:
    print("Creating the SCOPE '{}'".format(SCOPE_NAME))
    SCOPE = SCOPEs.create(SCOPE_OPTIONS)

# LIG payload
OPTIONS = {
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
                "permittedInterconnectTypeUri": INTERCONNECT_TYPE1_URI,
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
                "permittedInterconnectTypeUri": INTERCONNECT_TYPE1_URI,
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
                "permittedInterconnectTypeUri": INTERCONNECT_TYPE2_URI,
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
                "permittedInterconnectTypeUri": INTERCONNECT_TYPE2_URI,
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
                "permittedInterconnectTypeUri": INTERCONNECT_TYPE2_URI,
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
                "permittedInterconnectTypeUri": INTERCONNECT_TYPE2_URI,
                "enclosureIndex": 3
            }
        ]
    },
    "uplinkSets": [
        {
            "networkType": "FibreChannel",
            "networkUris": [FC_NETWORK_URI],
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
            "networkUris": [ISCSI_NETWORK_URI],
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
                                "relativeValue": 87,
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
            "networkUris": [MGMT_UNTAGGED_URI],
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
LIG = logical_interconnect_groups.get_by_name(OPTIONS["name"])
if not LIG:
    # Create a logical interconnect group
    print("Create a logical interconnect group")
    LIG = logical_interconnect_groups.create(OPTIONS)
    print("Created logical interconnect group with name - '{}' and uri -
	 '{}'".format(LIG.data['name'], LIG.data['uri']))

# Get all, with defaults
print("Get all Logical Interconnect Groups")
LIGS = logical_interconnect_groups.get_all()
for LIG_each in LIGS:
    print(" - {}".format(LIG_each['name']))

# Get by uri
print("Get a Logical Interconnect Group by uri")
LIG_BY_URI = logical_interconnect_groups.get_by_uri(LIGS[0]["uri"])
pprint(LIG_BY_URI.data)

# Get the first 10 records, sorting by name descending, filtering by name
print("Get the first Logical Interconnect Groups, sorting by name descending, filtering by name")
LIGS = logical_interconnect_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Interconnect Group'\"")
for LIG_each in LIGS:
    print(" - {}".format(LIG_each['name']))

# Get Logical Interconnect Group by property
LIG_PROP = logical_interconnect_groups.get_by('name', 'LIG')[0]
print("Found LIG by name: '%s'.\n  uri = '%s'" % (LIG_PROP['name'], LIG_PROP['uri']))

# Get Logical Interconnect Group by SCOPE_uris
if oneview_client.api_version >= 600:
    LIG_BY_SCOPE_URIS = logical_interconnect_groups.get_all(SCOPE_uris=SCOPE.data['uri'])
    if len(LIG_BY_SCOPE_URIS) > 0:
        print("Found {} Logical Interconnect Groups".format(len(LIG_BY_SCOPE_URIS)))
        for LIG_SCOPE in LIG_BY_SCOPE_URIS:
            print("Found Logical Interconnect Group by SCOPE_uris: '{}'.\n  uri =
	 '{}'".format(LIG_SCOPE['name'], LIG_SCOPE['uri']))
    else:
        print("No Logical Interconnect Group found.")

# Update a logical interconnect group
print("Update a logical interconnect group")
LIG_TO_UPDATE = LIG.data.copy()
LIG_TO_UPDATE["name"] = "Renamed Logical Interconnect Group"
LIG.update(LIG_TO_UPDATE)
pprint(LIG.data)

# Performs a patch operation
if oneview_client.api_version <= 500:
    SCOPE = oneview_client.SCOPEs.get_by_name(SCOPE_NAME)
    if SCOPE:
        print("\nPatches the logical interconnect group adding one SCOPE to it")
        UPDATED_LIG = LIG.patch('replace',
                                '/SCOPEUris',
                                [SCOPE.data['uri']])
        pprint(UPDATED_LIG.data)

# Get default settings
print("Get the default interconnect settings for a logical interconnect group")
LIG_DEFAULT_SETTINGS = LIG.get_default_settings()
pprint(LIG_DEFAULT_SETTINGS)

# Get settings
print("Gets the interconnect settings for a logical interconnect group")
LIG_SETTINGS = LIG.get_settings()
pprint(LIG_SETTINGS)

# Delete a logical interconnect group
print("Delete the created logical interconnect group")
LIG.delete()
print("Successfully deleted logical interconnect group")

# Create a logical interconnect group for automation
print("Create a logical interconnect group as a pre-requisite for LE creation")
LIG = logical_interconnect_groups.create(OPTIONS)
print("Created logical interconnect group with name - '{}' and uri - '{}'".format(LIG.data['name'],
	 LIG.data['uri']))
