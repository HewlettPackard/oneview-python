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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": "<api_version>"
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
server_PROFILES = oneview_client.server_PROFILES

# Dependency resources
PROFILE_templates = oneview_client.server_PROFILE_templates
ENCLOSURE_GROUPs = oneview_client.ENCLOSURE_GROUPs
server_HARDWARE_TYPEs = oneview_client.server_HARDWARE_TYPEs
SERVER_HARDWAREs = oneview_client.SERVER_HARDWARE
SCOPEs = oneview_client.SCOPEs

# To run this sample you must define a server hardware type uri and an enclosure group uri
PROFILE_TEMPLATE_NAME = "ProfileTemplate-1"
PROFILE_NAME = "TestProfile"
ENCLOSURE_GROUP_NAME = "EG"
SERVER_HARDWARE_TYPE_NAME = "SY 480 Gen9 1"
SERVER_HARDWARE_NAME = "0000A66102, bay 5"
# To run the example 'get a specific storage system' you must define a storage system ID
STORAGE_SYSTEM_ID = None

HARDWARE_TYPE = server_HARDWARE_TYPEs.get_by_name(SERVER_HARDWARE_TYPE_NAME)
ENCLOSURE_GROUP = ENCLOSURE_GROUPs.get_by_name(ENCLOSURE_GROUP_NAME)
SERVER_HARDWARE = SERVER_HARDWAREs.get_by_name(SERVER_HARDWARE_NAME)

# Get all
print("\nGet list of all server PROFILES")
ALL_PROFILES = server_PROFILES.get_all()
for PROFILE in ALL_PROFILES:
    print('  %s' % PROFILE['name'])

# Get by property
print("\nGet a list of server PROFILES that matches the specified macType")
if ALL_PROFILES:
    PROFILE_MAC_TYPE = ALL_PROFILES[0]["macType"]
    PROFILES = server_PROFILES.get_by('macType', PROFILE_MAC_TYPE)
    for PROFILE in PROFILES:
        print('  %s' % PROFILE['name'])

# Get by name
print("\nGet a server PROFILE by name")
PROFILE = server_PROFILES.get_by_name(PROFILE_NAME)

if PROFILE:
    print("Found PROFILE with name '{}' and uri '{}'".format(PROFILE.data['name'], PROFILE.data['uri']))
else:
    SERVER_TEMPLATE = PROFILE_templates.get_by_name(PROFILE_TEMPLATE_NAME)
    if not SERVER_TEMPLATE:
        # Create a server PROFILE template to associate with the server PROFILE
        SERVER_TEMPLATE = PROFILE_templates.create(dict(
            name=PROFILE_TEMPLATE_NAME,
            serverHardwareTypeUri=HARDWARE_TYPE.data["uri"],
            enclosureGroupUri=ENCLOSURE_GROUP.data["uri"]))

    basic_PROFILE_options = dict(
        name=PROFILE_NAME,
        serverProfileTemplateUri=SERVER_TEMPLATE.data["uri"],
        serverHardwareTypeUri=HARDWARE_TYPE.data["uri"],
        enclosureGroupUri=ENCLOSURE_GROUP.data["uri"]
    )

    # Create a server PROFILE
    print("\nCreate a basic connection-less assigned server PROFILE")
    PROFILE = server_PROFILES.create(basic_PROFILE_options)
    print("Created PROFILE with name '{}' and uri '{}'".format(PROFILE.data['name'], PROFILE.data['uri']))

# Get by uri
print("\nGet a server PROFILE by uri")
PROFILE = server_PROFILES.get_by_uri(PROFILE.data['uri'])
pprint(PROFILE.data)

# Update bootMode from recently created PROFILE
print("\nUpdate bootMode from recently created PROFILE")
if PROFILE:
    PROFILE_to_update = PROFILE.data.copy()
    PROFILE_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
    PROFILE.update(PROFILE_to_update)
    pprint(PROFILE.data)

# Server PROFILE compliance preview
print("\nGets the preview of manual and automatic updates required to make the server PROFILE consistent "
      "with its template.")
if PROFILE:
    SCHEMA = PROFILE.get_compliance_preview()
    pprint(SCHEMA)

# Patch
print("\nUpdate the PROFILE CONFIGuration from server PROFILE template")
if PROFILE:
    PROFILE.patch(operation="replace",
                  path="/templateCompliance", value="Compliant")
    pprint(PROFILE.data)

if oneview_client.api_version <= 500 and PROFILE:
    # Retrieve the error or status MESSAGES associated with the specified PROFILE
    print("\nList PROFILE status MESSAGES associated with a PROFILE")
    MESSAGES = PROFILE.get_MESSAGES()
    pprint(MESSAGES)

# Transform an server PROFILE
print("\nTransform an existing PROFILE by supplying a new server hardware type and/or enclosure group.")
if PROFILE:
    SERVER_TRANSFORMED = PROFILE.get_transformation(
        enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
        serverHardwareTypeUri=HARDWARE_TYPE.data['uri'])
    pprint(SERVER_TRANSFORMED)

print("Transformation complete. Updating server PROFILE with the new CONFIGuration.")
if PROFILE and SERVER_TRANSFORMED:
    PROFILE_updated = PROFILE.update(SERVER_TRANSFORMED['serverProfile'])
    pprint(PROFILE_updated.data)

# Create a new Server Profile Template based on an existing Server Profile
# This method i.e., get_new_PROFILE_template works with all the API versions till 1200
if oneview_client.api_version <= 1200 and PROFILE:
    NEW_SPT = PROFILE.get_new_PROFILE_template()
    print('\nNew SPT generated:')
    pprint(NEW_SPT)

    NEW_SPT['name'] = 'spt_generated_from_sp'
    NEW_SPT = PROFILE_templates.create(NEW_SPT)
    print('\nNew SPT created successfully.')

    NEW_SPT.delete()
    print('\nDropped recently created SPT.')

# Delete the created server PROFILE
print("\nDelete the created server PROFILE")
if PROFILE:
    PROFILE.delete()
    print("The server PROFILE was successfully deleted.")

# Get PROFILE ports
print("\nRetrieve the port model associated with a server hardware type and enclosure group")
PROFILE_ports = server_PROFILES.get_PROFILE_ports(enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
                                                  serverHardwareTypeUri=HARDWARE_TYPE.data["uri"])
pprint(PROFILE_ports)

# Get PROFILE ports
print("\nRetrieve the port model associated with a server hardware")
PROFILE_ports = oneview_client.server_PROFILES.get_PROFILE_ports(
    serverHardwareUri=SERVER_HARDWARE.data["uri"])
pprint(PROFILE_ports)

# Get the list of networks and network sets that are available to a server PROFILE along with their respective ports
print("\nList all Ethernet networks associated with a server hardware type and enclosure group")
AVAILABLE_NETWORKS = server_PROFILES.get_AVAILABLE_NETWORKS(
    enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
    serverHardwareTypeUri=HARDWARE_TYPE.data["uri"], view='Ethernet')
pprint(AVAILABLE_NETWORKS)

print("\n## Create the SCOPE")
SCOPE_OPTIONS = {
    "name": "SampleScopeForTest",
    "description": "Sample Scope description"
}
SCOPE = SCOPEs.get_by_name(SCOPE_OPTIONS['name'])
if not SCOPE:
    SCOPE = SCOPEs.create(SCOPE_OPTIONS)

# Get the all Ethernet networks associated with a server hardware type, enclosure group and SCOPEuris
# This method ie., get_AVAILABLE_NETWORKS works with all the API versions but the SCOPE_uris param is available
# with API version 600 and above
if oneview_client.api_version >= 600:
    AVAILABLE_NETWORKS = server_PROFILES.get_AVAILABLE_NETWORKS(
        enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
        serverHardwareTypeUri=HARDWARE_TYPE.data["uri"],
        view='Ethernet',
        SCOPE_uris=SCOPE.data['uri'])
    if len(AVAILABLE_NETWORKS) > 0:
        pprint(AVAILABLE_NETWORKS)
    else:
        print("No Server Profiles Group found.")

# Get the list of available servers
# This method i.e.,get_AVAILABLE_SERVERS works with all the API versions till 1200
# as it got deprecated from apiVersion 1200
if oneview_client.api_version <= 1200:
    print("\nList all available servers associated with a server hardware type and enclosure group")
    AVAILABLE_SERVERS = server_PROFILES.get_AVAILABLE_SERVERS(
        enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
        serverHardwareTypeUri=HARDWARE_TYPE.data["uri"])
    pprint(AVAILABLE_SERVERS)

# List available storage systems
# This method i.e., get_AVAILABLE_STORAGE_SYSTEMS works with all the API versions till 500
if oneview_client.api_version <= 500:
    print("\nList available storage systems associated with the given enclosure group URI and server
	 hardware type URI")
    AVAILABLE_STORAGE_SYSTEMS = server_PROFILES.get_AVAILABLE_STORAGE_SYSTEMS(
        count=25, start=0, enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
        serverHardwareTypeUri=HARDWARE_TYPE.data["uri"])
    pprint(AVAILABLE_STORAGE_SYSTEMS)

# Get a specific storage system
# This method ie.,get_AVAILABLE_STORAGE_SYSTEM works with all the API versions till 500
if STORAGE_SYSTEM_ID and oneview_client.api_version <= 500:
    print("\nRetrieve a specific storage system associated with the given enclosure group URI, a
	 server hardware"
          " type URI and a storage system ID")
    AVAILABLE_STORAGE_SYSTEM = server_PROFILES.get_AVAILABLE_STORAGE_SYSTEM(
        storageSystemId=STORAGE_SYSTEM_ID,
        enclosureGroupUri=ENCLOSURE_GROUP.data["uri"],
        serverHardwareTypeUri=HARDWARE_TYPE.data["uri"])
    pprint(AVAILABLE_STORAGE_SYSTEM)

# List available targets
print("\nList all available servers and bays for a given enclosure group.")
AVAILABLE_TARGETS = server_PROFILES.get_AVAILABLE_TARGETS(
    enclosureGroupUri=ENCLOSURE_GROUP.data["uri"])
pprint(AVAILABLE_TARGETS)

# Delete all server PROFILE (filtering)
print("\nRemove all PROFILES that match the name 'Profile fake'")
# Create a new PROFILE to delete
server_PROFILES.create(dict(
    name="Profile fake",
    serverHardwareTypeUri=HARDWARE_TYPE.data["uri"],
    enclosureGroupUri=ENCLOSURE_GROUP.data["uri"]
))
server_PROFILES.delete_all(filter="name='Profile fake'")
print("The server PROFILES were successfully deleted.")

# Create a server PROFILE for automation
print("\nCreate a basic connection-less assigned server PROFILE")
PROFILE = server_PROFILES.create(basic_PROFILE_options)
print("Created PROFILE with name '{}' and uri '{}'".format(PROFILE.data['name'], PROFILE.data['uri']))

# Make SP compliant with SPT
print("\nUpdate the PROFILE CONFIGuration from server PROFILE template")
if PROFILE:
    PROFILE.patch(operation="replace",
                  path="/templateCompliance", value="Compliant")
    pprint(PROFILE.data)
