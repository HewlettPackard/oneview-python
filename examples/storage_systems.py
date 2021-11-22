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

from pprint import pprint
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

OPTIONS = {
    "hostname": CONFIG['STORAGE_SYSTEM_hostname'],
    "username": CONFIG['STORAGE_SYSTEM_username'],
    "password": CONFIG['STORAGE_SYSTEM_password'],
    "family": CONFIG['STORAGE_SYSTEM_family']
}

oneview_client = OneViewClient(CONFIG)
STORAGE_SYSTEMs = oneview_client.STORAGE_SYSTEMs

# Get all managed storage systems
print("\nGet all managed storage systems")
STORAGE_SYSTEMS_ALL = STORAGE_SYSTEMs.get_all()
for ss in STORAGE_SYSTEMS_ALL:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))

# Get maximum of 5 storage systems which belong to family of type 'StoreServ',
# sorted by freeCapacity in descending order.
print("Get maximum of 5 storage systems which belong to family of type StoreServ, sorted by
	 freeCapacity in descending order.")
FILTER = 'family=StoreServ'
STORAGE_SYSTEMs_FILTERed = STORAGE_SYSTEMs.get_all(
    0, 5, FILTER="\"'family'='StoreServ'\"", sort='freeCapacity:desc')
for ss in STORAGE_SYSTEMs_FILTERed:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))
if not STORAGE_SYSTEMs_FILTERed:
    print("   No storage systems matching parameters")

# Get the list of supported host types
print("\nGet supported host types")
SUPPORT_HOST_TYPES = STORAGE_SYSTEMs.get_host_types()
pprint(SUPPORT_HOST_TYPES)

# Add and update storage system for management

STORAGE_SYSTEM = STORAGE_SYSTEMs.get_by_hostname(OPTIONS['hostname'])
if not STORAGE_SYSTEM:
    print("Create Storage System")
    STORAGE_SYSTEM = STORAGE_SYSTEMs.add(OPTIONS)
    print("\nAdded storage system {}.\n   uri = {}" .format(
          str(STORAGE_SYSTEM.data['name']), str(STORAGE_SYSTEM.data['uri'])))
else:
    print("\nStorage system {} was already added.\n   uri = {}" .format(
          str(STORAGE_SYSTEM.data['name']), str(STORAGE_SYSTEM.data['uri'])))
print(STORAGE_SYSTEM.data)

# Adds managed domains and managed pools to StoreServ storage systems
# This is a one-time only action, after this you cannot change the managed values
STORAGE_SYS_DATA = STORAGE_SYSTEM.data.copy()
if not STORAGE_SYS_DATA['deviceSpecificAttributes']['managedDomain']:
    STORAGE_SYS_DATA['deviceSpecificAttributes']['managedDomain'] = STORAGE_SYS_DATA[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    for pool in STORAGE_SYS_DATA['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == STORAGE_SYS_DATA['deviceSpecificAttributes']['managedDomain']:
            pool_to_manage = pool
            STORAGE_SYS_DATA['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            pprint(pool_to_manage)
            break
    STORAGE_SYS_DATA['deviceSpecificAttributes']['managedPools'] = [pool_to_manage]
    STORAGE_SYSTEM.update(STORAGE_SYS_DATA)
    print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
          STORAGE_SYSTEM.data['deviceSpecificAttributes']['managedDomain']))

# Get a list of storage pools
print("\nGet a list of storage pools managed by storage system")
if STORAGE_SYSTEM:
    STORAGE_POOLS = STORAGE_SYSTEM.get_STORAGE_POOLS()
    pprint(STORAGE_POOLS)

print("\nGet all reachable storage ports which are managed by the storage system")
if STORAGE_SYSTEM:
    REACHABLE_PORTS = STORAGE_SYSTEM.get_REACHABLE_PORTS()
    pprint(REACHABLE_PORTS)

print("\nGet TEMPLATES related to a storage system")
if STORAGE_SYSTEM:
    TEMPLATES = STORAGE_SYSTEM.get_TEMPLATES()
    pprint(TEMPLATES)

# Remove storage system
print("\nRemove storage system")
if STORAGE_SYSTEM:
    STORAGE_SYSTEM.remove()
    print("   Done.")

# Create storage system for automation
# Add and update storage system for management

STORAGE_SYSTEM = STORAGE_SYSTEMs.get_by_hostname(OPTIONS['hostname'])
if not STORAGE_SYSTEM:
    print("Create Storage System")
    STORAGE_SYSTEM = STORAGE_SYSTEMs.add(OPTIONS)
    print("\nAdded storage system {}.\n   uri = {}" .format(
          str(STORAGE_SYSTEM.data['name']), str(STORAGE_SYSTEM.data['uri'])))
else:
    print("\nStorage system {} was already added.\n   uri = {}" .format(
          str(STORAGE_SYSTEM.data['name']), str(STORAGE_SYSTEM.data['uri'])))
print(STORAGE_SYSTEM.data)

# Adds managed domains and managed pools to StoreServ storage systems
STORAGE_SYS_DATA = STORAGE_SYSTEM.data.copy()
if not STORAGE_SYS_DATA['deviceSpecificAttributes']['managedDomain']:
    STORAGE_SYS_DATA['deviceSpecificAttributes']['managedDomain'] = STORAGE_SYS_DATA[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    for pool in STORAGE_SYS_DATA['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == STORAGE_SYS_DATA['deviceSpecificAttributes']['managedDomain']:
            pool_to_manage = pool
            STORAGE_SYS_DATA['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            pprint(pool_to_manage)
            break
    STORAGE_SYS_DATA['deviceSpecificAttributes']['managedPools'] = [pool_to_manage]
    STORAGE_SYSTEM.update(STORAGE_SYS_DATA)
    print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
          STORAGE_SYSTEM.data['deviceSpecificAttributes']['managedDomain']))
