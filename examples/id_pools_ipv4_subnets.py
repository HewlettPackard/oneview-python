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
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

options = {
    "type": "Subnet",
    "name": "IPv4Subnet",
    "networkId": '10.10.1.0',
    "subnetmask": "255.255.255.0",
    "gateway": "10.10.1.1",
    "domain": "example.com",
    "dnsServers": ["10.10.10.215"]
}

print('\n Create IPv4 subnet for id pools')
ipv4_subnet = oneview_client.id_pools_ipv4_subnets.create(options)
pprint(ipv4_subnet)

print('\n Update IPv4 subnet for id pools')
ipv4_subnet['name'] = 'Changed Name'
ipv4_subnet = oneview_client.id_pools_ipv4_subnets.update(ipv4_subnet)

print('\n Get IPv4 subnet by uri')
ipv4_subnet_byuri = oneview_client.id_pools_ipv4_subnets.get(ipv4_subnet['uri'])
pprint(ipv4_subnet_byuri)

print('\n Get all IPv4 subnet')
all_subnets = oneview_client.id_pools_ipv4_subnets.get_all()
pprint(all_subnets)

print('\n Delete IPv4 subnet')
oneview_client.id_pools_ipv4_subnets.delete(ipv4_subnet)
print(" Successfully deleted IPv4 subnet")
