# -*- coding: utf-8 -*-
###
# (C) Copyright [2022] Hewlett Packard Enterprise Development LP
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

variant = 'DL'
options = {
    "hostname": config['server_hostname'],
    "username": config['server_username'],
    "password": config['server_password'],
    "force": False
}

oneview_client = OneViewClient(config)

rack_managers = oneview_client.rack_managers

# Get all rack managers
rackmanagers = []
print("Get all rack managers")
rack_managers_all = rack_managers.get_all()
# pprint(rack_managers_all)
for rm in rack_managers_all:
    print('%s' % rm['name'])
    rackmanagers.append(rm['name'])

# Adds a rack manager
# This is only supported on appliance which support managers
if variant != 'Synergy':
    added_rack_manager = rack_managers.add(options)
    print("Added rack manager '%s'.\n  uri = '%s'" % (added_rack_manager.data['name'], added_rack_manager.data['uri']))

# Get list of chassis from all rack managers
print("Get list of chassis from all rack managers")
chassis_all = rack_managers.get_all_chassis()
for ch in chassis_all['members']:
    pprint("Name:{} , ChassisType:{}".format(ch['name'], ch['chassisType']))

# Get list of manager resources from all rack managers
print("Get list of manager resources from all rack managers")
managers_all = rack_managers.get_all_managers()
for mn in managers_all['members']:
    pprint("Name:{} , ManagerType:{}".format(mn['name'], mn['managerType']))

# Get collection of partition resources from all rack managers
print("Get collection of partition resources from all rack managers")
partition_all = rack_managers.get_all_partitions()
for pn in partition_all['members']:
    pprint("Name:{} , partitionNum:{}".format(pn['name'], pn['partitionNum']))


# Get recently added rack manager resource
if rackmanagers:
    rackmanager = rack_managers.get_by_name(rackmanagers[0])
    pprint(rackmanager.data)

# Get all chassis associated with recently added rack manager
print("Get all chassis associated with recently added rack manager")
if rackmanager:
    associated_chassis = rackmanager.get_associated_chassis()
    pprint(associated_chassis)

# Retrieves a specific chassis that is part of the rack manager.
print("Retrieves a specific chassis that is part of the rack manager")
if associated_chassis:
    chassis_uri = associated_chassis['members'][0]['uri']
    pprint(rack_managers.get_a_specific_resource(chassis_uri))

# Get the environmental configuration of a rack manager
print("Get the environmental configuration of a rack manager")
if rackmanager:
    env_conf = rackmanager.get_environmental_configuration()
    pprint(env_conf)

# Get all chassis associated with recently added rack manager
print("Get all managers associated with recently added rack manager")
if rackmanager:
    associated_manager = rackmanager.get_associated_managers()
    pprint(associated_manager)

# Retrieves a specific manager that is part of the rack manager.
print("Retrieves a specific chassis that is part of the rack manager")
if associated_manager:
    manager_uri = associated_manager['members'][0]['uri']
    pprint(rack_managers.get_a_specific_resource(manager_uri))

# Get all chassis associated with recently added rack manager
print("Get all partitions associated with recently added rack manager")
if rackmanager:
    associated_partitions = rackmanager.get_associated_partitions()
    pprint(associated_partitions)

# Retrieves a specific partition that is part of the rack manager.
print("Retrieves a specific chassis that is part of the rack manager")
if associated_partitions:
    partition_uri = associated_partitions['members'][0]['uri']
    pprint(rack_managers.get_a_specific_resource(partition_uri))

# Get the environmental configuration of a rack manager
print("Get the remote support settings of a rack manager")
if rackmanager:
    remote_conf = rackmanager.get_remote_support_settings()
    pprint(remote_conf)

# Refreshes a rack manager
print("Refreshes a rack manager")
if rackmanagers:
    rm_name = rackmanagers[0]
    rm_to_refresh = rack_managers.get_by_name(rm_name)
    rm_to_refresh.patch('RefreshRackManagerOp', '', '')
    print("Succesfully refreshed rack manager.")

# remove a recently added rack manager
print("Remove a recently added rack manager")
if rackmanagers and variant != 'Synergy':
    rm_name = rackmanagers[0]
    rm_to_remove = rack_managers.get_by_name(rm_name)
    rm_to_remove.remove()
    print("Succesfully removed rack manager")
