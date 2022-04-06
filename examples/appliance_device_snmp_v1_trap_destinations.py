# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "destination": "1.1.1.2",
    "communityString": "testOne",
    "port": 162
}

destination_ip = '2.2.2.2'

# Try load config from a file (if there is a config file)
config = try_load_from_file()
oneview_client = OneViewClient(config)
appliance_device_snmp_v1_trap_destinations = oneview_client.appliance_device_snmp_v1_trap_destinations

# Lists the appliance device SNMP v1 Trap Destination
print("\n Get list of appliance SNMP v1 trap destination")
snmp_v1_trap_all = appliance_device_snmp_v1_trap_destinations.get_all()
for snmp_trap in snmp_v1_trap_all:
    print('  - {}: {}'.format(snmp_trap['destination'], snmp_trap['uri']))

# Add appliance device SNMP v1 Trap Destination
snmp_v1_trap = appliance_device_snmp_v1_trap_destinations.create(options)
print("\n Created appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap.data)

# Get by name
print("\n## Find an SNMPv1 trap destination by name")
snmp_v1_trap = appliance_device_snmp_v1_trap_destinations.get_by_name(snmp_v1_trap.data['destination'])
pprint(snmp_v1_trap.data)

# Add appliance device SNMP v1 Trap Destination with ID
trap_id = 9
options['destination'] = destination_ip
snmp_v1_trap_id = appliance_device_snmp_v1_trap_destinations.create(options, trap_id)
print("\n Created appliance SNMP v1 trap destination by id successfully!")
pprint(snmp_v1_trap_id.data)

# Get the appliance device SNMP v1 Trap Destination by id
print("\n Get appliance SNMP v1 trap destination by id")
snmp_v1_trap_by_id = appliance_device_snmp_v1_trap_destinations.get_by_id(1)
pprint(snmp_v1_trap_by_id.data)

# Lists the appliance device SNMP v1 Trap Destination by destination (unique)
print("\n## Get appliance SNMP v1 trap by destination..")
snmp_v1_traps = appliance_device_snmp_v1_trap_destinations.get_by('destination', options['destination'])
for snmp_trap in snmp_v1_traps:
    print(' - {} : {}'.format(snmp_trap['destination'], snmp_trap['communityString']))

# Get by URI
print("\n Find an SNMP v1 trap destination by URI")
snmp_v1_trap = appliance_device_snmp_v1_trap_destinations.get_by_uri(snmp_v1_trap.data['uri'])
pprint(snmp_v1_trap.data)

# Change appliance device SNMP v1 Trap Destination - Only Community String and Port can be changed
data = {'communityString': 'testTwo'}
snmp_v1_trap = snmp_v1_trap.update(data)
print("\n## Update appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap.data)

# Delete Created Entry
snmp_v1_trap.delete()
snmp_v1_trap_id.delete()
print("\n## Delete appliance SNMP v1 trap destination successfully!")
