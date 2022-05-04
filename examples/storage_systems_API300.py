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
import re
from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException
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

options = {
    "ip_hostname": config['storage_system_hostname'],
    "username": config['storage_system_username'],
    "password": config['storage_system_password']
}

oneview_client = OneViewClient(config)

# Add and update storage system for management
storage_system = oneview_client.storage_systems.add(options)
print("\nAdded storage system '%s'.\n   uri = '%s'" %
      (storage_system['name'], storage_system['uri']))
storage_system['managedDomain'] = storage_system['unmanagedDomains'][0]
storage_system = oneview_client.storage_systems.update(storage_system)
print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
    storage_system['managedDomain']))


# Add storage pool to be managed
try:
    print("\nAdd first storage pool from unmanaged storage pools to be managed")
    for pool in storage_system['unmanagedPools']:
        if pool['domain'] == storage_system['managedDomain']:
            pool_to_manage = pool
            break
    storage_system['managedPools'] = [{
        "type": pool_to_manage['type'],
        "domain": pool_to_manage['domain'],
        "name": pool_to_manage['name'],
        "deviceType": pool_to_manage['deviceType']
    }]
    storage_system = oneview_client.storage_systems.update(
        storage_system)
    print("\nManaged storage pool '{}' at uri: '{}'".format(storage_system[
          'managedPools'][0]['name'], storage_system['managedPools'][0]['uri']))
except HPEOneViewException as e:
    print(e.msg)

# Get all managed storage systems
print("\nGet all managed storage systems")
storage_systems_all = oneview_client.storage_systems.get_all()
for ss in storage_systems_all:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))

# Get maximum of 5 storage systems which belong to model of type 'HP_3PAR
# 7200', sorted by freeCapacity in descending order.
print(
    "Get maximum of 5 storage systems which belong to model of type 'HP_3PAR 7200,' sorted by freeCapacity in "
    "descending order.")
filter = 'model=HP_3PAR 7200'
storage_systems_filtered = oneview_client.storage_systems.get_all(
    0, 5, filter="\"'name'='ThreePAR7200-5718'\"", sort='freeCapacity:desc')
for ss in storage_systems_filtered:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))
if not storage_systems_filtered:
    print("   No storage systems matching parameters")

# Get the list of supported host types
print("\nGet supported host types")
support_host_types = oneview_client.storage_systems.get_host_types()
pprint(support_host_types)

# Get a list of storage pools
print("\nGet a list of storage pools managed by storage system")
storage_pools = oneview_client.storage_systems.get_storage_pools(
    storage_system['uri'])
pprint(storage_pools)

# Get a specified storage system by id
try:
    storage_system_by_id = oneview_client.storage_systems.get('TXQ1010307')
    print("\nGot storage system by id 'TXQ1010307' at uri '{}'".format(
        storage_system_by_id['uri']))
except HPEOneViewException as e:
    print(e.msg)

# Add managed ports
ports_to_manage = []
for port in storage_system['unmanagedPorts']:
    if port['actualNetworkSanUri'] != "unknown":
        port_to_manage = {
            "type": port['type'],
            "name": port['name'],
            "portName": port['portName'],
            "portWwn": port['portWwn'],
            "expectedNetworkUri": port['actualNetworkSanUri'],
            "actualNetworkUri": port['actualNetworkUri'],
            "actualNetworkSanUri": port['actualNetworkUri'],
            "groupName": port['groupName'],
            "protocolType": port['protocolType'],
            "label": port['label']
        }
        ports_to_manage.append(port_to_manage)
storage_system['managedPorts'] = ports_to_manage
storage_system = oneview_client.storage_systems.update(storage_system)
print("\nSuccessfully added ports to be managed")

# Get managed ports for specified storage system
print("\nGet all managed ports for storage system at uri '{}'".format(
    storage_system['uri']))
managed_ports = oneview_client.storage_systems.get_managed_ports(
    storage_system['uri'])
for port in managed_ports['members']:
    print("   '{}' at uri: {}".format(port['name'], port['uri']))

# Get managed target port for specified storage system
print("\nGet managed port by uri")
managed_port_by_uri = oneview_client.storage_systems.get_managed_ports(
    storage_system['uri'], storage_system['managedPorts'][0]['uri'])
print("   '{}' at uri: {}".format(
    managed_port_by_uri['name'], managed_port_by_uri['uri']))

# Get managed target port for specified storage system by id
try:
    port_id = re.sub("/rest/storage-systems/TXQ1010307/managedPorts/",
                     '', storage_system['managedPorts'][0]['uri'])
    print("\nGet managed port by id: '{}'".format(port_id))
    managed_port_by_id = oneview_client.storage_systems.get_managed_ports(
        'TXQ1010307', port_id)
    print("   '{}' at uri: {}".format(
        managed_port_by_id['name'], managed_port_by_id['uri']))
except HPEOneViewException as e:
    print(e.msg)

# Remove storage system
print("\nRemove storage system")
oneview_client.storage_systems.remove(storage_system)
print("   Done.")
