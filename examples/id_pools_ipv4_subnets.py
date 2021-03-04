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
    "name": "IPv4Subnet",
    "networkId": '192.169.1.0',
    "subnetmask": "255.255.255.0",
    "gateway": "192.169.1.1",
    "domain": "example.com",
    "dnsServers": ["192.169.1.215"]
}

id_pools_ipv4_subnets = oneview_client.id_pools_ipv4_subnets

print('\n Create IPv4 subnet for id pools')
ipv4_subnet = id_pools_ipv4_subnets.create(options)
pprint(ipv4_subnet.data)

print('\n Update IPv4 subnet for id pools')
updated_data = {'name': 'Changed Name'}
ipv4_subnet = ipv4_subnet.update(updated_data)

print('\n Get IPv4 subnet by uri')
ipv4_subnet_byuri = id_pools_ipv4_subnets.get_by_uri(ipv4_subnet.data['uri'])
pprint(ipv4_subnet_byuri.data)

print('\n Get all IPv4 subnet')
all_subnets = id_pools_ipv4_subnets.get_all()
pprint(all_subnets)

subnet_id = ipv4_subnet.data['allocatorUri'].split('/')[-2]
print("\n Allocates a set of IDs from a pool")
try:
    allocated_ids = id_pools_ipv4_subnets.allocate({"count": 10}, subnet_id)
    pprint(allocated_ids)
except HPEOneViewException as e:
    print(e.msg)

print("\n Collect a set of IDs back to Id Pool")
try:
    collected_ids = id_pools_ipv4_subnets.collect({"idList": allocated_ids['idList']}, subnet_id)
    pprint(collected_ids)
except HPEOneViewException as e:
    print(e.msg)

print('\n Delete IPv4 subnet')
ipv4_subnet.delete()
print(" Successfully deleted IPv4 subnet")

# Create iscsi subnet for automation purpose

iscsi_options = {
    "name": "iscsi_Subnet",
    "networkId": '192.168.10.0',
    "subnetmask": "255.255.255.0",
    "gateway": "192.168.10.1",
    "domain": "iscsi.com",
}

print('\n Create IPv4 subnet for iscsi')
ipv4_subnet = id_pools_ipv4_subnets.create(iscsi_options)
pprint(ipv4_subnet.data)

