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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Find or add storage system
print("Find or add storage system")
s_systems = oneview_client.storage_systems.get_all()
storage_system_added = True
if s_systems:
    s_system = s_systems[0]
    if s_system['deviceSpecificAttributes']['managedPools']:
        storage_system_added = False
        print("   Found storage system '{}' at uri: {}".format(
            s_system['name'], s_system['uri']))
    elif s_system['hostname'] == config['storage_system_hostname']:
        oneview_client.storage_systems.remove(s_system, force=True)
        print("   Removing Storage System since it has no storage pools managed")


if storage_system_added:
    options = {
        "hostname": config['storage_system_hostname'],
        "username": config['storage_system_username'],
        "password": config['storage_system_password'],
        "family": config['storage_system_family']
    }
    s_system = oneview_client.storage_systems.add(options)
    print("   Added storage system '{}' at uri: {}".format(
        s_system['name'], s_system['uri']))
    s_system['deviceSpecificAttributes']['managedDomain'] = s_system[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    print("   Discovering Storage Pools...")
    s_system['deviceSpecificAttributes']['managedPools'] = []
    for pool in s_system['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == s_system['deviceSpecificAttributes']['managedDomain']:
            s_system['deviceSpecificAttributes']['managedPools'].append(pool)
            s_system['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            print("        Discovered '{}' storage pool").format(pool['name'])
    s_system = oneview_client.storage_systems.update(s_system)
    print("   Added the discovered pools for management")
    storage_system_added = True
    print


# Get all managed storage pools
print("\nGet all storage pools")
storage_pools_all = oneview_client.storage_pools.get_all()
for pool in storage_pools_all:
    print("   '{}' state is {}".format(pool['name'], pool['state']))

# Get all managed storage pools
print("\nGet all managed storage pools")
storage_pools_all = oneview_client.storage_pools.get_all(filter='isManaged=True')
for pool in storage_pools_all:
    print("   '{}' state is {}".format(pool['name'], pool['state']))

# Remove first storage pool
if storage_pools_all:
    remove_pool = storage_pools_all[0]
    print("\nRemove '{}' storage pool from management").format(remove_pool['name'])
    remove_pool['isManaged'] = False
    oneview_client.storage_pools.update(remove_pool)
    print("   Done.")

# Get all managed storage pools
print("\nGet all unmanaged storage pools")
storage_pools_all = oneview_client.storage_pools.get_all(filter='isManaged=False')
for pool in storage_pools_all:
    print("   '{}' state is {}".format(pool['name'], pool['state']))
