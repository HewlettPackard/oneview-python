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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

URI = '/rest/appliance/network-interfaces'

# Try load CONFIG from a file
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
network_interface = oneview_client.appliance_NETWORK_INTERFACES

# Get CONFIGured network interface from appliance
print("\nGet network interface details from appliance:\n ")
NETWORK_INTERFACES = network_interface.get_all().data['applianceNetworks']
for net_interface in NETWORK_INTERFACES:
    pprint(net_interface['hostname'])
    pprint(net_interface['interfaceName'])

# Create network interface if it doesn't exist
print("\nCreate network interface on the appliance:\n")
NI_DETAILS = {"applianceNetworks": [{
              "interfaceName": "Appliance test",
              "device": "eth0",
              "macAddress": "00:11:22:33:ff:3e",
              "ipv4Type": "STATIC",
              "ipv6Type": "UNCONFIGURE",
              "hostname": "test.com",
              "app1Ipv4Addr": "<ip_address1>",
              "app2Ipv4Addr": "<ip_address2>",
              "virtIpv4Addr": "<ip_address>",
              "ipv4Subnet": "<subnet_id>",
              "ipv4Gateway": "<gateway>",
              "ipv4NameServers": [
                  "<dns1>",
                  "<dns2>"
              ]}]}

NEW_NETWORK_INTERFACE = network_interface.create(NI_DETAILS)
pprint(NEW_NETWORK_INTERFACE.data)
print("\nNetwork Interface created successfully")

# Updates dns servers of the network interface
# For update, we use the same create method
# as PUT not supported for this resource
print("\nUpdate dns servers of the network interface:\n")
UPDATED_DETAILS = {"applianceNetworks": [{
                   "interfaceName": "Appliance test",
                   "device": "eth0",
                   "macAddress": "00:11:22:33:ff:3e",
                   "ipv4Type": "STATIC",
                   "ipv6Type": "UNCONFIGURE",
                   "hostname": "test.com",
                   "app1Ipv4Addr": "<ip_address1>",
                   "app2Ipv4Addr": "<ip_address2>",
                   "virtIpv4Addr": "<ip_address>",
                   "ipv4Subnet": "<subnet_id>",
                   "ipv4Gateway": "<gateway>",
                   "ipv4NameServers": [
                       "<dns1>",
                       "<dns3>"
                   ]}]}
UPDATED_NETWORK_INTERFACE = network_interface.create(UPDATED_DETAILS)
pprint(UPDATED_NETWORK_INTERFACE.data)
print("\nNetwork Interface updated successfully")

# Get network CONFIGuration by the mac address
print("\nGet network interface details from appliance:\n ")
if NETWORK_INTERFACES:
    NETWORK_INTERFACE_BY_MAC = network_interface.get_by_mac_address(NETWORK_INTERFACES[0]['macAddress'])
    pprint(NETWORK_INTERFACE_BY_MAC.data)

# Get unCONFIGured network interfaces on the appliance
print("\nGet unCONFIGured network interfaces from appliance:\n ")
NETWORK_INTERFACE_UNCONFIGURED = network_interface.get_all_mac_address()
pprint(NETWORK_INTERFACE_UNCONFIGURED)
