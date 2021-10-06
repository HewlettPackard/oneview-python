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
from CONFIG_loader import try_load_from_file

# This resource is only available on HPE Synergy

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
sas_logical_interconnect_groups = oneview_client.sas_logical_interconnect_groups
INTERCONNECT_TYPEs = oneview_client.sas_INTERCONNECT_TYPEs

INTERCONNECT_TYPE_NAME = "Synergy 12Gb SAS Connection Module"
# The Interconnect Type which is permitted to form SAS interconnect map must be defined to run this
# example
INTERCONNECT_TYPE = INTERCONNECT_TYPEs.get_by_name(INTERCONNECT_TYPE_NAME)
pprint(INTERCONNECT_TYPE)

# Create a SAS Logical Interconnect Group
DATA = {
    "name": "Test SAS Logical Interconnect Group",
    "state": "Active",
    "interconnectMapTemplate": {
        "interconnectMapEntryTemplates": [{
            "logicalLocation": {
                "locationEntries": [
                    {
                        "type": "Bay",
                        "relativeValue": 1
                    }, {
                        "type": "Enclosure",
                        "relativeValue": 1
                    }
                ]
            },
            "enclosureIndex": 1,
            "permittedInterconnectTypeUri": INTERCONNECT_TYPE.DATA["uri"]
        }, {
            "logicalLocation": {
                "locationEntries": [
                    {
                        "type": "Bay",
                        "relativeValue": 4
                    }, {
                        "type": "Enclosure",
                        "relativeValue": 1
                    }
                ]
            },
            "enclosureIndex": 1,
            "permittedInterconnectTypeUri": INTERCONNECT_TYPE.DATA["uri"]
        }]
    },
    "enclosureType": "SY12000",
    "enclosureIndexes": [1],
    "interconnectBaySet": 1
}

# Get all SAS Logical Interconnect Groups
print("\nGet all SAS Logical Interconnect Groups")
SAS_LIGS = sas_logical_interconnect_groups.get_all()
for SAS_LIG in SAS_LIGS:
    print("\n   '{name}' at uri: {uri}".format(**SAS_LIG))

# Get SAS Interconnect Group by scope_uris
if oneview_client.api_version >= 600:
    SAS_LIG_BY_SCOPE_URIS = sas_logical_interconnect_groups.get_all(
        scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
    if len(SAS_LIG_BY_SCOPE_URIS) > 0:
        print("found %d SAS Interconnect Groups" % (len(SAS_LIG_BY_SCOPE_URIS)))
        i = 0
        while i < len(SAS_LIG_BY_SCOPE_URIS):
            print("Found SAS Interconnect Group by scope_uris: '%s'.\n  uri = '%s'" %
	 (SAS_LIG_BY_SCOPE_URIS[i]['name'], SAS_LIG_BY_SCOPE_URIS[i]['uri']))
            i += 1
        pprint(SAS_LIG_BY_SCOPE_URIS)
    else:
        print("No SAS Interconnect Group found.")

SAS_LIG = sas_logical_interconnect_groups.get_by_name(DATA["name"])
if not SAS_LIG:
    SAS_LIG = sas_logical_interconnect_groups.create(DATA)
    print("\nSAS Logical Interconnect Group '{name}' created successfully.\n  uri =
	 '{uri}'".format(**SAS_LIG.DATA))

# Update the SAS Logical Interconnect Group
print("\nUpdate the SAS Logical Interconnect Group")
RESOURCE_TO_UPDATE = SAS_LIG.DATA.copy()
RESOURCE_TO_UPDATE['name'] = 'Test SAS Logical Interconnect Group - Renamed1'

SAS_LIG.update(RESOURCE_TO_UPDATE)
pprint(SAS_LIG.DATA)

# Delete the SAS Logical Interconnect Group
SAS_LIG.delete()
print("\nSAS Logical Interconnect Group deleted successfully")
