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
from hpeOneView.exceptions import HPEOneViewException
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

OPTIONS = {
    "type": "Range",
    "startAddress": "VCUS6EI000",
    "endAddress": "VCUS6EIZZZ",
    "rangeCategory": "Custom"
}

OPTIONS_ADDITIONAL = {
    "type": "Range",
    "name": "VSN",
    "prefix": None,
    "enabled": True,
    "startAddress": "VCGV2Y4000",
    "endAddress": "VCGV2Y4ZZZ",
    "rangeCategory": "Generated",
    "totalCount": 46656,
    "freeIdCount": 46656,
    "allocatedIdCount": 0,
    "defaultRange": True,
    "allocatorUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocator",
    "collectorUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/collector",
    "reservedIdCount": 0,
    "freeFragmentUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/free-fragments?start=0&count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocated-fragments?start=0&count=-1",
    "category": "id-range-VSN",
    "uri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4",
    "eTag": None,
    "created": "2013-04-08 18:11:17.862",
    "modified": "2013-04-08 18:11:17.862"
}

# Create VSN Range for id pools
vsn_range = oneview_client.id_pools_vsn_ranges.create(OPTIONS)
pprint(vsn_range)

# Get vsn range by uri
vsn_range_byuri = oneview_client.id_pools_vsn_ranges.get(vsn_range['uri'])
print("Got vsn range from '{}' to '{}' by uri:\n   '{}'".format(vsn_range_byuri[
      'startAddress'], vsn_range_byuri['endAddress'], vsn_range_byuri['uri']))

# Get vsn range by id
vsn_range_byId = oneview_client.id_pools_vsn_ranges.get(vsn_range['uri'])
print("Got vsn range from '{}' to '{}' by uri:\n   '{}'".format(vsn_range_byId[
      'startAddress'], vsn_range_byId['endAddress'], vsn_range_byId['uri']))

# Enable a vSN range
INFORMATION = {
    "type": "Range",
    "enabled": True
}
vsn_range = oneview_client.id_pools_vsn_ranges.enable(
    INFORMATION, vsn_range['uri'])
print("Successfully enabled vsn range at\n   'uri': {}\n   with 'enabled': {}".format(
    vsn_range['uri'], vsn_range['enabled']))

# Allocate a set of IDs from vsn range
INFORMATION = {
    "count": 10
}
successfully_allocated_ids = oneview_client.id_pools_vsn_ranges.allocate(
    INFORMATION, vsn_range['uri'])
print("Successfully allocated IDs:")
pprint(successfully_allocated_ids)

# Get all allocated fragments in vsn range
print("Get all allocated fragments in vsn range")
allocated_fragments = oneview_client.id_pools_vsn_ranges.get_allocated_fragments(
    vsn_range['uri'])
pprint(allocated_fragments)

# Get all free fragments in vsn range
print("Get all free fragments in vsn range")
allocated_fragments = oneview_client.id_pools_vsn_ranges.get_free_fragments(
    vsn_range['uri'])
pprint(allocated_fragments)

# Collect a set of IDs back to vsn range
try:
    INFORMATION = {
        "idList": successfully_allocated_ids['idList']
    }
    successfully_collected_ids = oneview_client.id_pools_vsn_ranges.collect(
        INFORMATION, vsn_range['uri'])
except HPEOneViewException as e:
    print(e.msg)

# Disable a vsn range
INFORMATION = {
    "type": "Range",
    "enabled": False
}
vsn_range = oneview_client.id_pools_vsn_ranges.enable(
    INFORMATION, vsn_range['uri'])
print("Successfully disabled vsn range at\n   'uri': {}\n   with 'enabled': {}".format(
    vsn_range['uri'], vsn_range['enabled']))

# Delete vsn_range
oneview_client.id_pools_vsn_ranges.delete(vsn_range)
print("Successfully deleted vsn range")

# Create vsn Range for id pools with more OPTIONS specified
print("Create vsn range with more OPTIONS specified for id pools")
vsn_range = oneview_client.id_pools_vsn_ranges.create(OPTIONS_ADDITIONAL)
pprint(vsn_range)

# Delete vsn_range
oneview_client.id_pools_vsn_ranges.delete(vsn_range)
print("Successfully deleted newly created vsn range")
