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

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

OPTIONS = {
    "name": "172.18.13.11",
    "displayName": "vcenter",
    "hypervisorType": "Vmware",
    "username": "dcs",
    "password": "dcs",
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
HYPERVISOR_MANAGERS = oneview_client.hypervisor_managers

# Find recently created hypervisor manager by name
print("\nGet Hypervisor Manager by name")
HYPERVISOR_MANAGER = HYPERVISOR_MANAGERS.get_by_name(OPTIONS['name'])

if HYPERVISOR_MANAGER:
   
	 print("\nFound hypervisor-manager by name: {}.\n  uri = {}".format(HYPERVISOR_MANAGER.\
            data['name'], HYPERVISOR_MANAGER.data['uri']))
else:
    # Create a HypervisorManager with the OPTIONS provided
    HYPERVISOR_MANAGER =
	 HYPERVISOR_MANAGERS.create(data=OPTIONS)
    print("\nCreated a hypervisor-manager with name: {}.\n  uri = {}".format(HYPERVISOR_MANAGER.\
            data['name'], HYPERVISOR_MANAGER.data['uri']))

# Get all, with defaults
print("\nGet all hypervisor managers")
HYP_MANAGERS_ALL = HYPERVISOR_MANAGERS.get_all()
for hyp in HYP_MANAGERS_ALL:
    print('  - {}'.format(hyp['name']))

# Get the first 10 records
print("\nGet the first ten hypervisor managers")
HYP_MGRS_TOP_TEN = HYPERVISOR_MANAGERS.get_all(0, 10)
for hyp in HYP_MGRS_TOP_TEN:
    print('  - {}'.format(hyp['name']))

# Filter by hypervisor type
print("\nGet all hypervisor managers filtering by hypervisor type")
HYP_MGRS_FILTERED = HYPERVISOR_MANAGERS.get_all(filter="\"'hypervisorType'='Vmware'\"")
for hyp in HYP_MGRS_FILTERED:
    print("Hypervisor with type 'Vmware'  - {}".format(hyp['name']))

# Get all sorting by name descending
print("\nGet all hypervisor managers sorting by name")
HYP_MGRS_SORTED = HYPERVISOR_MANAGERS.get_all(sort='name:descending')
pprint(HYP_MGRS_SORTED)

# Get by uri
print("\nGet a hypervisor managers by uri")
HYP_MGRS_BY_URI = HYPERVISOR_MANAGERS.get_by_uri(HYPERVISOR_MANAGER.data['uri'])
pprint(HYP_MGRS_BY_URI.data)

# Update display name of recently created hypervisor manager
DATA_TO_UPDATE = {'displayName': 'Updated
	 vcenter'}
HYPERVISOR_MANAGER.update(data=DATA_TO_UPDATE)
print("\nUpdated hypervisor manager {} successfully.\n  uri = {}".format(HYPERVISOR_MANAGER.\
        data['name'], HYPERVISOR_MANAGER.data['uri']))
print("  with attribute 'displayName': {}".format(HYPERVISOR_MANAGER.data['displayName']))

# Delete the created hypervisor manager
HYPERVISOR_MANAGER.delete()
print("\nSuccessfully deleted hypervisor manager")

# Create a HypervisorManager for automation
HYPERVISOR_MANAGER = HYPERVISOR_MANAGERS.create(data=OPTIONS)
print("\nCreated a hypervisor-manager with name: {}.\n  uri = {}".format(HYPERVISOR_MANAGER.\
        data['name'], HYPERVISOR_MANAGER.data['uri']))
