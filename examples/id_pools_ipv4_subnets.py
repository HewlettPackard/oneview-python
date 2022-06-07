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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview-ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

options = {
    "name": "iscsi_subnet",
    "networkId": config["subnet_networkid"],
    "subnetmask": config["subnet_mask"],
    "gateway": config["subnet_gateway"],
    "domain": "example.com",
    "dnsServers": []
}

id_pools_ipv4_subnets = oneview_client.id_pools_ipv4_subnets
ethernet_networks = oneview_client.ethernet_networks

print('\n Create IPv4 subnet for id pools')
ipv4_subnet = id_pools_ipv4_subnets.create(options)
pprint(ipv4_subnet.data)

print('\n Update IPv4 subnet for id pools')
updated_data = {'name': 'Changed Name'}
ipv4_subnet = ipv4_subnet.update(updated_data)

print('\n Get IPv4 subnet by uri')
ipv4_subnet = id_pools_ipv4_subnets.get_by_uri(ipv4_subnet.data['uri'])
pprint(ipv4_subnet)

print('\n Get all IPv4 subnet')
all_subnets = id_pools_ipv4_subnets.get_all()
pprint(all_subnets)

print('\nAssociate Subnet with Ethernet for ID allocation')
options = {
    "name": "SubnetEthernet",
    "vlanId": 209,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
    "subnetUri": ipv4_subnet.data['uri']
}

ethernet_network = ethernet_networks.create(options)
ethernet_network =  ethernet_networks.get_by_name('SubnetEthernet')
print('\nCreate Range with set of IDs')
option = {
    "name": "IPv4iscsi",
    "startStopFragments": [
        {
            "startAddress": config["range_start_address"],
            "endAddress": config["range_end_address"]
        }
    ],
    "subnetUri": ipv4_subnet.data['uri']
}
id_pool_ipv4_range = oneview_client.id_pools_ipv4_ranges
ipv4_range = id_pool_ipv4_range.create(option).data

subnet_id = ipv4_subnet.data['allocatorUri'].split('/')[-2]
print("++",subnet_id)
print("\n Allocates a set of IDs from a pool")
try:
    allocated_ids = id_pools_ipv4_subnets.allocate({"count": 2}, subnet_id)
    pprint(allocated_ids)
except HPEOneViewException as e:
    print(e.msg)

print("\n Collect a set of IDs back to Id Pool")
try:
    collected_ids = id_pools_ipv4_subnets.collect({"idList": allocated_ids['idList']}, subnet_id)
    pprint(collected_ids)
except HPEOneViewException as e:
    print(e.msg)

print('\nDelete assocaited resource before deleting subnet')
ethernet_network.delete()

print('\n Delete IPv4 subnet')
ipv4_subnet.delete()
print(" Successfully deleted IPv4 subnet")
options = {
    "name": "iscsi_subnet",
    "networkId": config["subnet_networkid"],
    "subnetmask": config["subnet_mask"],
    "gateway": config["subnet_gateway"],
    "domain": "example.com",
    "dnsServers": []
}
# Create a iscsi network for automation
ipv4_subnet = id_pools_ipv4_subnets.create(options)
option = {
    "name": "IPv4_mgmt",
    "startStopFragments": [
        {
            "startAddress": config["range_start_address"],
            "endAddress": config["range_end_address"]
        }
    ],
    "subnetUri": ipv4_subnet.data['uri']
}

if oneview_client.api_version > 1000:
    ipv4_range = id_pool_ipv4_range.create(option).data
    