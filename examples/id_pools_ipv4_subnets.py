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

CONFIG = {
    "ip": "<oneview-ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

OPTIONS = {
    "name": "IPv4Subnet",
    "networkId": CONFIG['subnet_networkid'],
    "subnetmask": CONFIG['subnet_mask'],
    "gateway": CONFIG['subnet_gateway'],
    "domain": "example.com",
    "dnsServers": []
}

ID_POOLS_IPV4_SUBNETS = ONEVIEW_CLIENT.id_pools_ipv4_subnets
ETHERNET_NETWORKS = ONEVIEW_CLIENT.ethernet_networks

print('\n Create IPv4 subnet for id pools')
IPV4_SUBNET = ID_POOLS_IPV4_SUBNETS.create(OPTIONS)
pprint(IPV4_SUBNET.data)

print('\n Update IPv4 subnet for id pools')
UPDATED_DATA = {'name': 'Changed Name'}
IPV4_SUBNET = IPV4_SUBNET.update(UPDATED_DATA)

print('\n Get IPv4 subnet by uri')
IPV4_SUBNET_BYURI = ID_POOLS_IPV4_SUBNETS.get_by_uri(IPV4_SUBNET.data['uri'])
pprint(IPV4_SUBNET_BYURI.data)

print('\n Get all IPv4 subnet')
ALL_SUBNETS = ID_POOLS_IPV4_SUBNETS.get_all()
pprint(ALL_SUBNETS)

print('\nAssociate Subnet with Ethernet for ID allocation')
OPTIONS = {
    "name": "SubnetEthernet",
    "vlanId": 209,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
    "subnetUri": IPV4_SUBNET.data['uri']
}

ETHERNET_NETWORK = ETHERNET_NETWORKS.create(OPTIONS)

print('\nCreate Range with set of IDs')
OPTION = {
    "name": "IPv4",
    "startStopFragments": [
        {
            "startAddress": CONFIG['range_start_address'],
            "endAddress": CONFIG['range_end_address']
        }
    ],
    "subnetUri": IPV4_SUBNET.data['uri']
}
ID_POOL_IPV4_RANGE = ONEVIEW_CLIENT.id_pools_ipv4_ranges
IPV4_RANGE = ID_POOL_IPV4_RANGE.create(OPTION).data

SUBNET_ID = IPV4_SUBNET.data['allocatorUri'].split('/')[-2]
print("\n Allocates a set of IDs from a pool")
try:
    ALLOCATED_IDS = ID_POOLS_IPV4_SUBNETS.allocate({"count": 2}, SUBNET_ID)
    pprint(ALLOCATED_IDS)
except HPEOneViewException as err:
    print(err.msg)

print("\n Collect a set of IDs back to Id Pool")
try:
    COLLECTED_IDS = ID_POOLS_IPV4_SUBNETS.collect({"idList": ALLOCATED_IDS['idList']}, SUBNET_ID)
    pprint(COLLECTED_IDS)
except HPEOneViewException as err:
    print(err.msg)

print('\nDelete assocaited resource before deleting subnet')
ETHERNET_NETWORK.delete()

print('\n Delete IPv4 subnet')
IPV4_SUBNET.delete()
print(" Successfully deleted IPv4 subnet")
