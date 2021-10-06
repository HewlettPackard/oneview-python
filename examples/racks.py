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

# NOTE: To run this sample you must define the name of an already managed ENCLOSURE
ENCLOSURE_NAME = "Encl1"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Retrieve ENCLOSURE using ENCLOSURE_NAME
ENCLOSURE = oneview_client.ENCLOSUREs.get_by('name', ENCLOSURE_NAME)[0]

# Add empty rack with default values
print("\nAdd an empty rack with default values")
EMPTY_RACK_OPTIONS = {
    "name": "OneViewSDK Test Empty Rack"
}
RACK_EMPTY = oneview_client.racks.add(EMPTY_RACK_OPTIONS)
pprint(RACK_EMPTY)

# Add a rack
print("\nAdd rack with custom size and a single mounted ENCLOSURE at slot 20")
RACK_OPTIONS = {
    "uuid": "4b4b87e2-eea8-4c90-8eca-b72eaaeecggf",
    "name": "OneViewSDK Test Rack",
    "depth": 1500,
    "height": 2500,
    "width": 1200,
    "rackMounts": [{
        "mountUri": ENCLOSURE['uri'],
        "topUSlot": 20,
        "uHeight": 10
    }]
}
RACK_CUSTOM = oneview_client.racks.add(RACK_OPTIONS)
pprint(RACK_CUSTOM)

# Get device TOPOLOGY
print("\nGet device TOPOLOGY for '{name}'".format(**RACK_CUSTOM))
TOPOLOGY = oneview_client.racks.get_device_TOPOLOGY(RACK_CUSTOM['uri'])
pprint(TOPOLOGY)

# Get all racks
print("\nGet all racks")
RACKS_ALL = oneview_client.racks.get_all()
for rack in RACKS_ALL:
    print("   '{name}' at uri: {uri}".format(**rack))

# Get five racks, SORTing by name ascending
print("\nGet five racks, SORTed by name ascending")
COUNT = 5
SORT = 'name:asc'
RACKS_SORTED = oneview_client.racks.get_all(COUNT=COUNT, SORT=SORT)
for rack in RACKS_SORTED:
    print("   '{name}' at uri: {uri}".format(**rack))

# Get rack by UUID
print("\nGet rack by 'uuid': '{uuid}'".format(**RACK_CUSTOM))
RACK_BYUUID = oneview_client.racks.get_by('uuid', RACK_CUSTOM['uuid'])
print("   Found '{name}' at uri: {uri}".format(**rack))

# Update the name of a rack
print("\nUpdate the name of '{name}' at uri: '{uri}'".format(**RACK_CUSTOM))
RACK_CUSTOM['name'] = RACK_CUSTOM['name'] + "-updated"
RACK_CUSTOM = oneview_client.racks.update(RACK_CUSTOM)
print("   Updated rack to have name: '{name}'".format(**RACK_CUSTOM))

# Remove created racks
print("\nRemove created racks by resource")
oneview_client.racks.remove(RACK_CUSTOM)
oneview_client.racks.remove(RACK_EMPTY)
print("   Done.")
