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
    "type": "Range",
    "name": "IPv4",
    "rangeCategory": "Custom",
    "startAddress": "10.10.2.2",
    "endAddress": "10.10.2.254",
    "subnetUri": "/rest/id-pools/ipv4/subnets/7e77926c-195c-4984-926d-c858fde63f9b"
}

print("\n Create an IPv4 Range for id pools")
ipv4_range = oneview_client.id_pools_ipv4_ranges.create(options)
pprint(ipv4_range)

print("\n Update the IPv4 Range")
ipv4_range['name'] = 'New Name'
ipv4_range = oneview_client.id_pools_ipv4_ranges.update(ipv4_range)
pprint(ipv4_range)

print("\n Get the IPv4 range by uri")
ipv4_range_byuri = oneview_client.id_pools_ipv4_ranges.get(ipv4_range['uri'])
pprint(ipv4_range_byuri)

print("\n Enable an IPv4 range")
ipv4_range = oneview_client.id_pools_ipv4_ranges.enable(
    {
        "type": "Range",
        "enabled": True
    },
    ipv4_range['uri'])
print(" IPv4 range enabled successfully.")

print("\n Get all allocated fragments in IPv4 range")
allocated_fragments = oneview_client.id_pools_ipv4_ranges.get_allocated_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Get all free fragments in IPv4 range")
allocated_fragments = oneview_client.id_pools_ipv4_ranges.get_free_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Disable an IPv4 range")
ipv4_range = oneview_client.id_pools_ipv4_ranges.enable({
    "type": "Range",
    "enabled": False
}, ipv4_range['uri'])
print(" IPv4 range disabled successfully.")

print("\n Delete the IPv4_range")
oneview_client.id_pools_ipv4_ranges.delete(ipv4_range)
print(" Successfully deleted IPv4 range")
