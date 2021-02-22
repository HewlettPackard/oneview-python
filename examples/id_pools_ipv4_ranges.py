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

# Try load config from a file (if there is a config file)
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

config = try_load_from_file(config)

oneview_client = OneViewClient(config)

options = {
    "type": "Range",
    "name": "IPv4",
    "rangeCategory": "Custom",
    "startAddress": "",
    "endAddress": "",
    "subnetUri": ""
}


option = {
    "type": "Range",
    "name": "IPv4",
    "startStopFragments": [
        {
            "startAddress": "",
            "endAddress": ""
        },
        {
            "startAddress": "",
            "endAddress": ""
        }
    ],
    "subnetUri": ""
}

id_pool_ipv4_range = oneview_client.id_pools_ipv4_ranges

print("\n Create an IPv4 Range for id pools")
if oneview_client.api_version > 1000:
    ipv4_range = id_pool_ipv4_range.create(option).data
else:
    ipv4_range = id_pool_ipv4_range.create(options).data
pprint(ipv4_range)

print("\n Get the IPv4 range by uri")
ipv4Range = id_pool_ipv4_range.get_by_uri(ipv4_range['uri'])
pprint(ipv4Range.data)

print("Getting Schema")
schema = ipv4Range.get_schema()
pprint(schema)

print("\n Update the IPv4 Range")
update_ipv4Range = ipv4Range.data
update_ipv4Range['name'] = 'New Name'
ipv4_range = ipv4Range.update(update_ipv4Range)
pprint(ipv4_range.data)

print("\n Enable an IPv4 range")
ipv4_range = ipv4Range.enable(
    {
        "type": "Range",
        "enabled": True
    },
    ipv4_range.data['uri'])
print(" IPv4 range enabled successfully.")

print("Allocates a set of IDs from an IPv4 range. The maximum number of IDs in a request is 100.")
print("The allocator returned contains the list of IDs successfully allocated. Associate the IPv4 address range with a resource before requesting IDs from it.")

ipv4_range = ipv4Range.allocator({
    "count": 7,
    "idList": [
        "",
        "",
    ]
}, ipv4_range['uri'])
print("Allocated set of ID to ipv4 Range")

print("\n Get all allocated fragments in IPv4 range")
allocated_fragments = ipv4Range.get_allocated_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Get all free fragments in IPv4 range")
allocated_fragments = ipv4Range.get_free_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Disable an IPv4 range")
ipv4_range = ipv4Range.enable({
    "type": "Range",
    "enabled": False
}, ipv4_range['uri'])
print(" IPv4 range disabled successfully.")

print("\n Delete the IPv4_range")
ipv4Range.delete()
print(" Successfully deleted IPv4 range")

print("Collects a set of IDs back to an IPv4 range.")
ipv4_range = ipv4Range.collector({
    "idList": [
        "",
        "",
    ]
}, "id_ip4_range_uri")
print(ipv4_range)
