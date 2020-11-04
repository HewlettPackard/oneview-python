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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
profile_templates = oneview_client.server_profile_templates

# Dependency resources
hardware_types = oneview_client.server_hardware_types
enclosure_groups = oneview_client.enclosure_groups
scopes = oneview_client.scopes
ethernet_networks = oneview_client.ethernet_networks

# These variables must be defined according with your environment
server_profile_name = "ProfileTemplate-1"
hardware_type_name = "SY 480 Gen9 1"
enclosure_group_name = "EG"
hardware_type_for_transformation = "SY 480 Gen9 2"
enclosure_group_for_transformation = "EG-2"
scope_name = "SampleScope"
mgmt_nw_name = "mgmt_nw"

hardware_type = hardware_types.get_by_name(hardware_type_name)
enclosure_group = enclosure_groups.get_by_name(enclosure_group_name)
scope_uri = scopes.get_by_name(scope_name).data['uri']
mgmt_nw_uri = ethernet_networks.get_by_name(mgmt_nw_name).data['uri']

# SPT payload
basic_template_options = {
    "name": server_profile_name,
    "serverHardwareTypeUri": hardware_type.data["uri"],
    "enclosureGroupUri": enclosure_group.data["uri"],
    "connectionSettings": {
        "connections": [
            {
                "id": 1,
                "name": "mgmt_nw",
                "functionType": "Ethernet",
                "portId": "Auto",
                "requestedMbps": "2500",
                "networkUri": mgmt_nw_uri,
            }
        ],
        "manageConnections": True,
        "complianceControl": "Checked"
    }
}

# Get all
print("\nGet list of all server profile templates")
all_templates = profile_templates.get_all()
for template in all_templates:
    print('  %s' % template['name'])

# Get Server Profile Template by scope_uris
if oneview_client.api_version >= 600:
    server_profile_templates_by_scope_uris = profile_templates.get_all(scope_uris=scope_uri)
    if len(server_profile_templates_by_scope_uris) > 0:
        print("Found %d Server profile Templates" % (len(server_profile_templates_by_scope_uris)))
        i = 0
        while i < len(server_profile_templates_by_scope_uris):
            print("Found Server Profile Template by scope_uris: '%s'.\n  uri = '%s'" % (server_profile_templates_by_scope_uris[i]['name'],
                                                                                        server_profile_templates_by_scope_uris[i]['uri']))
            i += 1
        pprint(server_profile_templates_by_scope_uris)
    else:
        print("No Server Profile Template found.")

# Get by property
print("\nGet a list of server profile templates that matches the specified macType")
if all_templates:
    template_mac_type = all_templates[0]["macType"]
    templates = profile_templates.get_by('macType', template_mac_type)
    for template in templates:
        print('  %s' % template['name'])

# Get available networks
print("\nGet available networks")
available_networks = profile_templates.get_available_networks(enclosureGroupUri=enclosure_group.data["uri"],
                                                              serverHardwareTypeUri=hardware_type.data["uri"])
print(available_networks)

# Get by name
print("\nGet a server profile templates by name")
template = oneview_client.server_profile_templates.get_by_name(server_profile_name)
if template:
    pprint(template.data)
else:
    # Create a server profile template
    print("Create a basic connection-less server profile template ")
    template = profile_templates.create(basic_template_options)
    pprint(template.data)

# Update bootMode from recently created template
print("\nUpdate bootMode from recently created template")
if template:
    template_to_update = template.data.copy()
    template_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
    template.update(template_to_update)
    pprint(template.data)

# Get new profile
print("\nGet new profile")
if template:
    profile = template.get_new_profile()
    pprint(profile)

if oneview_client.api_version >= 300 and template:
    # Get server profile template transformation
    print("\nGet a server profile template transformation")
    hardware = hardware_types.get_by_name(hardware_type_for_transformation)
    enclosure_group = enclosure_groups.get_by_name(enclosure_group_for_transformation)

    if hardware and enclosure_group:

        transformation = template.get_transformation(hardware.data["uri"],
                                                     enclosure_group.data["uri"])
        pprint(transformation)

# Delete the created template
print("\nDelete the created template")
if template:
    template.delete()
    print("The template was successfully deleted.")

# Create a server profile template for automation
print("Create a basic connection-less server profile template ")
template = profile_templates.create(basic_template_options)
pprint(template.data)
