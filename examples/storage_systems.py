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
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
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


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

options = {
    "hostname": config['storage_system_hostname'],
    "username": config['storage_system_username'],
    "password": config['storage_system_password'],
    "family": config['storage_system_family']
}

oneview_client = OneViewClient(config)
storage_systems = oneview_client.storage_systems

# Get all managed storage systems
print("\nGet all managed storage systems")
storage_systems_all = storage_systems.get_all()
for ss in storage_systems_all:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))

# Get maximum of 5 storage systems which belong to family of type 'StoreServ',
# sorted by freeCapacity in descending order.
print(
    "Get maximum of 5 storage systems which belong to family of type StoreServ, sorted by freeCapacity in "
    "descending order.")
filter = 'family=StoreServ'
storage_systems_filtered = storage_systems.get_all(
    0, 5, filter="\"'family'='StoreServ'\"", sort='freeCapacity:desc')
for ss in storage_systems_filtered:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))
if not storage_systems_filtered:
    print("   No storage systems matching parameters")

# Get the list of supported host types
print("\nGet supported host types")
support_host_types = storage_systems.get_host_types()
pprint(support_host_types)

# Add and update storage system for management
try:
    storage_system = storage_systems.add(options)
    print("\nAdded storage system '%s'.\n   uri = '%s'" %
          (storage_system.data['name'], storage_system.data['uri']))
except HPOneViewException as e:
    storage_system = storage_systems.get_by_hostname(options['hostname'])
    if storage_system:
        print("\nStorage system '%s' was already added.\n   uri = '%s'" %
              (storage_system.data['name'], storage_system.data['uri']))
    else:
        print(e.msg)

# Adds managed domains and managed pools to StoreServ storage systems
# This is a one-time only action, after this you cannot change the managed values
storage_sys_data = storage_system.data.copy()
if not storage_sys_data['deviceSpecificAttributes']['managedDomain']:
    storage_sys_data['deviceSpecificAttributes']['managedDomain'] = storage_sys_data[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    for pool in storage_sys_data['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == storage_sys_data['deviceSpecificAttributes']['managedDomain']:
            pool_to_manage = pool
            storage_sys_data['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            pprint(pool_to_manage)
            break
    storage_sys_data['deviceSpecificAttributes']['managedPools'] = [pool_to_manage]
    storage_system.update(storage_sys_data)
    print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
          storage_system.data['deviceSpecificAttributes']['managedDomain']))

# Get a list of storage pools
print("\nGet a list of storage pools managed by storage system")
storage_pools = storage_system.get_storage_pools()
pprint(storage_pools)

print("\nGet all reachable storage ports which are managed by the storage system")
reachable_ports = storage_system.get_reachable_ports()
pprint(reachable_ports)

print("\nGet templates related to a storage system")
templates = storage_system.get_templates()
pprint(templates)

# Remove storage system
print("\nRemove storage system")
storage_system.remove()
print("   Done.")
