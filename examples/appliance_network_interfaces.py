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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

uri = '/rest/appliance/network-interfaces'

# Try load config from a file
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
network_interface = oneview_client.appliance_network_interfaces

# Get configured network interface from appliance
print("\nGet network interface details from appliance:\n ")
network_interfaces = network_interface.get_all().data['applianceNetworks']
for net_interface in network_interfaces:
    pprint(net_interface['hostname'])
    pprint(net_interface['interfaceName'])

# Create network interface
print("\nCreate network interface on the appliance:\n")
ni_details = {"applianceNetworks": [{
              "interfaceName": "Appliance test",
              "device": "eth0",
              "macAddress": "00:50:56:98:f1:3e",
              "ipv4Type": "STATIC",
              "ipv6Type": "UNCONFIGURE",
              "hostname": "test.com",
              "app1Ipv4Addr": "10.1.19.124",
              "app2Ipv4Addr": "10.1.19.123",
              "virtIpv4Addr": "10.1.19.120",
              "ipv4Subnet": "255.255.192.0",
              "ipv4Gateway": "10.1.0.1",
              "ipv4NameServers": [
                  "16.110.135.51",
                  "16.110.135.52"
              ]}]}

new_network_interface = network_interface.create(ni_details)
pprint(new_network_interface.data)
print("\nNetwork Interface created successfully")

# Get network configuration by the mac address
print("\nGet network interface details from appliance:\n ")
if network_interfaces:
    network_interface_by_mac = network_interface.get_by_id(network_interfaces[0]['macAddress'])
    pprint(network_interface_by_mac.data)

# Get unconfigured network interfaces on the appliance
print("\nGet unconfigured network interfaces from appliance:\n ")
network_interface_unconfigured = network_interface.get_by_mac_address()
pprint(network_interface_unconfigured.data)
