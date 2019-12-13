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
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

config = {
    "ip": "10.30.9.143",
    "credentials": {
        "userName": "administrator",
        "password": "sijeadmin"
    },
    'api_version': 1200,
    'storage_system_hostname': '172.18.11.11',
    'storage_system_username': 'dcs',
    'storage_system_password': 'dcs',
    'storage_system_family': 'StoreServ'
}


scope_uris = '/rest/scopes/754e0dce-3cbd-4188-8923-edf86f068bf7'
storage_pool_uris = ['/rest/storage-pools/5F9CA89B-C632-4F09-BC55-A8AA00DA5C4A']

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
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
        "ip_hostname": config['storage_system_hostname'],
        "username": config['storage_system_username'],
        "password": config['storage_system_password']
    }
    s_system = storage_systems.add(options)
    s_system_data = s_system.data
    s_system_data['managedDomain'] = s_system.data['unmanagedDomains'][0]
    s_systems.update(s_system_data)
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

# Get storage pool by id and update it
try:
    print('Update storage pool description with new description "new description"')
    s_system_data = s_system.data.copy()
    s_system_data['description'] = "new description"
    s_system.update(s_system_data)
    print('Updated storage pool description')

except HPOneViewException as e:
    print(e.msg)

# Remove storage system, if it was added
if storage_system_added:
    print("Remove recently added storage system")
    s_system.remove()
    print("   Done.")
