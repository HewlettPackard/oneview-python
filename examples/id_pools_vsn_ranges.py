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
from config_loader import try_load_from_file

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

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
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/free-fragments?start=0&\
                count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocated-fragments?start=\
                0&count=-1",
    "category": "id-range-VSN",
    "uri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4",
    "eTag": None,
    "created": "2013-04-08 18:11:17.862",
    "modified": "2013-04-08 18:11:17.862"
}

# Create VSN Range for id pools
VSN_RANGE = ONEVIEW_CLIENT.id_pools_vsn_ranges.create(OPTIONS)
pprint(VSN_RANGE)

# Get vsn range by uri
VSN_RANGE_BY_URI = ONEVIEW_CLIENT.id_pools_vsn_ranges.get(VSN_RANGE['uri'])
print("Got vsn range from '{}' to '{}' by uri:\n   '{}'".format(VSN_RANGE_BY_URI[\
      'startAddress'], VSN_RANGE_BY_URI['endAddress'], VSN_RANGE_BY_URI['uri']))

# Get vsn range by id
VSN_RANGE_BY_ID = ONEVIEW_CLIENT.id_pools_vsn_ranges.get(VSN_RANGE['uri'])
print("Got vsn range from '{}' to '{}' by uri:\n   '{}'".format(VSN_RANGE_BY_ID[\
      'startAddress'], VSN_RANGE_BY_ID['endAddress'], VSN_RANGE_BY_ID['uri']))

# Enable a vSN range
INFORMATION = {
    "type": "Range",
    "enabled": True
}
VSN_RANGE = ONEVIEW_CLIENT.id_pools_vsn_ranges.enable(
    INFORMATION, VSN_RANGE['uri'])
print("Successfully enabled vsn range at\n   'uri': {}\n   with 'enabled': {}".format(\
    VSN_RANGE['uri'], VSN_RANGE['enabled']))

# Allocate a set of IDs from vsn range
INFORMATION = {
    "count": 10
}
SUCCESSFULLY_ALLOCATED_IDS = ONEVIEW_CLIENT.id_pools_vsn_ranges.allocate(\
    INFORMATION, VSN_RANGE['uri'])
print("Successfully allocated IDs:")
pprint(SUCCESSFULLY_ALLOCATED_IDS)

# Get all allocated fragments in vsn range
print("Get all allocated fragments in vsn range")
ALLOCATED_FRAGMENTS = ONEVIEW_CLIENT.id_pools_vsn_ranges.get_allocated_fragments(
    VSN_RANGE['uri'])
pprint(ALLOCATED_FRAGMENTS)

# Get all free fragments in vsn range
print("Get all free fragments in vsn range")
ALLOCATED_FRAGMENTS = ONEVIEW_CLIENT.id_pools_vsn_ranges.get_free_fragments(
    VSN_RANGE['uri'])
pprint(ALLOCATED_FRAGMENTS)

# Collect a set of IDs back to vsn range
try:
    INFORMATION = {
        "idList": SUCCESSFULLY_ALLOCATED_IDS['idList']
    }
    SUCCESSFULLY_COLLECTED_IDS = ONEVIEW_CLIENT.id_pools_vsn_ranges.collect(
        INFORMATION, VSN_RANGE['uri'])
except HPEOneViewException as err:
    print(err.msg)

# Disable a vsn range
INFORMATION = {
    "type": "Range",
    "enabled": False
}
VSN_RANGE = ONEVIEW_CLIENT.id_pools_vsn_ranges.enable(
    INFORMATION, VSN_RANGE['uri'])
print("Successfully disabled vsn range at\n   'uri': {}\n   with 'enabled': {}".format(
    VSN_RANGE['uri'], VSN_RANGE['enabled']))

# Delete VSN_RANGE
ONEVIEW_CLIENT.id_pools_vsn_ranges.delete(VSN_RANGE)
print("Successfully deleted vsn range")

# Create vsn Range for id pools with more OPTIONS specified
print("Create vsn range with more OPTIONS specified for id pools")
VSN_RANGE = ONEVIEW_CLIENT.id_pools_vsn_ranges.create(OPTIONS_ADDITIONAL)
pprint(VSN_RANGE)

# Delete VSN_RANGE
ONEVIEW_CLIENT.id_pools_vsn_ranges.delete(VSN_RANGE)
print("Successfully deleted newly created vsn range")
