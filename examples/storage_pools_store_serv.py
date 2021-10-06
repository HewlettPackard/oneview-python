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

from hpeOneView.oneview_client import OneViewClient
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Find or add storage system
print("Find or add storage system")
S_SYSTEMS = oneview_client.storage_systems.get_all()
STORAGE_SYSTEM_ADDED = True
if S_SYSTEMS:
    S_SYSTEM = S_SYSTEMS[0]
    if S_SYSTEM['deviceSpecificAttributes']['managedPools']:
        STORAGE_SYSTEM_ADDED = False
        print("   Found storage system '{}' at uri: {}".format(
            S_SYSTEM['name'], S_SYSTEM['uri']))
    elif S_SYSTEM['hostname'] == CONFIG['storage_system_hostname']:
        oneview_client.storage_systems.remove(S_SYSTEM, force=True)
        print("   Removing Storage System since it has no storage pools managed")


if STORAGE_SYSTEM_ADDED:
    OPTIONS = {
        "hostname": CONFIG['storage_system_hostname'],
        "username": CONFIG['storage_system_username'],
        "password": CONFIG['storage_system_password'],
        "family": CONFIG['storage_system_family']
    }
    S_SYSTEM = oneview_client.storage_systems.add(OPTIONS)
    print("   Added storage system '{}' at uri: {}".format(
        S_SYSTEM['name'], S_SYSTEM['uri']))
    S_SYSTEM['deviceSpecificAttributes']['managedDomain'] = S_SYSTEM[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    print("   Discovering Storage Pools...")
    S_SYSTEM['deviceSpecificAttributes']['managedPools'] = []
    for pool in S_SYSTEM['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == S_SYSTEM['deviceSpecificAttributes']['managedDomain']:
            S_SYSTEM['deviceSpecificAttributes']['managedPools'].append(pool)
            S_SYSTEM['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            print("        Discovered '{}' storage pool").format(pool['name'])
    S_SYSTEM = oneview_client.storage_systems.update(S_SYSTEM)
    print("   Added the discovered pools for management")
    STORAGE_SYSTEM_ADDED = True
    print


# Get all managed storage pools
print("\nGet all storage pools")
STORAGE_POOLS_ALL = oneview_client.storage_pools.get_all()
for pool in STORAGE_POOLS_ALL:
    print("   '{}' state is {}".format(pool['name'], pool['state']))

# Get all managed storage pools
print("\nGet all managed storage pools")
STORAGE_POOLS_ALL = oneview_client.storage_pools.get_all(filter='isManaged=True')
for pool in STORAGE_POOLS_ALL:
    print("   '{}' state is {}".format(pool['name'], pool['state']))

# Remove first storage pool
if STORAGE_POOLS_ALL:
    REMOVE_POOL = STORAGE_POOLS_ALL[0]
    print("\nRemove '{}' storage pool from management").format(REMOVE_POOL['name'])
    REMOVE_POOL['isManaged'] = False
    oneview_client.storage_pools.update(REMOVE_POOL)
    print("   Done.")

# Get all managed storage pools
print("\nGet all unmanaged storage pools")
STORAGE_POOLS_ALL = oneview_client.storage_pools.get_all(filter='isManaged=False')
for pool in STORAGE_POOLS_ALL:
    print("   '{}' state is {}".format(pool['name'], pool['state']))
