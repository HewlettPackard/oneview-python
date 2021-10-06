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
API_VARIANT = 'Synergy'
ONEVIEW_CLIENT = OneViewClient(CONFIG)
ENCLOSURE_GROUPS = ONEVIEW_CLIENT.enclosure_groups
SCOPES = ONEVIEW_CLIENT.scopes
LOGICAL_INTERCONNECT_GROUPS = ONEVIEW_CLIENT.logical_interconnect_groups

LIG_NAME = 'LIG'
LIG_URI = LOGICAL_INTERCONNECT_GROUPS.get_by_name(LIG_NAME).data['uri']

EG_OPTIONS = {
    "name": "EG",
    "interconnectBayMappings": [
        {
            "interconnectBay": 3,
            "logicalInterconnectGroupUri": LIG_URI
        },
        {
            "interconnectBay": 6,
            "logicalInterconnectGroupUri": LIG_URI
        }
    ],
    "ipAddressingMode": "External",
    "ipRangeUris": [],
    "ipv6AddressingMode": "External",
    "ipv6RangeUris": [],
    "enclosureCount": 3,
    "osDeploymentSettings": {
        "manageOSDeployment": True,
        "deploymentModeSettings": {
            "deploymentMode": "Internal",
            "deploymentNetworkUri": None
        }
    }
}

# Get the first 10 records, sorting by name descending
print("Get the ten first Enclosure Groups, sorting by name descending")
EGS = ENCLOSURE_GROUPS.get_all(0, 10, sort='name:descending')
pprint(EGS)

print("\n## Create the SCOPE")
SCOPE_OPTIONS = {
    "name": "SampleScopeForTest",
    "deSCRIPTion": "Sample Scope deSCRIPTion"
}
SCOPE = SCOPES.get_by_name(SCOPE_OPTIONS['name'])
if not SCOPE:
    SCOPE = SCOPES.create(SCOPE_OPTIONS)

# Get Enclosure Group by SCOPE_uris
if ONEVIEW_CLIENT.api_version >= 600:
    EG_BY_SCOPE_URIS = ENCLOSURE_GROUPS.get_all(SCOPE_uris=SCOPE.data['uri'])
    if len(EG_BY_SCOPE_URIS) > 0:
        print("Found Enclosure Group by SCOPE_uris: '%s'.\n  uri = '%s'" %\
	 (EG_BY_SCOPE_URIS[0]['name'], EG_BY_SCOPE_URIS[0]['uri']))
        pprint(EG_BY_SCOPE_URIS)
    else:
        print("No Enclosure Group found.")

# Get by name
ENCLOSURE_GROUP = ENCLOSURE_GROUPS.get_by_name(EG_OPTIONS["name"])
if not ENCLOSURE_GROUP:
    # Create a Enclosure Group
    print("Create a Enclosure Group")
    if ONEVIEW_CLIENT.api_version <= 500:
        OPTIONS = {"stackingMode": "Enclosure"}
        OPTIONS.update(EG_OPTIONS)
        ENCLOSURE_GROUP = ENCLOSURE_GROUPS.create(OPTIONS)
    else:
        ENCLOSURE_GROUP = ENCLOSURE_GROUPS.create(EG_OPTIONS)
print("Created enclosure group of name - '{}' with uri - '{}'".format\
        (ENCLOSURE_GROUP.data['name'], ENCLOSURE_GROUP.data['uri']))

# Get all, with default
print("Get all Enclosure Groups")
EGS = ENCLOSURE_GROUPS.get_all()
pprint(EGS)

# Get by uri
print("Get an Enclosure Group by uri")
EG_BYURI = ENCLOSURE_GROUPS.get_by_uri(EGS[0]["uri"])
pprint(EG_BYURI.data)

# Update an Enclosure Group
RESOURCE = {"name": "Renamed EG"}
print("Renaming the enclosure Group")
ENCLOSURE_GROUP.update(RESOURCE)
pprint(ENCLOSURE_GROUP.data)

# Update an Enclosure Group Script
if API_VARIANT == 'C7000':
    # update_SCRIPT is available for API version 300 in Synergy and in all versions in C7000
    print("Update an Enclosure Group Script")
    SCRIPT = "#TEST COMMAND"
    UPDATE_SCRIPT_RESULT = ENCLOSURE_GROUP.update_SCRIPT(SCRIPT)
    pprint(UPDATE_SCRIPT_RESULT)

    # Gets the CONFIGuration SCRIPT of a Enclosure Group
    # get_SCRIPT is available for API version 300 in Synergy and in all versions in C7000
    print("Gets the CONFIGuration SCRIPT of an Enclosure Group")
    SCRIPT = ENCLOSURE_GROUP.get_SCRIPT()
    print(SCRIPT)

# Delete an Enclosure Group
print("Delete the created Enclosure Group")
ENCLOSURE_GROUP.delete()
print("Successfully deleted Enclosure Group")
SCOPE.delete()

# Create EG & EG-2 for automation
ENCLOSURE_GROUP = ENCLOSURE_GROUPS.create(EG_OPTIONS)
print("Created enclosure group of name - '{}' with uri - '{}'".format(ENCLOSURE_GROUP.data['name'],\
	 ENCLOSURE_GROUP.data['uri']))

EG_OPTIONS['name'] = "EG-2"
ENCLOSURE_GROUP = ENCLOSURE_GROUPS.create(EG_OPTIONS)
print("Created enclosure group of name - '{}' with uri - '{}'".format(ENCLOSURE_GROUP.data['name'],\
	 ENCLOSURE_GROUP.data['uri']))
