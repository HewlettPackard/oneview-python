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
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# This resource is only available on HPE Synergy

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
sas_logical_interconnect_groups = oneview_client.sas_logical_interconnect_groups
interconnect_types = oneview_client.sas_interconnect_types

interconnect_type_name = "Synergy 12Gb SAS Connection Module"
# The Interconnect Type which is permitted to form SAS interconnect map must be defined to run this example
interconnect_type = interconnect_types.get_by_name(interconnect_type_name)
pprint(interconnect_type)

# Create a SAS Logical Interconnect Group
data = {
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
            "permittedInterconnectTypeUri": interconnect_type.data["uri"]
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
            "permittedInterconnectTypeUri": interconnect_type.data["uri"]
        }]
    },
    "enclosureType": "SY12000",
    "enclosureIndexes": [1],
    "interconnectBaySet": 1
}

# Get all SAS Logical Interconnect Groups
print("\nGet all SAS Logical Interconnect Groups")
sas_ligs = sas_logical_interconnect_groups.get_all()
for sas_lig in sas_ligs:
    print("\n   '{name}' at uri: {uri}".format(**sas_lig))

# Get SAS Interconnect Group by scope_uris
if oneview_client.api_version >= 600:
    sas_lig_by_scope_uris = sas_logical_interconnect_groups.get_all(
        scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
    if len(sas_lig_by_scope_uris) > 0:
        print("found %d SAS Interconnect Groups" % (len(sas_lig_by_scope_uris)))
        i = 0
        while i < len(sas_lig_by_scope_uris):
            print("Found SAS Interconnect Group by scope_uris: '%s'.\n  uri = '%s'" % (sas_lig_by_scope_uris[i]['name'], sas_lig_by_scope_uris[i]['uri']))
            i += 1
        pprint(sas_lig_by_scope_uris)
    else:
        print("No SAS Interconnect Group found.")

sas_lig = sas_logical_interconnect_groups.get_by_name(data["name"])
if not sas_lig:
    sas_lig = sas_logical_interconnect_groups.create(data)
    print("\nSAS Logical Interconnect Group '{name}' created successfully.\n  uri = '{uri}'".format(**sas_lig.data))

# Update the SAS Logical Interconnect Group
print("\nUpdate the SAS Logical Interconnect Group")
resource_to_update = sas_lig.data.copy()
resource_to_update['name'] = 'Test SAS Logical Interconnect Group - Renamed1'

sas_lig.update(resource_to_update)
pprint(sas_lig.data)

# Delete the SAS Logical Interconnect Group
sas_lig.delete()
print("\nSAS Logical Interconnect Group deleted successfully")
