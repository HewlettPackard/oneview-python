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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

hypervisor_manager_information = {
    "type": "HypervisorManagerV2",
    "name": "172.18.13.11",
    "displayName": "vcenter",
    "hypervisorType": "Vmware",
    "username": "dcs",
    "password": "dcs",
    "initialScopeUris": []
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient.from_json_file("/home/venkatesh/Documents/oneview-python/examples/config.json")

# Add a hypervisor manager
hypervisor_manager_added = oneview_client.hypervisor_managers.add(hypervisor_manager_information)
print('Added hypervisor manager "{name}" successfully\n'.format(**hypervisor_manager_added))

# Retrieve hypervisor manager by URI
hypervisor_manager = oneview_client.hypervisor_managers.get(hypervisor_manager_added['uri'])
print('Get hypervisor manager by URI "{uri}", retrieved "{name}" successfully\n'.format(**hypervisor_manager))

# Retrieve hypervisor manager by FILTER
hypervisor_manager_list = oneview_client.hypervisor_managers.get_by('hypervisorType', 'Vmware')
print('Get hypervisor manager by FILTER "{hypervisorType}", retrieved "{name}" successfully\n'.format(**hypervisor_manager_list[0]))

# Update the hypervisor manager
hypervisor_manager['displayName'] = "New hypervisor"
hypervisor_manager = oneview_client.hypervisor_managers.update(hypervisor_manager)
print('Hypervisor manager "{displayName}" updated successfully\n'.format(**hypervisor_manager))

# Retrieve hypervisor manager by NAME
hypervisor_manager = oneview_client.hypervisor_managers.get_by_name(hypervisor_manager['name'])
print('Get hypervisor manager by NAME "{name}", retrieved "{uri}" successfully\n'.format(**hypervisor_manager))

# Update the hypervisor manager forcefully
hypervisor_manager['displayName'] = "Update hypervisor force"
hypervisor_manager = oneview_client.hypervisor_managers.update(hypervisor_manager, force=True)
print('Hypervisor manager "{displayName}" updated forcefully\n'.format(**hypervisor_manager))

# Get all hypervisor managers
print("Get all hypervisor managers:")
hypervisor_manager_all = oneview_client.hypervisor_managers.get_all()
for hyp_mgr in hypervisor_manager_all:
    print(" - " + hyp_mgr['name'])

# Remove added hypervisor manager
oneview_client.hypervisor_managers.delete(hypervisor_manager)
print('Successfully removed the hypervisor manager "{name}"\n'.format(**hypervisor_manager))

# Add another hypervisor manager and remove forcefully
hypervisor_manager_added = oneview_client.hypervisor_managers.add(hypervisor_manager_information)
oneview_client.hypervisor_managers.delete(hypervisor_manager_added, force=True)
print("Successfully added and removed the hypervisor manager forcefully")

