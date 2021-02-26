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

config = {
    "ip": "<oneview-ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

pool_type_vsn = 'vsn'
pool_type_vwwn = 'vwwn'
pool_type_vmac = 'vmac'
pool_type_ipv4 = 'ipv4'

id_pools = oneview_client.id_pools
print("\n Gets schema: ")
schema = id_pools.schema()
pprint(schema.data)

print("\n Gets the Pool: " + pool_type_vsn)
id_pool = id_pools.get_pool_type(pool_type_vsn)
pprint(id_pool.data)

print("\n Gets the Pool: " + pool_type_vwwn)
id_pool = id_pools.get_pool_type(pool_type_vwwn)
pprint(id_pool.data)

print("\n Gets the Pool: " + pool_type_ipv4)
id_pool = id_pools.get_pool_type(pool_type_ipv4)
pprint(id_pool.data)

print("\n Gets the Pool: " + pool_type_vmac)
id_pool = id_pools.get_pool_type(pool_type_vmac)
pprint(id_pool.data)

print("\n Enable the Id Pool")
data = {
    "rangeUris": id_pool.data['rangeUris'],
    "type": "Pool",
    "enabled": True
}
id_pool = id_pools.update_pool_type(data, pool_type_vmac)
print(" Id Pool Updated")

print("\n Generates a random range")
rnd_range = id_pools.generate(pool_type_vsn)
pprint(rnd_range.data)

print("\n Allocates a set of IDs from a pool")
allocated_ids = id_pools.allocate({"count": 10}, pool_type_vsn)
pprint(allocated_ids)

print("\n Checks the range availability in the Id pool")
range_availability = id_pools.get_check_range_availability(pool_type_vsn, allocated_ids['idList'])
pprint(range_availability.data)

print("\n Validates a set of user specified IDs to reserve in the pool")
ids = [str(x)[:-3] + '200' for x in allocated_ids['idList']]
validated = id_pools.validate({'idList': ids}, pool_type_vsn)
pprint(validated)

print("\n Validates an Id Pool")
get_validate = id_pools.validate_id_pool(pool_type_ipv4, ['172.18.9.11'])
pprint(get_validate.data)

print("\n Collect a set of IDs back to Id Pool")
try:
    collected_ids = id_pools.collect({"idList": allocated_ids['idList']}, pool_type_vsn)
    pprint(collected_ids)
except HPEOneViewException as e:
    print(e.msg)
