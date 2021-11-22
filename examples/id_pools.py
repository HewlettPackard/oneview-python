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
from hpeOneView.exceptions import HPEOneViewException
from config_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview-ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

POOL_TYPE_VSN = 'vsn'
POOL_TYPE_VWWN = 'vwwn'
POOL_TYPE_VMAC = 'vmac'
POOL_TYPE_IPV4 = 'ipv4'

ID_POOLS = ONEVIEW_CLIENT.id_pools
print("\n Gets SCHEMA: ")
SCHEMA = ID_POOLS.get_schema()
pprint(SCHEMA)

print("\n Gets the Pool: " + POOL_TYPE_VSN)
ID_POOL = ID_POOLS.get_pool_type(POOL_TYPE_VSN)
pprint(ID_POOL.data)

print("\n Gets the Pool: " + POOL_TYPE_VWWN)
ID_POOL = ID_POOLS.get_pool_type(POOL_TYPE_VWWN)
pprint(ID_POOL.data)

print("\n Gets the Pool: " + POOL_TYPE_IPV4)
ID_POOL = ID_POOLS.get_pool_type(POOL_TYPE_IPV4)
pprint(ID_POOL.data)

print("\n Gets the Pool: " + POOL_TYPE_VMAC)
ID_POOL = ID_POOLS.get_pool_type(POOL_TYPE_VMAC)
pprint(ID_POOL.data)

print("\n Enable the Id Pool")
DATA = {
    "rangeUris": ID_POOL.data['rangeUris'],
    "type": "Pool",
    "enabled": True
}
ID_POOL = ID_POOLS.update_pool_type(DATA, POOL_TYPE_VMAC)
print(" Id Pool Updated")

print("\n Generates a random range")
RND_RANGE = ID_POOLS.generate(POOL_TYPE_VSN)
pprint(RND_RANGE.data)

print("\n Allocates a set of IDs from a pool")
ALLOCATED_IDS = ID_POOLS.allocate({"count": 10}, POOL_TYPE_VSN)
pprint(ALLOCATED_IDS)

print("\n Checks the range availability in the Id pool")
RANGE_AVAILABILITY = ID_POOLS.get_check_range_availability(POOL_TYPE_VSN, ALLOCATED_IDS['idList'])
pprint(RANGE_AVAILABILITY.data)

print("\n Validates a set of user specified IDs to reserve in the pool")
IDS = [str(x)[:-3] + '200' for x in ALLOCATED_IDS['idList']]
VALIDATED = ID_POOLS.validate({'idList': IDS}, POOL_TYPE_VSN)
pprint(VALIDATED)

print("\n Validates an Id Pool")
GET_VALIDATE = ID_POOLS.validate_id_pool(POOL_TYPE_IPV4, ['172.18.9.11'])
pprint(GET_VALIDATE.data)

print("\n Collect a set of IDs back to Id Pool")
try:
    COLLECTED_IDS = ID_POOLS.collect({"idList": ALLOCATED_IDS['idList']}, POOL_TYPE_VSN)
    pprint(COLLECTED_IDS)
except HPEOneViewException as err:
    print(err.msg)
