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

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

options = {
    "name": "172.18.13.11",
    "displayName": "vcenter",
    "hypervisorType": "Vmware",
    "username": "dcs",
    "password": "dcs",
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
hypervisor_managers = oneview_client.hypervisor_managers

# Find recently created hypervisor manager by name
print("\nGet Hypervisor Manager by name")
hypervisor_manager = hypervisor_managers.get_by_name(options['name'])

if hypervisor_manager:
    print("\nFound hypervisor-manager by name: {}.\n  uri = {}".format(hypervisor_manager.data['name'], hypervisor_manager.data['uri']))
else:
    # Create a HypervisorManager with the options provided
    hypervisor_manager = hypervisor_managers.create(data=options)
    print("\nCreated a hypervisor-manager with name: {}.\n  uri = {}".format(hypervisor_manager.data['name'], hypervisor_manager.data['uri']))

# Get all, with defaults
print("\nGet all hypervisor managers")
hyp_managers_all = hypervisor_managers.get_all()
for hyp in hyp_managers_all:
    print('  - {}'.format(hyp['name']))

# Get the first 10 records
print("\nGet the first ten hypervisor managers")
hyp_mgrs_top_ten = hypervisor_managers.get_all(0, 10)
for hyp in hyp_mgrs_top_ten:
    print('  - {}'.format(hyp['name']))

# Filter by hypervisor type
print("\nGet all hypervisor managers filtering by hypervisor type")
hyp_mgrs_filtered = hypervisor_managers.get_all(filter="\"'hypervisorType'='Vmware'\"")
for hyp in hyp_mgrs_filtered:
    print("Hypervisor with type 'Vmware'  - {}".format(hyp['name']))

# Get all sorting by name descending
print("\nGet all hypervisor managers sorting by name")
hyp_mgrs_sorted = hypervisor_managers.get_all(sort='name:descending')
pprint(hyp_mgrs_sorted)

# Get by uri
print("\nGet a hypervisor managers by uri")
hyp_mgrs_by_uri = hypervisor_managers.get_by_uri(hypervisor_manager.data['uri'])
pprint(hyp_mgrs_by_uri.data)

# Update display name of recently created hypervisor manager
data_to_update = {'displayName': 'Updated vcenter'}
hypervisor_manager.update(data=data_to_update)
print("\nUpdated hypervisor manager {} successfully.\n  uri = {}".format(hypervisor_manager.data['name'], hypervisor_manager.data['uri']))
print("  with attribute 'displayName': {}".format(hypervisor_manager.data['displayName']))

# Delete the created hypervisor manager
hypervisor_manager.delete()
print("\nSuccessfully deleted hypervisor manager")
