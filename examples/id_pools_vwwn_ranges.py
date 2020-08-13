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
    "startAddress": "10:00:38:9d:20:60:00:00",
    "endAddress": "10:00:38:9d:20:6f:ff:ff",
    "rangeCategory": "Custom"
}

options_additional = {
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
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/free-fragments?start=0&count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/allocated-fragments?start=0&count=-1",
    "category": "id-range-VWWN",
    "uri":
        "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142",
    "eTag": None,
    "created": "2013-04-08 18:11:18.049",
    "modified": "2013-04-08 18:11:18.049"
}

# Create vwwn Range for id pools
print("create vWWN range for id pools")
vwwn_range = oneview_client.id_pools_vwwn_ranges.create(options)
pprint(vwwn_range)

# Get vwwn range by uri
vwwn_range_byuri = oneview_client.id_pools_vwwn_ranges.get(vwwn_range['uri'])
print("Got vwwn range from '{}' to '{}' by uri:\n   '{}'".format(vwwn_range_byuri[
      'startAddress'], vwwn_range_byuri['endAddress'], vwwn_range_byuri['uri']))

# Get vwwn range by id
vwwn_range_byId = oneview_client.id_pools_vwwn_ranges.get(vwwn_range['uri'])
print("Got vwwn range from '{}' to '{}' by uri:\n   '{}'".format(vwwn_range_byId[
      'startAddress'], vwwn_range_byId['endAddress'], vwwn_range_byId['uri']))

# Enable a vWWN range
information = {
    "type": "Range",
    "enabled": True
}
vwwn_range = oneview_client.id_pools_vwwn_ranges.enable(
    information, vwwn_range['uri'])
print("Successfully enabled vwwn range at\n   'uri': {}\n   with 'enabled': {}".format(
    vwwn_range['uri'], vwwn_range['enabled']))

# Allocate a set of IDs from vwwn range
information = {
    "count": 10
}
successfully_allocated_ids = oneview_client.id_pools_vwwn_ranges.allocate(
    information, vwwn_range['uri'])
print("Successfully allocated IDs:")
pprint(successfully_allocated_ids)

# Get all allocated fragments in vwwn range
print("Get all allocated fragments in vwwn range")
allocated_fragments = oneview_client.id_pools_vwwn_ranges.get_allocated_fragments(
    vwwn_range['uri'])
pprint(allocated_fragments)

# Get all free fragments in vwwn range
print("Get all free fragments in vwwn range")
allocated_fragments = oneview_client.id_pools_vwwn_ranges.get_free_fragments(
    vwwn_range['uri'])
pprint(allocated_fragments)

# Collect a set of IDs back to vwwn range
try:
    information = {
        "idList": successfully_allocated_ids['idList']
    }
    successfully_collected_ids = oneview_client.id_pools_vwwn_ranges.collect(
        information, vwwn_range['uri'])
except HPEOneViewException as e:
    print(e.msg)

# Disable a vwwn range
information = {
    "type": "Range",
    "enabled": False
}
vwwn_range = oneview_client.id_pools_vwwn_ranges.enable(
    information, vwwn_range['uri'])
print("Successfully disabled vwwn range at\n   'uri': {}\n   with 'enabled': {}".format(
    vwwn_range['uri'], vwwn_range['enabled']))

# Delete vwwn_range
oneview_client.id_pools_vwwn_ranges.delete(vwwn_range)
print("Successfully deleted vwwn range")

# Create vwwn Range for id pools with more options specified
print("Create vWWN range with more options specified for id pools")
vwwn_range = oneview_client.id_pools_vwwn_ranges.create(options_additional)
pprint(vwwn_range)

# Delete vwwn_range
oneview_client.id_pools_vwwn_ranges.delete(vwwn_range)
print("Successfully deleted newly created vwwn range")
