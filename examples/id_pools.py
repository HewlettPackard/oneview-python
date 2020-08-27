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

pool_type_vsn = 'vsn'
pool_type_vwwn = 'vwwn'
pool_type_vmac = 'vmac'
pool_type_ipv4 = 'ipv4'

print("\n Gets the Pool: " + pool_type_vsn)
id_pool = oneview_client.id_pools.get(pool_type_vsn)
pprint(id_pool)

print("\n Gets the Pool: " + pool_type_vwwn)
id_pool = oneview_client.id_pools.get(pool_type_vwwn)
pprint(id_pool)

print("\n Gets the Pool: " + pool_type_vmac)
id_pool = oneview_client.id_pools.get(pool_type_vmac)
pprint(id_pool)

print("\n Gets the Pool: " + pool_type_ipv4)
id_pool = oneview_client.id_pools.get(pool_type_ipv4)
pprint(id_pool)

print("\n Enable the Id Pool")
id_pool = oneview_client.id_pools.enable({"type": "Pool",
                                          "enabled": True},
                                         pool_type_vsn)
print(" Id Pool enabled")

print("\n Generates a random range")
rnd_range = oneview_client.id_pools.generate(pool_type_vsn)
pprint(rnd_range)

print("\n Allocates a set of IDs from a pool")
allocated_ids = oneview_client.id_pools.allocate({"count": 10
                                                  }, pool_type_vsn)
pprint(allocated_ids)

print("\n Checks the range availability in the Id pool")
range_availability = oneview_client.id_pools.get_check_range_availability(pool_type_vsn,
                                                                          ['VCGYOAF00P',
                                                                           'VCGYOAF002'])
pprint(range_availability)

print("\n Validates a set of user specified IDs to reserve in the pool")
validated = oneview_client.id_pools.validate({'idList': ['VCGYOAA023',
                                                         'VCGYOAA024']}, pool_type_vsn)
pprint(validated)

print("\n Validates an Id Pool")
get_validate = oneview_client.id_pools.validate_id_pool(pool_type_ipv4,
                                                        ['172.18.9.11'])
pprint(get_validate)

print("\n Collect a set of IDs back to Id Pool")
try:
    collected_ids = oneview_client.id_pools.collect({"idList": allocated_ids['idList']},
                                                    pool_type_vsn)
    pprint(collected_ids)
except HPEOneViewException as e:
    print(e.msg)
