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
    "startAddress": "10:00:38:9d:20:60:00:00",
    "endAddress": "10:00:38:9d:20:6f:ff:ff",
    "rangeCategory": "Custom"
}

OPTIONS_ADDITIONAL = {
    "type": "Range",
    "name": "VWWN",
    "prefix": None,
    "enabled": True,
    "startAddress": "10:00:38:9d:20:60:00:00",
    "endAddress": "10:00:38:9d:20:6f:ff:ff",
    "rangeCategory": "Generated",
    "totalCount": 1048576,
    "freeIdCount": 1048576,
    "allocatedIdCount": 0,
    "defaultRange": True,
    "allocatorUri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/allocator",
    "collectorUri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/collector",
    "reservedIdCount": 0,
    "freeFragmentUri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/free-fragments?start=0&\
                count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/allocated-fragments?start\
                =0&count=-1",
    "category": "id-range-VWWN",
    "uri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142",
    "eTag": None,
    "created": "2013-04-08 18:11:18.049",
    "modified": "2013-04-08 18:11:18.049"
}

# Create vwwn Range for id pools
print("create vWWN range for id pools")
VWWN_RANGE = ONEVIEW_CLIENT.id_pools_vwwn_ranges.create(OPTIONS)
pprint(VWWN_RANGE)

# Get vwwn range by uri
VWWN_RANGE_BY_URI = ONEVIEW_CLIENT.id_pools_vwwn_ranges.get(VWWN_RANGE['uri'])
print("Got vwwn range from '{}' to '{}' by uri:\n   '{}'".format(VWWN_RANGE_BY_URI[\
      'startAddress'], VWWN_RANGE_BY_URI['endAddress'], VWWN_RANGE_BY_URI['uri']))

# Get vwwn range by id
VWWN_RANGE_BY_ID = ONEVIEW_CLIENT.id_pools_vwwn_ranges.get(VWWN_RANGE['uri'])
print("Got vwwn range from '{}' to '{}' by uri:\n   '{}'".format(VWWN_RANGE_BY_ID[\
      'startAddress'], VWWN_RANGE_BY_ID['endAddress'], VWWN_RANGE_BY_ID['uri']))

# Enable a vWWN range
INFORMATION = {
    "type": "Range",
    "enabled": True
}
VWWN_RANGE = ONEVIEW_CLIENT.id_pools_vwwn_ranges.enable(
    INFORMATION, VWWN_RANGE['uri'])
print("Successfully enabled vwwn range at\n   'uri': {}\n   with 'enabled': {}".format(\
    VWWN_RANGE['uri'], VWWN_RANGE['enabled']))

# Allocate a set of IDs from vwwn range
INFORMATION = {
    "count": 10
}
SUCCESSFULLY_ALLOCATED_IDS = ONEVIEW_CLIENT.id_pools_vwwn_ranges.allocate(\
    INFORMATION, VWWN_RANGE['uri'])
print("Successfully allocated IDs:")
pprint(SUCCESSFULLY_ALLOCATED_IDS)

# Get all allocated fragments in vwwn range
print("Get all allocated fragments in vwwn range")
ALLOCATED_FRAGMENTS = ONEVIEW_CLIENT.id_pools_vwwn_ranges.get_allocated_fragments(\
    VWWN_RANGE['uri'])
pprint(ALLOCATED_FRAGMENTS)

# Get all free fragments in vwwn range
print("Get all free fragments in vwwn range")
ALLOCATED_FRAGMENTS = ONEVIEW_CLIENT.id_pools_vwwn_ranges.get_free_fragments(
    VWWN_RANGE['uri'])
pprint(ALLOCATED_FRAGMENTS)

# Collect a set of IDs back to vwwn range
try:
    INFORMATION = {
        "idList": SUCCESSFULLY_ALLOCATED_IDS['idList']
    }
    SUCCESSFULLY_COLLECTED_IDS = ONEVIEW_CLIENT.id_pools_vwwn_ranges.collect(
        INFORMATION, VWWN_RANGE['uri'])
except HPEOneViewException as err:
    print(err.msg)

# Disable a vwwn range
INFORMATION = {
    "type": "Range",
    "enabled": False
}
VWWN_RANGE = ONEVIEW_CLIENT.id_pools_vwwn_ranges.enable(
    INFORMATION, VWWN_RANGE['uri'])
print("Successfully disabled vwwn range at\n   'uri': {}\n   with 'enabled': {}".format(
    VWWN_RANGE['uri'], VWWN_RANGE['enabled']))

# Delete VWWN_RANGE
ONEVIEW_CLIENT.id_pools_vwwn_ranges.delete(VWWN_RANGE)
print("Successfully deleted vwwn range")

# Create vwwn Range for id pools with more OPTIONS specified
print("Create vWWN range with more OPTIONS specified for id pools")
VWWN_RANGE = ONEVIEW_CLIENT.id_pools_vwwn_ranges.create(OPTIONS_ADDITIONAL)
pprint(VWWN_RANGE)

# Delete VWWN_RANGE
ONEVIEW_CLIENT.id_pools_vwwn_ranges.delete(VWWN_RANGE)
print("Successfully deleted newly created vwwn range")
