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
    "startAddress": "E2:13:C5:F0:00:00",
    "endAddress": "E2:13:C5:FF:FF:FF",
    "rangeCategory": "Custom"
}

OPTIONS_ADDITIONAL = {
    "type": "Range",
    "name": None,
    "prefix": None,
    "enabled": True,
    "rangeCategory": "Generated",
    "startAddress": "E2:13:C5:F0:00:00",
    "endAddress": "E2:13:C5:FF:FF:FF",
    "totalCount": 1048575,
    "freeIdCount": 1048575,
    "allocatedIdCount": 0,
    "allocatorUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/allocator",
    "collectorUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/collector",
    "reservedIdCount": 0,
    "freeFragmentUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/free-fragments?start=0&count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/allocated-fragments?start=0&count=-1",
    "uri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8",
    "category": "id-range-VMAC",
    "eTag": None,
    "created": "2013-03-20 01:29:10.570",
    "modified": "2013-03-20 01:29:10.570"

}

# Create vmac Range for id pools
vmac_range = oneview_client.id_pools_vmac_ranges.create(OPTIONS)
pprint(vmac_range)

# Get vmac range by uri
vmac_range_byuri = oneview_client.id_pools_vmac_ranges.get(vmac_range['uri'])
print("Got vmac range from '{}' to '{}' by uri:\n   '{}'".format(vmac_range_byuri[
      'startAddress'], vmac_range_byuri['endAddress'], vmac_range_byuri['uri']))

# Get vmac range by id
vmac_range_byId = oneview_client.id_pools_vmac_ranges.get(vmac_range['uri'])
print("Got vmac range from '{}' to '{}' by uri:\n   '{}'".format(vmac_range_byId[
      'startAddress'], vmac_range_byId['endAddress'], vmac_range_byId['uri']))

# Enable a vMAC range
INFORMATION = {
    "type": "Range",
    "enabled": True
}
vmac_range = oneview_client.id_pools_vmac_ranges.enable(
    INFORMATION, vmac_range['uri'])
print("Successfully enabled vmac range at\n   'uri': {}\n   with 'enabled': {}".format(
    vmac_range['uri'], vmac_range['enabled']))

# Allocate a set of IDs from vmac range
INFORMATION = {
    "count": 10
}
successfully_allocated_ids = oneview_client.id_pools_vmac_ranges.allocate(
    INFORMATION, vmac_range['uri'])
print("Successfully allocated IDs:")
pprint(successfully_allocated_ids)

# Get all allocated fragments in vmac range
print("Get all allocated fragments in vmac range")
allocated_fragments = oneview_client.id_pools_vmac_ranges.get_allocated_fragments(
    vmac_range['uri'])
pprint(allocated_fragments)

# Get all free fragments in vmac range
print("Get all free fragments in vmac range")
allocated_fragments = oneview_client.id_pools_vmac_ranges.get_free_fragments(
    vmac_range['uri'])
pprint(allocated_fragments)

# Collect a set of IDs back to vmac range
try:
    INFORMATION = {
        "idList": successfully_allocated_ids['idList']
    }
    successfully_collected_ids = oneview_client.id_pools_vmac_ranges.collect(
        INFORMATION, vmac_range['uri'])
except HPEOneViewException as e:
    print(e.msg)

# Disable a vmac range
INFORMATION = {
    "type": "Range",
    "enabled": False
}
vmac_range = oneview_client.id_pools_vmac_ranges.enable(
    INFORMATION, vmac_range['uri'])
print("Successfully disabled vmac range at\n   'uri': {}\n   with 'enabled': {}".format(
    vmac_range['uri'], vmac_range['enabled']))

# Delete vmac_range
oneview_client.id_pools_vmac_ranges.delete(vmac_range)
print("Successfully deleted vmac range")

# Create vmac Range for id pools with more OPTIONS specified
print("Create vMAC range with more OPTIONS specified for id pools")
vmac_range = oneview_client.id_pools_vmac_ranges.create(OPTIONS_ADDITIONAL)
pprint(vmac_range)

# Delete vmac_range
oneview_client.id_pools_vmac_ranges.delete(vmac_range)
print("Successfully deleted newly created vMAC range")
