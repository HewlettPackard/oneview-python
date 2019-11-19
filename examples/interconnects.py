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
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

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

# To run this example you must define an interconnect, otherwise, it will get the first one automatically
interconnect_id = ""
if not interconnect_id:
    interconnect_id = oneview_client.interconnects.get_all(0, 1)[0]['uri']

port_d1 = {
    "type": "port",
    "portName": "d1",
    "bayNumber": 1,
    "enabled": False,
    "portId": "{0}:d1".format(interconnect_id)
}

port_d2 = {
    "portName": "d2",
    "enabled": False,
    "portId": "{0}:d2".format(interconnect_id)
}

ports_for_update = [port_d1, port_d2]

# Get the first two Interconnects
print("\nGet the first two interconnects")
try:
    interconnects = oneview_client.interconnects.get_all(0, 2)
    pprint(interconnects)
except HPOneViewException as e:
    print(e.msg)

# Get Interconnects Statistics
print("\nGet the interconnect statistics")
try:
    interconnect_statistics = oneview_client.interconnects.get_statistics(interconnect_id)
    if interconnect_statistics:
        pprint(interconnect_statistics['moduleStatistics'])
    else:
        pprint("\nThere are no statistics for the interconnect {0}".format(interconnect_id))
except HPOneViewException as e:
    print(e.msg)

# Get the Statistics from a port of an Interconnects
print("\nGet the port statistics for downlink port 1 on the interconnect "
      "that matches the specified ID")
try:
    statistics = oneview_client.interconnects.get_statistics(interconnect_id, port_d1["portName"])
    pprint(statistics)
except HPOneViewException as e:
    print(e.msg)

# Get the subport Statistics from a port of an Interconnects
print("\nGet the subport statistics for subport 1 on downlink port 2 on the interconnect "
      "that matches the specified ID")
try:
    statistics = oneview_client.interconnects.get_subport_statistics(interconnect_id,
                                                                     port_d1["portName"],
                                                                     port_d1["bayNumber"])
    pprint(statistics)
except HPOneViewException as e:
    print(e.msg)

# Get by ID
print("\nGet Interconnect that matches the specified ID")
try:
    interconnect = oneview_client.interconnects.get(interconnect_id)
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Get by hostName
print("\nGet an interconnect by hostName")
try:
    interconnect = oneview_client.interconnects.get_by('hostName', interconnect["hostName"])[0]
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Get by name
print("\nGet an interconnect by name")
try:
    interconnect = oneview_client.interconnects.get_by_name(interconnect["name"])
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Turn the power off
print("\nTurn the power off and the UID light to 'Off' for interconnect " +
      "that matches the specified ID")
try:
    interconnect = oneview_client.interconnects.patch(
        id_or_uri=interconnect_id,
        operation='replace',
        path='/powerState',
        value='Off'
    )
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Updates an interconnect port.
print("\nUpdate the interconnect port")
try:
    port_for_update = port_d1.copy()
    port_for_update["enabled"] = False

    updated = oneview_client.interconnects.update_port(port_for_update, interconnect_id)
    pprint(updated)
except HPOneViewException as e:
    print(e.msg)

# Reset of port protection.
print("\nTrigger a reset of port protection of the interconnect that matches the specified ID")
try:
    result = oneview_client.interconnects.reset_port_protection(interconnect_id)
    pprint(result)
except HPOneViewException as e:
    print(e.msg)

# Get name servers
print("\nGet the named servers for the interconnect that matches the specified ID")

try:
    interconnect_ns = oneview_client.interconnects.get_name_servers(interconnect_id)
    pprint(interconnect_ns)
except HPOneViewException as e:
    print(e.msg)

# Get the interconnect ports.
try:
    print("\nGet all the interconnect ports.")
    ports = oneview_client.interconnects.get_ports(interconnect_id)
    pprint(ports)

    print("\nGet an interconnect port.")
    ports = oneview_client.interconnects.get_port(interconnect_id, port_d1["portId"])
    pprint(ports)

except HPOneViewException as e:
    print(e.msg)

# Updates the interconnect ports.
print("\nUpdate the interconnect ports")

try:
    updated = oneview_client.interconnects.update_ports(ports_for_update, interconnect_id)

    # filtering only updated ports
    names = [port_d1["portName"], port_d2["portName"]]
    updated_ports = [port for port in updated["ports"] if port["portName"] in names]

    pprint(updated_ports)
except HPOneViewException as e:
    print(e.msg)

# Updates the interconnect configuration.
print("\nUpdate the interconnect configuration")

try:
    updated = oneview_client.interconnects.update_configuration(interconnect_id)
    pprint(updated)
except HPOneViewException as e:
    print(e.msg)

# Gets the interconnect configuration.
print("\nGet the interconnect pluggable module information")

try:
    plug_info = oneview_client.interconnects.get_pluggable_module_information(interconnect_id)
    pprint(plug_info)
except HPOneViewException as e:
    print(e.msg)
