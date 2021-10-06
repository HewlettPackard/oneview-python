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

from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException
from CONFIG_loader import try_load_from_file
from pprint import pprint

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient.from_json_file('CONFIG.json')
storage_systems = oneview_client.storage_systems
STORAGE_POOLs = oneview_client.STORAGE_POOLs
SCOPEs = oneview_client.SCOPEs

# Find or add storage system
print("Find or add storage system")
S_SYSTEMS = storage_systems.get_all()
if S_SYSTEMS:
    S_SYSTEM_DATA = S_SYSTEMS[0]
    S_SYSTEM = storage_systems.get_by_uri(S_SYSTEM_DATA["uri"])
    STORAGE_SYSTEM_ADDED = False
    print("Found storage system '{}' at uri: {}".format(
        S_SYSTEM.data['name'], S_SYSTEM.data['uri']))
else:
    OPTIONS = {
        "hostname": CONFIG['storage_system_hostname'],
        "username": CONFIG['storage_system_username'],
        "password": CONFIG['storage_system_password'],
        "family": CONFIG['storage_system_family']
    }
    S_SYSTEM = storage_systems.add(OPTIONS)
    S_SYSTEM_DATA = S_SYSTEM.data.copy()
    S_SYSTEM_DATA['deviceSpecificAttributes']['managedDomain'] = S_SYSTEM_DATA['deviceSpecificAttributes']['discoveredDomains'][0]
    for pool in S_SYSTEM_DATA['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == S_SYSTEM_DATA['deviceSpecificAttributes']['managedDomain']:
            pool_to_manage = pool
            S_SYSTEM_DATA['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            pprint(pool_to_manage)
            break
    S_SYSTEM_DATA['deviceSpecificAttributes']['managedPools'] = [pool_to_manage]
    S_SYSTEM.update(S_SYSTEM_DATA)
    print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
          S_SYSTEM.data['deviceSpecificAttributes']['managedDomain']))
    STORAGE_SYSTEM_ADDED = True

    print("   Added storage system '{}' at uri: {}".format(
        S_SYSTEM.data['name'], S_SYSTEM.data['uri']))

# Find and add unmanaged storage pool for management
# Create and delete operations supports only with API version 300 and below.
if oneview_client.api_version <= 300:
    POOL_NAME = ''
    STORAGE_POOL_ADD = None

    print("Find and add unmanaged storage pool for management")
    for pool in S_SYSTEM.data['unmanagedPools']:
        if pool['domain'] == S_SYSTEM.data['managedDomain']:
            POOL_NAME = pool['name']
            break

    if POOL_NAME:
        print("   Found pool '{}'".format(POOL_NAME))
        OPTIONS = {
            "storageSystemUri": S_SYSTEM.data['uri'],
            "poolName": POOL_NAME
        }
        STORAGE_POOL_ADD = STORAGE_POOLs.add(OPTIONS)
        print("   Successfully added pool")
    else:
        print("   No available unmanaged storage pools to add")

    # Remove storage pool
    if STORAGE_POOL_ADD:
        print("Remove recently added storage pool")
        STORAGE_POOL_ADD.remove()
        print("   Done.")

# Create a SCOPE
print("\n## Create the SCOPE")
OPTIONS = {
    "name": "SampleScope",
    "description": "Sample Scope description"
}
SCOPE = SCOPEs.get_by_name(OPTIONS['name'])
if not SCOPE:
    SCOPE = SCOPEs.create(OPTIONS)
pprint(SCOPE.data)

# Get all the reachable storage pools filtered by SCOPE uris.
print("Get all reachable storage pools filtered by SCOPEs")
REACHABLE_STORAGE_POOLS = STORAGE_POOLs.get_REACHABLE_STORAGE_POOLS(SCOPE_uris=SCOPE.data['uri'])
print(REACHABLE_STORAGE_POOLS)

# Get all managed storage pools
print("Get all managed storage pools")
STORAGE_POOLS_ALL = STORAGE_POOLs.get_all()
for pool in STORAGE_POOLS_ALL:
    print("   '{}' at uri: '{}'".format(pool['name'], pool['uri']))

# Get all reachable storage pools by passing a set of storage pools uris
# to exclude those storage pools from SCOPE validation checks.
STORAGE_POOLS_ALL = STORAGE_POOLs.get_all()
STORAGE_POOL_URIS = []
STORAGE_POOL_URIS.append(STORAGE_POOLS_ALL[0]['uri'])
print("Get all reachable storage pools by passing a set of storage pool uris to exclude from SCOPE
	 validation.")
REACHABLE_STORAGE_POOLS = STORAGE_POOLs.get_REACHABLE_STORAGE_POOLS(SCOPE_exclusions=STORAGE_POOL_URIS)
print(REACHABLE_STORAGE_POOLS)

# Get maximum of 5 storage pools sorted by freeCapacity in descending order.
print(
    "Get maximum of 5 storage pools  sorted by freeCapacity in descending order.")
STORAGE_POOLS_FILTERED = STORAGE_POOLs.get_all(
    0, 5, sort='freeCapacity:desc')
for pool in STORAGE_POOLS_FILTERED:
    print("   '{}' at uri: '{}'".format(
        pool['name'], pool['uri']))

if STORAGE_POOLS_ALL and STORAGE_POOLS_ALL[0]:
    # Get storage pool by id and update it
    STORAGE_POOL = STORAGE_POOLs.get_by_uri(STORAGE_POOLS_ALL[0]['uri'])
    try:
        print('Update storage pool description with new description "new description"')
        S_POOL_DATA = STORAGE_POOL.data.copy()
        S_POOL_DATA['description'] = "new description"
        STORAGE_POOL.update(S_POOL_DATA)
        print('Updated storage pool description')

    except HPEOneViewException as e:
        print(e.msg)

# comment the below example to support automation dependency
# Remove storage system, if it was added
# if STORAGE_SYSTEM_ADDED:
#     print("Remove recently added storage system")
#     S_SYSTEM.remove()
#     print("Done.")
