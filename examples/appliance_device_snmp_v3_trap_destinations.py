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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "type": "Destination",
    "destinationAddress": "1.1.1.1",
    "port": 162,
    "existingDestinations": ['2.3.2.3']
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
appliance_device_snmp_v3_trap_destinations = oneview_client.appliance_device_snmp_v3_trap_destinations
appliance_device_snmp_v3_users = oneview_client.appliance_device_snmp_v3_users

# Get all snmpv3 users
# snmp v3 user must be there to create this
snmp_users = appliance_device_snmp_v3_users.get_all()
if snmp_users:
    snmp_userId = snmp_users[0]['id']
    # Adding userId to snmpv3 users payload
    options['userId'] = snmp_userId
    
    # Add appliance device SNMP v3 Trap Destination
    snmp_v3_trap = appliance_device_snmp_v3_trap_destinations.create(options)
    print("\n## Created appliance SNMPv3 trap destination successfully!")
    pprint(snmp_v3_trap.data)


# Lists the appliance device SNMP v3 Trap Destination
print("\n## Get list of appliance SNMPv3 trap destination")
snmp_v3_trap_all = appliance_device_snmp_v3_trap_destinations.get_all()
for snmp_trap in snmp_v3_trap_all:
    print('  - {}: {}'.format(snmp_trap['destinationAddress'], snmp_trap['uri']))

# Get by name
print("\n## Find an SNMPv3 trap destination by name")
snmp_v3_trap = appliance_device_snmp_v3_trap_destinations.get_by_name(snmp_v3_trap.data['destinationAddress'])
pprint(snmp_v3_trap.data)

# Get by URI
print("\n## Find an SNMPv3 trap destination by URI")
snmp_v3_trap = appliance_device_snmp_v3_trap_destinations.get_by_uri(snmp_v3_trap.data['uri'])
pprint(snmp_v3_trap.data)

# Change appliance device SNMP v3 Trap Destination - Only Community String and Port can be changed
snmpv3_data = {"port": 170}
snmp_v3_trap = snmp_v3_trap.update(snmpv3_data)
print("\n## Update appliance SNMPv3 trap destination successfully!")
pprint(snmp_v3_trap.data)

# Delete Created Entry
snmp_v3_trap.delete(snmp_v3_trap)
print("\n## Delete appliance SNMPv3 trap destination successfully!")
