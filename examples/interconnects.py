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
from config_loader import try_load_from_file

config = {
    "ip": "<ov_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
interconnects = oneview_client.interconnects

# To run this example you must define an interconnect, otherwise, it will get the first one automatically
interconnect_uri = interconnects.get_all(0, 1)[0]['uri']
interconnect_id = interconnect_uri.replace('/rest/interconnects/', '')
interconnect = interconnects.get_by_uri(interconnect_uri)

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
interconnects_all = interconnects.get_all(0, 2)
pprint(interconnects_all)

# Get Interconnects Statistics
print("\nGet the interconnect statistics")
interconnect_statistics = interconnect.get_statistics()
if interconnect_statistics:
    pprint(interconnect_statistics['moduleStatistics'])
else:
    pprint("\nThere are no statistics for the interconnect {0}".format(interconnect.data["name"]))

# Get the Statistics from a port of an Interconnects
print("\nGet the port statistics for downlink port 1 on the interconnect "
      "that matches the specified ID")
try:
    statistics = interconnect.get_statistics(port_d1["portName"])
    pprint(statistics)
except HPEOneViewException as e:
    print(e.msg)

# Get the subport Statistics from a port of an Interconnects
print("\nGet the subport statistics for subport 1 on downlink port 2 on the interconnect "
      "that matches the specified ID")
try:
    statistics = interconnect.get_subport_statistics(port_d1["portName"],
                                                     port_d1["bayNumber"])
    pprint(statistics)
except HPEOneViewException as e:
    print(e.msg)

# Get by hostName
print("\nGet an interconnect by hostName")
try:
    interconnect_by_host = interconnects.get_by('hostName', interconnect.data["hostName"])[0]
    pprint(interconnect_by_host)
except HPEOneViewException as e:
    print(e.msg)

# Get by name
print("\nGet an interconnect by name")
try:
    interconnect_by_name = interconnects.get_by_name(interconnect.data["name"])
    pprint(interconnect_by_name.data)
except HPEOneViewException as e:
    print(e.msg)

# Turn the power off
print("\nTurn the power off and the UID light to 'Off' for interconnect " +
      "that matches the specified ID")
try:
    interconnect_patch = interconnect.patch(
        operation='replace',
        path='/powerState',
        value='Off'
    )
    pprint(interconnect_patch)
except HPEOneViewException as e:
    print(e.msg)

# Updates an interconnect port.
print("\nUpdate the interconnect port")
try:
    port_for_update = port_d1.copy()
    port_for_update["enabled"] = False

    updated = interconnect.update_port(port_for_update)
    pprint(updated)
except HPEOneViewException as e:
    print(e.msg)

# Reset of port protection.
print("\nTrigger a reset of port protection of the interconnect that matches the specified ID")
try:
    result = interconnect.reset_port_protection()
    pprint(result)
except HPEOneViewException as e:
    print(e.msg)

# Get name servers
print("\nGet the named servers for the interconnect that matches the specified ID")

try:
    interconnect_ns = interconnect.get_name_servers()
    pprint(interconnect_ns)
except HPEOneViewException as e:
    print(e.msg)

# Get the interconnect ports.
try:
    print("\nGet all the interconnect ports.")
    ports = interconnect.get_ports()
    pprint(ports)

    print("\nGet an interconnect port.")
    ports = interconnect.get_port(port_d1["portId"])
    pprint(ports)

except HPEOneViewException as e:
    print(e.msg)

# Updates the interconnect ports.
print("\nUpdate the interconnect ports")
try:
    updated = interconnect.update_ports(ports_for_update)

    # filtering only updated ports
    names = [port_d1["portName"], port_d2["portName"]]
    updated_ports = [port for port in updated["ports"] if port["portName"] in names]

    pprint(updated_ports)
except HPEOneViewException as e:
    print(e.msg)

# Updates the interconnect configuration.
print("\nUpdate the interconnect configuration")
try:
    updated = interconnect.update_configuration()
    pprint(updated)
except HPEOneViewException as e:
    print(e.msg)

# Gets the interconnect configuration.
print("\nGet the interconnect pluggable module information")
try:
    plug_info = interconnect.get_pluggable_module_information()
    pprint(plug_info)
except HPEOneViewException as e:
    print(e.msg)
