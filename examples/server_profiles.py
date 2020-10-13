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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
server_profiles = oneview_client.server_profiles

# Dependency resources
profile_templates = oneview_client.server_profile_templates
enclosure_groups = oneview_client.enclosure_groups
server_hardware_types = oneview_client.server_hardware_types
server_hardwares = oneview_client.server_hardware
scopes = oneview_client.scopes

# To run this sample you must define a server hardware type uri and an enclosure group uri
profile_template_name = "OneView Test Profile Template"
profile_name = "OneView Test Profile"
enclosure_group_name = "EG"
server_hardware_type_name = "SY 480 Gen9 2"
server_hardware_name = "0000A66102, bay 3"
# To run the example 'get a specific storage system' you must define a storage system ID
storage_system_id = None

hardware_type = server_hardware_types.get_by_name(server_hardware_type_name)
enclosure_group = enclosure_groups.get_by_name(enclosure_group_name)
server_hardware = server_hardwares.get_by_name(server_hardware_name)

# Get all
print("\nGet list of all server profiles")
all_profiles = server_profiles.get_all()
for profile in all_profiles:
    print('  %s' % profile['name'])

# Get by property
print("\nGet a list of server profiles that matches the specified macType")
if all_profiles[1]:
    profile_mac_type = all_profiles[1]["macType"]
    profiles = server_profiles.get_by('macType', profile_mac_type)
    for profile in profiles:
        print('  %s' % profile['name'])

# Get by uri
print("\nGet a server profile by uri")
profile = server_profiles.get_by_uri(all_profiles[0]['uri'])
pprint(profile.data)

# Get by name
print("\nGet a server profile by name")
profile = server_profiles.get_by_name(profile_name)

if profile:
    pprint(profile)
else:
    server_template = profile_templates.get_by_name(profile_template_name)
    if not server_template:
        # Create a server profile template to associate with the server profile
        server_template = profile_templates.create(dict(
            name=profile_template_name,
            serverHardwareTypeUri=hardware_type.data["uri"],
            enclosureGroupUri=enclosure_group.data["uri"]))

    # Create a server profile
    print("\nCreate a basic connection-less assigned server profile")
    basic_profile_options = dict(
        name=profile_name,
        serverProfileTemplateUri=server_template.data["uri"],
        serverHardwareTypeUri=hardware_type.data["uri"],
        enclosureGroupUri=enclosure_group.data["uri"]
    )
    profile = server_profiles.create(basic_profile_options)
    pprint(profile.data)

# Update bootMode from recently created profile
print("\nUpdate bootMode from recently created profile")
if profile:
    profile_to_update = profile.data.copy()
    profile_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
    profile.update(profile_to_update)
    pprint(profile.data)

# Patch
print("\nUpdate the profile configuration from server profile template")
if profile:
    profile.patch(operation="replace",
                  path="/templateCompliance", value="Compliant")
    pprint(profile.data)

# Server profile compliance preview
print("\nGets the preview of manual and automatic updates required to make the server profile consistent "
      "with its template.")
if profile:
    schema = profile.get_compliance_preview()
    pprint(schema)

if oneview_client.api_version <= 500 and profile:
    # Retrieve the error or status messages associated with the specified profile
    print("\nList profile status messages associated with a profile")
    messages = profile.get_messages()
    pprint(messages)

# Transform an server profile
print("\nTransform an existing profile by supplying a new server hardware type and/or enclosure group.")
if profile:
    server_transformed = profile.get_transformation(
        enclosureGroupUri=enclosure_group.data["uri"],
        serverHardwareTypeUri=hardware_type.data['uri'])
    pprint(server_transformed)

print("Transformation complete. Updating server profile with the new configuration.")
if profile and server_transformed:
    profile_updated = profile.update(server_transformed['serverProfile'])
    pprint(profile_updated.data)

# Create a new Server Profile Template based on an existing Server Profile
# This method i.e., get_new_profile_template works with all the API versions till 1200
if oneview_client.api_version <= 1200 and profile:
    new_spt = profile.get_new_profile_template()
    print('\nNew SPT generated:')
    pprint(new_spt)

    new_spt['name'] = 'spt_generated_from_sp'
    new_spt = profile_templates.create(new_spt)
    print('\nNew SPT created successfully.')

    new_spt.delete()
    print('\nDropped recently created SPT.')

# Delete the created server profile
print("\nDelete the created server profile")
if profile:
    profile.delete()
    print("The server profile was successfully deleted.")

# Delete the created server profile template
if server_template:
    server_template.delete()
    print("The server profile template was successfully deleted")

# Get profile ports
print("\nRetrieve the port model associated with a server hardware type and enclosure group")
profile_ports = server_profiles.get_profile_ports(enclosureGroupUri=enclosure_group.data["uri"],
                                                  serverHardwareTypeUri=hardware_type.data["uri"])
pprint(profile_ports)

# Get profile ports
print("\nRetrieve the port model associated with a server hardware")
profile_ports = oneview_client.server_profiles.get_profile_ports(
    serverHardwareUri=server_hardware.data["uri"])
pprint(profile_ports)

# Get the list of networks and network sets that are available to a server profile along with their respective ports
print("\nList all Ethernet networks associated with a server hardware type and enclosure group")
available_networks = server_profiles.get_available_networks(
    enclosureGroupUri=enclosure_group.data["uri"],
    serverHardwareTypeUri=hardware_type.data["uri"], view='Ethernet')
pprint(available_networks)

print("\n## Create the scope")
options = {
    "name": "SampleScopeForTest",
    "description": "Sample Scope description"
}
scope = scopes.create(options)

# Get the all Ethernet networks associated with a server hardware type, enclosure group and scopeuris
# This method ie., get_available_networks works with all the API versions but the scope_uris param is available
# with API version 600 and above
if oneview_client.api_version >= 600:
    available_networks = server_profiles.get_available_networks(
        enclosureGroupUri=enclosure_group.data["uri"],
        serverHardwareTypeUri=hardware_type.data["uri"],
        view='Ethernet',
        scope_uris=scope.data['uri'])
    if len(available_networks) > 0:
        pprint(available_networks)
    else:
        print("No Server Profiles Group found.")

# Get the list of available servers
# This method i.e.,get_available_servers works with all the API versions till 1200
# as it got deprecated from apiVersion 1200
if oneview_client.api_version <= 1200:
    print("\nList all available servers associated with a server hardware type and enclosure group")
    available_servers = server_profiles.get_available_servers(
        enclosureGroupUri=enclosure_group.data["uri"],
        serverHardwareTypeUri=hardware_type.data["uri"])
    pprint(available_servers)

# List available storage systems
# This method i.e., get_available_storage_systems works with all the API versions till 500
if oneview_client.api_version <= 500:
    print("\nList available storage systems associated with the given enclosure group URI and server hardware type URI")
    available_storage_systems = server_profiles.get_available_storage_systems(
        count=25, start=0, enclosureGroupUri=enclosure_group.data["uri"],
        serverHardwareTypeUri=hardware_type.data["uri"])
    pprint(available_storage_systems)

# Get a specific storage system
# This method ie.,get_available_storage_system works with all the API versions till 500
if storage_system_id and oneview_client.api_version <= 500:
    print("\nRetrieve a specific storage system associated with the given enclosure group URI, a server hardware"
          " type URI and a storage system ID")
    available_storage_system = server_profiles.get_available_storage_system(
        storageSystemId=storage_system_id,
        enclosureGroupUri=enclosure_group.data["uri"],
        serverHardwareTypeUri=hardware_type.data["uri"])
    pprint(available_storage_system)

# List available targets
print("\nList all available servers and bays for a given enclosure group.")
available_targets = server_profiles.get_available_targets(
    enclosureGroupUri=enclosure_group.data["uri"])
pprint(available_targets)

# Delete all server profile (filtering)
print("\nRemove all profiles that match the name 'Profile fake'")
# Create a new profile to delete
server_profiles.create(dict(
    name="Profile fake",
    serverHardwareTypeUri=hardware_type.data["uri"],
    enclosureGroupUri=enclosure_group.data["uri"]
))
server_profiles.delete_all(filter="name='Profile fake'")
print("The server profiles were successfully deleted.")
