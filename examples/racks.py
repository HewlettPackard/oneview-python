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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# NOTE: To run this sample you must define the name of an already managed enclosure
ENCLOSURE_NAME = "Encl1"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Retrieve enclosure using ENCLOSURE_NAME
enclosure = oneview_client.enclosures.get_by('name', ENCLOSURE_NAME)[0]

# Add empty rack with default values
print("\nAdd an empty rack with default values")
EMPTY_RACK_OPTIONS = {
    "name": "OneViewSDK Test Empty Rack"
}
rack_empty = oneview_client.racks.add(EMPTY_RACK_OPTIONS)
pprint(rack_empty)

# Add a rack
print("\nAdd rack with custom size and a single mounted enclosure at slot 20")
RACK_OPTIONS = {
    "uuid": "4b4b87e2-eea8-4c90-8eca-b72eaaeecggf",
    "name": "OneViewSDK Test Rack",
    "depth": 1500,
    "height": 2500,
    "width": 1200,
    "rackMounts": [{
        "mountUri": enclosure['uri'],
        "topUSlot": 20,
        "uHeight": 10
    }]
}
rack_custom = oneview_client.racks.add(RACK_OPTIONS)
pprint(rack_custom)

# Get device topology
print("\nGet device topology for '{name}'".format(**rack_custom))
topology = oneview_client.racks.get_device_topology(rack_custom['uri'])
pprint(topology)

# Get all racks
print("\nGet all racks")
racks_all = oneview_client.racks.get_all()
for rack in racks_all:
    print("   '{name}' at uri: {uri}".format(**rack))

# Get five racks, SORTing by name ascending
print("\nGet five racks, SORTed by name ascending")
COUNT = 5
SORT = 'name:asc'
racks_SORTed = oneview_client.racks.get_all(COUNT=COUNT, SORT=SORT)
for rack in racks_SORTed:
    print("   '{name}' at uri: {uri}".format(**rack))

# Get rack by UUID
print("\nGet rack by 'uuid': '{uuid}'".format(**rack_custom))
rack_byUuid = oneview_client.racks.get_by('uuid', rack_custom['uuid'])
print("   Found '{name}' at uri: {uri}".format(**rack))

# Update the name of a rack
print("\nUpdate the name of '{name}' at uri: '{uri}'".format(**rack_custom))
rack_custom['name'] = rack_custom['name'] + "-updated"
rack_custom = oneview_client.racks.update(rack_custom)
print("   Updated rack to have name: '{name}'".format(**rack_custom))

# Remove created racks
print("\nRemove created racks by resource")
oneview_client.racks.remove(rack_custom)
oneview_client.racks.remove(rack_empty)
print("   Done.")
