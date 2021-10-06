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

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
ENCLOSURE_GROUPs = oneview_client.ENCLOSURE_GROUPs
id_pool_IPV4_RANGE = oneview_client.id_pools_IPV4_RANGEs
id_pool_IPV4_SUBNET = oneview_client.id_pools_IPV4_SUBNETs

OPTIONS = {
    "name": "IPv4",
    "rangeCategory": "Custom",
    "startAddress": "",
    "endAddress": "",
    "subnetUri": ""
}

SUBNET_OPTIONS = {
    "name": "iscsi_Subnet",
    "networkId": CONFIG['subnet_networkid'],
    "subnetmask": CONFIG['subnet_mask'],
    "gateway": CONFIG['subnet_gateway'],
    "domain": "example.com",
}

print('\n Create IPv4 subnet to have Range of IPs')
IPV4_SUBNET = id_pool_IPV4_SUBNET.create(SUBNET_OPTIONS)
pprint(IPV4_SUBNET.data)

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

print("\n Create an IPv4 Range for id pools")
if oneview_client.api_version > 1000:
    IPV4_RANGE = id_pool_IPV4_RANGE.create(OPTION).data
else:
    IPV4_RANGE = id_pool_IPV4_RANGE.create(OPTIONS).data
pprint(IPV4_RANGE)

print("\n Get the IPv4 range by uri")
IPV4RANGE = id_pool_IPV4_RANGE.get_by_uri(IPV4_RANGE['uri'])
pprint(IPV4RANGE.data)

print("Getting Schema")
SCHEMA = IPV4RANGE.get_SCHEMA()
pprint(SCHEMA)

print("\n Update the IPv4 Range")
UPDATE_IPV4RANGE = IPV4RANGE.data
UPDATE_IPV4RANGE['name'] = 'New Name'
IPV4_RANGE = IPV4RANGE.update(UPDATE_IPV4RANGE)
pprint(IPV4_RANGE.data)

print("\n Enable an IPv4 range")
IPV4_RANGE = IPV4RANGE.enable(
    {
        "type": "Range",
        "enabled": True
    },
    IPV4_RANGE.data['uri'])
print(" IPv4 range enabled successfully.")

print("\nAssociate EG with range for allocation")
EG_OPTIONS = {
    "name": "RangeEG",
    "ipAddressingMode": "ipPool",
    "ipRangeUris": [IPV4_RANGE['uri']],
    "enclosureCount": 3,
}
ENCLOSURE_GROUP = ENCLOSURE_GROUPs.create(EG_OPTIONS)

print("\nAllocates a set of IDs from an IPv4 range")

IPV4_RANGE_UPDATED = IPV4RANGE.update_allocator({
    "count": 2,
}, IPV4_RANGE['uri'])
pprint(IPV4_RANGE_UPDATED)
print("Allocated set of ID to ipv4 Range")


print("\n Get all allocated fragments in IPv4 range")
ALLOCATED_FRAGMENTS = IPV4RANGE.get_ALLOCATED_FRAGMENTS(IPV4_RANGE['uri'])
pprint(ALLOCATED_FRAGMENTS)

print("\n Get all free fragments in IPv4 range")
ALLOCATED_FRAGMENTS = IPV4RANGE.get_free_fragments(IPV4_RANGE['uri'])
pprint(ALLOCATED_FRAGMENTS)

print("Collects a set of IDs back to an IPv4 range.")
IPV4_RANGE_COLLECTOR = IPV4RANGE.update_collector({
    "idList": IPV4_RANGE_UPDATED['idList']
}, IPV4_RANGE['uri'])
print(IPV4_RANGE_COLLECTOR)

print("\nRemove associated EG before deletion")
ENCLOSURE_GROUP.delete()

print("\n Disable an IPv4 range")
IPV4_RANGE = IPV4RANGE.enable({
    "type": "Range",
    "enabled": False
}, IPV4_RANGE['uri'])
print(" IPv4 range disabled successfully.")

print("\n Delete the IPv4_range")
IPV4RANGE.delete()
print(" Successfully deleted IPv4 range")
