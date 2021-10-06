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
from hpeOneView.exceptions import HPEOneViewException
from CONFIG_loader import try_load_from_file

# This resource is only available on C7000 enclosures

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# provide info about your switch here
SWITCH_ID = "7a2704e2-564d-4163-8745-2a0b807a5e03"
SWITCH_URI = "/rest/switches/" + SWITCH_ID

PORT_NAME = "1.1"
PORT_ID = "{SWITCH_ID}:{PORT_NAME}".format(**locals())

# To run the SCOPE patch operations in this example, a SCOPE name is required.
SCOPE_NAME = "SCOPE1"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

print("\nGet a switch statistics:\n")
try:
    SWITCH_STATISTICS = oneview_client.switches.get_statistics(SWITCH_URI)
    pprint(SWITCH_STATISTICS)
except HPEOneViewException as e:
    print(e.msg)

print("\nGet a switch statistics with portName\n")
try:
    SWITCH_STATISTICS = oneview_client.switches.get_statistics(SWITCH_URI, "1.2")
    pprint(SWITCH_STATISTICS)
except HPEOneViewException as e:
    print(e.msg)

print("\nGet all switches in domain\n")
SWITCHES_ALL = oneview_client.switches.get_all()
pprint(SWITCHES_ALL)

try:
    print("\nGet switch by id\n")
    SWITCH_BY_ID = oneview_client.switches.get(SWITCH_ID)
    pprint(SWITCH_BY_ID)
except HPEOneViewException as e:
    print(e.msg)

try:
    print("\nGet switch by uri\n")
    SWITCH_BY_URI = oneview_client.switches.get(SWITCH_URI)
    pprint(SWITCH_BY_URI)
except HPEOneViewException as e:
    print(e.msg)

try:
    print("\nGet environmental CONFIGuration of switch by id\n")
    SWITCH_BY_ID = oneview_client.switches.get_environmental_CONFIGuration(SWITCH_ID)
    pprint(SWITCH_BY_ID)
except HPEOneViewException as e:
    print(e.msg)

try:
    print("\nGet environmental CONFIGuration of switch by uri\n")
    SWITCH_ENV_CONF = oneview_client.switches.get_environmental_CONFIGuration(SWITCH_URI)
    pprint(SWITCH_ENV_CONF)
except HPEOneViewException as e:
    print(e.msg)

try:
    print("\nGet switch by rack name\n")
    SWITCH_BY_RACK_NAME = oneview_client.switches.get_by("rackName", "Test Name")
    pprint(SWITCH_BY_RACK_NAME)
except HPEOneViewException as e:
    print(e.msg)

# Get SCOPE to be added
print("\nTrying to retrieve SCOPE named '%s'." % SCOPE_NAME)
SCOPE = oneview_client.SCOPEs.get_by_name(SCOPE_NAME)

# Performs a patch operation on the Logical Switch
if SCOPE and oneview_client.api_version == 500:
    print("\nPatches the switch assigning the '%s' SCOPE to it." % SCOPE_NAME)
    SWITCH_BY_URI = oneview_client.switches.patch(SWITCH_BY_URI['uri'],
                                                  'replace',
                                                  '/SCOPEUris',
                                                  [SCOPE['uri']])
    pprint(SWITCH_BY_URI)

if oneview_client.api_version >= 300:
    try:
        print("\nUpdate the switch PORTS\n")

        PORTS_TO_UPDATE = [{
            "enabled": True,
            "portId": PORT_ID,
            "portName": PORT_NAME
        }]

        PORTS = oneview_client.switches.update_PORTS(id_or_uri=SWITCH_ID, PORTS=PORTS_TO_UPDATE)
        print("  Done.")
    except HPEOneViewException as e:
        print(e.msg)

# Delete the migrated switch
print("\nDelete a switch:\n")
try:
    oneview_client.switches.delete(SWITCH_BY_ID)
    print("Successfully deleted the switch")
except HPEOneViewException as e:
    print(e.msg)
