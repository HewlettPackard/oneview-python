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
from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
PROFILE_TEMPLATES = oneview_client.server_profile_templates

# Dependency resources
HARDWARE_TYPES = oneview_client.server_hardware_types
ENCLOSURE_GROUPS = oneview_client.enclosure_groups
SCOPES = oneview_client.scopes
ETHERNET_NETWORKS = oneview_client.ethernet_networks

# These variables must be defined according with your environment
SERVER_PROFILE_NAME = "ProfileTemplate-1"
HARDWARE_TYPE_NAME = "SY 480 Gen9 1"
ENCLOSURE_GROUP_NAME = "EG"
HARDWARE_TYPE_FOR_TRANSFORMATION = "SY 480 Gen9 2"
ENCLOSURE_GROUP_FOR_TRANSFORMATION = "EG-2"
SCOPE_NAME = "SampleScope"
MGMT_NW_NAME = "mgmt"

HARDWARE_TYPE = HARDWARE_TYPES.get_by_name(HARDWARE_TYPE_NAME)
ENCLOSURE_GROUP = ENCLOSURE_GROUPS.get_by_name(ENCLOSURE_GROUP_NAME)
SCOPE_URI = SCOPES.get_by_name(SCOPE_NAME).data['uri']
MGMT_NW_URI = ETHERNET_NETWORKS.get_by_name(MGMT_NW_NAME).data['uri']

# SPT payload
BASIC_TEMPLATE_OPTIONS = {
    "name": SERVER_PROFILE_NAME,
    "serverHardwareTypeUri": HARDWARE_TYPE.data["uri"],
    "enclosureGroupUri": ENCLOSURE_GROUP.data["uri"],
    "connectionSettings": {
        "connections": [
            {
                "id": 1,
                "name": "mgmt_nw",
                "functionType": "Ethernet",
                "portId": "Auto",
                "requestedMbps": "2500",
                "networkUri": MGMT_NW_URI,
            }
        ],
        "manageConnections": True,
        "complianceControl": "Checked"
    }
}

# Get all
print("\nGet list of all server PROFILE TEMPLATES")
ALL_TEMPLATES = PROFILE_TEMPLATES.get_all()
for TEMPLATE in ALL_TEMPLATES:
    print('  %s' % TEMPLATE['name'])

# Get Server Profile Template by SCOPE_URIs
if oneview_client.api_version >= 600:
    SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS = PROFILE_TEMPLATES.get_all(SCOPE_URIs=SCOPE_URI)
    if len(SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS) > 0:
        print("Found %d Server PROFILE Templates" % (len(SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS)))
        i = 0
        while i < len(SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS):
            print("Found Server Profile Template by SCOPE_URIs: '%s'.\n  uri = '%s'" % \
                    (SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS[i]['name'],\
                    SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS[i]['uri']))
            i += 1
        pprint(SERVER_PROFILE_TEMPLATES_BY_SCOPE_URIS)
    else:
        print("No Server Profile Template found.")

# Get by property
print("\nGet a list of server PROFILE TEMPLATES that matches the specified macType")
if ALL_TEMPLATES:
    TEMPLATE_MAC_TYPE = ALL_TEMPLATES[0]["macType"]
    TEMPLATES = PROFILE_TEMPLATES.get_by('macType', TEMPLATE_MAC_TYPE)
    for TEMPLATE in TEMPLATES:
        print('  %s' % TEMPLATE['name'])

# Get available networks
print("\nGet available networks")
AVAILABLE_NETWORKS = PROFILE_TEMPLATES.get_available_networks(enclosureGroupUri=\
        ENCLOSURE_GROUP.data["uri"], serverHardwareTypeUri=HARDWARE_TYPE.data["uri"])
print(AVAILABLE_NETWORKS)

# Get by name
print("\nGet a server PROFILE TEMPLATES by name")
TEMPLATE = oneview_client.server_profile_templates.get_by_name(SERVER_PROFILE_NAME)
if TEMPLATE:
    pprint(TEMPLATE.data)
else:
    # Create a server PROFILE TEMPLATE
    print("Create a basic connection-less server PROFILE TEMPLATE ")
    TEMPLATE = PROFILE_TEMPLATES.create(BASIC_TEMPLATE_OPTIONS)
    pprint(TEMPLATE.data)

# Update bootMode from recently created TEMPLATE
print("\nUpdate bootMode from recently created TEMPLATE")
if TEMPLATE:
    TEMPLATE_TO_UPDATE = TEMPLATE.data.copy()
    TEMPLATE_TO_UPDATE["bootMode"] = dict(manageMode=True, mode="BIOS")
    TEMPLATE.update(TEMPLATE_TO_UPDATE)
    pprint(TEMPLATE.data)

# Patch operation to refresh the TEMPLATE
print("\nUpdate the TEMPLATE CONFIGuration with RefreshPending")
if oneview_client.api_version >= 1800 and TEMPLATE:
    TEMPLATE.patch(operation="replace", path="/refreshState", value="RefreshPending")
    pprint(TEMPLATE.data)

# Get new PROFILE
print("\nGet new PROFILE")
if TEMPLATE:
    PROFILE = TEMPLATE.get_new_PROFILE()
    pprint(PROFILE)

if oneview_client.api_version >= 300 and TEMPLATE:
    # Get server PROFILE TEMPLATE TRANSFORMATION
    print("\nGet a server PROFILE TEMPLATE TRANSFORMATION")
    HARDWARE = HARDWARE_TYPES.get_by_name(HARDWARE_TYPE_FOR_TRANSFORMATION)
    ENCLOSURE_GROUP = ENCLOSURE_GROUPS.get_by_name(ENCLOSURE_GROUP_FOR_TRANSFORMATION)

    if HARDWARE and ENCLOSURE_GROUP:

        TRANSFORMATION = TEMPLATE.get_TRANSFORMATION(HARDWARE.data["uri"],
                                                     ENCLOSURE_GROUP.data["uri"])
        pprint(TRANSFORMATION)

# Delete the created TEMPLATE
print("\nDelete the created TEMPLATE")
if TEMPLATE:
    TEMPLATE.delete()
    print("The TEMPLATE was successfully deleted.")

# Create a server PROFILE TEMPLATE for automation
print("Create a basic connection-less server PROFILE TEMPLATE ")
TEMPLATE = PROFILE_TEMPLATES.create(BASIC_TEMPLATE_OPTIONS)
pprint(TEMPLATE.data)
