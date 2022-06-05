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
enclosure_groups = oneview_client.enclosure_groups
id_pool_ipv4_range = oneview_client.id_pools_ipv4_ranges
id_pool_ipv4_subnet = oneview_client.id_pools_ipv4_subnets

options = {
    "name": "IPv4",
    "rangeCategory": "Custom",
    "startAddress": "",
    "endAddress": "",
    "subnetUri": ""
}

subnet_options = {
    "name": "mgmt_subnet",
    "networkId": config["networkId"],
    "subnetmask": config["subnetmask"],
    "gateway": config["gateway"],
    "domain": "example.com",
}

print('\n Create IPv4 subnet to have Range of IPs')
ipv4_subnet = id_pool_ipv4_subnet.create(subnet_options)
pprint(ipv4_subnet.data)

option = {
    "name": "IPv4_mgmt",
    "startStopFragments": [
        {
            "startAddress": config["startAddress"],
            "endAddress": config["endAddress"]
        }
    ],
    "subnetUri": ipv4_subnet.data['uri']
}

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

print("\nAssociate EG with range for allocation")
eg_options = {
    "name": "RangeEG",
    "ipAddressingMode": "ipPool",
    "ipRangeUris": [ipv4_range['uri']],
    "enclosureCount": 3,
}
enclosure_group = enclosure_groups.create(eg_options)

print("\nAllocates a set of IDs from an IPv4 range")

ipv4_range_updated = ipv4Range.update_allocator({
    "count": 2,
}, ipv4_range['uri'])
pprint(ipv4_range_updated)
print("Allocated set of ID to ipv4 Range")


print("\n Get all allocated fragments in IPv4 range")
allocated_fragments = ipv4Range.get_allocated_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Get all free fragments in IPv4 range")
allocated_fragments = ipv4Range.get_free_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("Collects a set of IDs back to an IPv4 range.")
ipv4_range_collector = ipv4Range.update_collector({
    "idList": ipv4_range_updated['idList']
}, ipv4_range['uri'])
print(ipv4_range_collector)

print("\nRemove associated EG before deletion")
enclosure_group.delete()

print("\n Disable an IPv4 range")
ipv4_range = ipv4Range.enable({
    "type": "Range",
    "enabled": False
}, ipv4_range['uri'])
print(" IPv4 range disabled successfully.")

print("\n Delete the IPv4_range")
ipv4Range.delete()
print(" Successfully deleted IPv4 range")
print('\n Delete IPv4 subnet')
ipv4_subnet.delete()
print(" Successfully deleted IPv4 subnet")
# Create a mgmt network for automation
ipv4_subnet = id_pool_ipv4_subnet.create(subnet_options)
option = {
    "name": "IPv4_mgmt",
    "startStopFragments": [
        {
            "startAddress": config["startAddress"],
            "endAddress": config["endAddress"]
        }
    ],
    "subnetUri": ipv4_subnet.data['uri']
}

if oneview_client.api_version > 1000:
    ipv4_range = id_pool_ipv4_range.create(option).data
