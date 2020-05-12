# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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

from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file
from pprint import pprint

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

scope_uris = '/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf'
storage_pool_uris = ['/rest/storage-pools/5F9CA89B-C632-4F09-BC55-A8AA00DA5C4A']

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient.from_json_file('config.json')
storage_systems = oneview_client.storage_systems
storage_pools = oneview_client.storage_pools

# Find or add storage system
print("Find or add storage system")
s_systems = storage_systems.get_all()
if s_systems:
    s_system_data = s_systems[0]
    s_system = storage_systems.get_by_uri(s_system_data["uri"])
    storage_system_added = False
    print("   Found storage system '{}' at uri: {}".format(
        s_system.data['name'], s_system.data['uri']))
else:
    options = {
        "hostname": config['storage_system_hostname'],
        "username": config['storage_system_username'],
        "password": config['storage_system_password'],
        "family": config['storage_system_family']
    }
    s_system = storage_systems.add(options)
    s_system_data = s_system.data.copy()
    s_system_data['deviceSpecificAttributes']['managedDomain'] = s_system_data['deviceSpecificAttributes']['discoveredDomains'][0]
    for pool in s_system_data['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == s_system_data['deviceSpecificAttributes']['managedDomain']:
            pool_to_manage = pool
            s_system_data['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            pprint(pool_to_manage)
            break
    s_system_data['deviceSpecificAttributes']['managedPools'] = [pool_to_manage]
    s_system.update(s_system_data)
    print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
          s_system.data['deviceSpecificAttributes']['managedDomain']))
    storage_system_added = True

    print("   Added storage system '{}' at uri: {}".format(
        s_system.data['name'], s_system.data['uri']))

# Find and add unmanaged storage pool for management
# Create and delete operations supports only with API version 300 and below.
if oneview_client.api_version <= 300:
    pool_name = ''
    storage_pool_add = None

    print("Find and add unmanaged storage pool for management")
    for pool in s_system.data['unmanagedPools']:
        if pool['domain'] == s_system.data['managedDomain']:
            pool_name = pool['name']
            break

    if pool_name:
        print("   Found pool '{}'".format(pool_name))
        options = {
            "storageSystemUri": s_system.data['uri'],
            "poolName": pool_name
        }
        storage_pool_add = storage_pools.add(options)
        print("   Successfully added pool")
    else:
        print("   No available unmanaged storage pools to add")

    # Remove storage pool
    if storage_pool_add:
        print("Remove recently added storage pool")
        storage_pool_add.remove()
        print("   Done.")

# Get all the reachable storage pools filtered by scope uris.
print("Get all reachable storage pools filtered by scopes")
reachable_storage_pools = storage_pools.get_reachable_storage_pools(scope_uris=scope_uris)
print(reachable_storage_pools)

# Get all reachable storage pools by passing a set of storage pools uris
# to exclude those storage pools from scope validation checks.
print("Get all reachable storage pools by passing a set of storage pool uris to exclude from scope validation.")
reachable_storage_pools = storage_pools.get_reachable_storage_pools(scope_exclusions=storage_pool_uris)
print(reachable_storage_pools)

# Get all managed storage pools
print("Get all managed storage pools")
storage_pools_all = storage_pools.get_all()
for pool in storage_pools_all:
    print("   '{}' at uri: '{}'".format(pool['name'], pool['uri']))

# Get maximum of 5 storage pools sorted by freeCapacity in descending order.
print(
    "Get maximum of 5 storage pools  sorted by freeCapacity in descending order.")
storage_pools_filtered = storage_pools.get_all(
    0, 5, sort='freeCapacity:desc')
for pool in storage_pools_filtered:
    print("   '{}' at uri: '{}'".format(
        pool['name'], pool['uri']))

if storage_pools_all and storage_pools_all[0]:
    # Get storage pool by id and update it
    storage_pool = storage_pools.get_by_uri(storage_pools_all[0]['uri'])
    try:
        print('Update storage pool description with new description "new description"')
        s_pool_data = storage_pool.data.copy()
        s_pool_data['description'] = "new description"
        storage_pool.update(s_pool_data)
        print('Updated storage pool description')

    except HPOneViewException as e:
        print(e.msg)

# Remove storage system, if it was added
if storage_system_added:
    print("Remove recently added storage system")
    s_system.remove()
    print("   Done.")
