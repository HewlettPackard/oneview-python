# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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

CONFIG = {
    "ip": "<ov_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
INTERCONNECTS = oneview_client.INTERCONNECTS

# To run this example you must define an INTERCONNECT, otherwise, it will get the first one
# automatically
INTERCONNECT_URI = INTERCONNECTS.get_all(0, 1)[0]['uri']
INTERCONNECT_ID = INTERCONNECT_URI.replace('/rest/INTERCONNECTS/', '')
INTERCONNECT = INTERCONNECTS.get_by_uri(INTERCONNECT_URI)

PORT_D1 = {
    "type": "port",
    "portName": "d1",
    "bayNumber": 1,
    "enabled": False,
    "portId": "{0}:d1".format(INTERCONNECT_ID)
}

PORT_D2 = {
    "portName": "d2",
    "enabled": False,
    "portId": "{0}:d2".format(INTERCONNECT_ID)
}

PORTS_FOR_UPDATE = [PORT_D1, PORT_D2]

# Get the first two Interconnects
print("\nGet the first two INTERCONNECTS")
INTERCONNECTS_ALL = INTERCONNECTS.get_all(0, 2)
pprint(INTERCONNECTS_ALL)

# Get Interconnects Statistics
print("\nGet the INTERCONNECT STATISTICS")
INTERCONNECT_STATISTICS = INTERCONNECT.get_STATISTICS()
if INTERCONNECT_STATISTICS:
    pprint(INTERCONNECT_STATISTICS['moduleStatistics'])
else:
    pprint("\nThere are no STATISTICS for the INTERCONNECT {0}".format(INTERCONNECT.data["name"]))

# Get the Statistics from a port of an Interconnects
print("\nGet the port STATISTICS for downlink port 1 on the INTERCONNECT "
      "that matches the specified ID")
try:
    STATISTICS = INTERCONNECT.get_STATISTICS(PORT_D1["portName"])
    pprint(STATISTICS)
except HPEOneViewException as e:
    print(e.msg)

# Get the subport Statistics from a port of an Interconnects
print("\nGet the subport STATISTICS for subport 1 on downlink port 2 on the INTERCONNECT "
      "that matches the specified ID")
try:
    STATISTICS = INTERCONNECT.get_subport_STATISTICS(PORT_D1["portName"],
                                                     PORT_D1["bayNumber"])
    pprint(STATISTICS)
except HPEOneViewException as e:
    print(e.msg)

# Get by hostName
print("\nGet an INTERCONNECT by hostName")
try:
    INTERCONNECT_BY_HOST = INTERCONNECTS.get_by('hostName', INTERCONNECT.data["hostName"])[0]
    pprint(INTERCONNECT_BY_HOST)
except HPEOneViewException as e:
    print(e.msg)

# Get by name
print("\nGet an INTERCONNECT by name")
try:
    INTERCONNECT_BY_NAME = INTERCONNECTS.get_by_name(INTERCONNECT.data["name"])
    pprint(INTERCONNECT_BY_NAME.data)
except HPEOneViewException as e:
    print(e.msg)

# Turn the power off
print("\nTurn the power off and the UID light to 'Off' for INTERCONNECT " +
      "that matches the specified ID")
try:
    INTERCONNECT_PATCH = INTERCONNECT.patch(
        operation='replace',
        path='/powerState',
        value='Off'
    )
    pprint(INTERCONNECT_PATCH.data)
except HPEOneViewException as e:
    print(e.msg)

# Updates an INTERCONNECT port.
print("\nUpdate the INTERCONNECT port")
try:
    PORT_FOR_UPDATE = PORT_D1.copy()
    PORT_FOR_UPDATE["enabled"] = False

    UPDATED = INTERCONNECT.update_port(PORT_FOR_UPDATE)
    pprint(UPDATED)
except HPEOneViewException as e:
    print(e.msg)

# Reset of port protection.
print("\nTrigger a reset of port protection of the INTERCONNECT that matches the specified ID")
try:
    RESULT = INTERCONNECT.reset_port_protection()
    pprint(RESULT)
except HPEOneViewException as e:
    print(e.msg)

# Get name servers
print("\nGet the named servers for the INTERCONNECT that matches the specified ID")

try:
    INTERCONNECT_NS = INTERCONNECT.get_name_servers()
    pprint(INTERCONNECT_NS)
except HPEOneViewException as e:
    print(e.msg)

# Get the INTERCONNECT PORTS.
try:
    print("\nGet all the INTERCONNECT PORTS.")
    PORTS = INTERCONNECT.get_PORTS()
    pprint(PORTS)

    print("\nGet an INTERCONNECT port.")
    PORTS = INTERCONNECT.get_port(PORT_D1["portId"])
    pprint(PORTS)

except HPEOneViewException as e:
    print(e.msg)

# Updates the INTERCONNECT PORTS.
print("\nUpdate the INTERCONNECT PORTS again")
try:
    UPDATED = INTERCONNECT.update_PORTS(PORTS_FOR_UPDATE)

    # filtering only UPDATED PORTS
    NAMES = [PORT_D1["portName"], PORT_D2["portName"]]
    UPDATED_PORTS = [port for port in UPDATED["PORTS"] if port["portName"] in NAMES]

    pprint(UPDATED_PORTS)
except HPEOneViewException as e:
    print(e.msg)

# Updates the INTERCONNECT CONFIGuration.
print("\nUpdate the INTERCONNECT CONFIGuration")
try:
    UPDATED = INTERCONNECT.update_CONFIGuration()
    pprint(UPDATED)
except HPEOneViewException as e:
    print(e.msg)

# Gets the INTERCONNECT CONFIGuration.
print("\nGet the INTERCONNECT pluggable module information")
try:
    PLUG_INFO = INTERCONNECT.get_pluggable_module_information()
    pprint(PLUG_INFO)
except HPEOneViewException as e:
    print(e.msg)

# Turn the power on
print("\nTurn the power on and the UID light to 'On' for INTERCONNECT " +
      "that matches the specified ID")
try:
    INTERCONNECT_PATCH = INTERCONNECT.patch(
        operation='replace',
        path='/powerState',
        value='On'
    )
    pprint(INTERCONNECT_PATCH.data)
except HPEOneViewException as e:
    print(e.msg)
