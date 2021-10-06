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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

OPTIONS = {
    "type": "Destination",
    "destinationAddress": "1.1.1.1",
    "port": 162,
    "existingDestinations": ['2.3.2.3']
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
appliance_device_SNMP_V3_TRAP_destinations = oneview_client.appliance_device_SNMP_V3_TRAP_destinations
appliance_device_snmp_v3_users = oneview_client.appliance_device_snmp_v3_users

# Get all snmpv3 users
# snmp v3 user must be there to create this
SNMP_USERS = appliance_device_snmp_v3_users.get_all()
if SNMP_USERS:
    SNMP_USERID = SNMP_USERS[0]['id']
    # Adding userId to snmpv3 users payload
    OPTIONS['userId'] = SNMP_USERID
    # Add appliance device SNMP v3 Trap Destination
    SNMP_V3_TRAP = appliance_device_SNMP_V3_TRAP_destinations.create(OPTIONS)
    print("\n## Created appliance SNMPv3 trap destination successfully!")
    pprint(SNMP_V3_TRAP.data)


# Lists the appliance device SNMP v3 Trap Destination
print("\n## Get list of appliance SNMPv3 trap destination")
SNMP_V3_TRAP_ALL = appliance_device_SNMP_V3_TRAP_destinations.get_all()
for snmp_trap in SNMP_V3_TRAP_ALL:
    print('  - {}: {}'.format(snmp_trap['destinationAddress'], snmp_trap['uri']))

# Get by name
print("\n## Find an SNMPv3 trap destination by name")
SNMP_V3_TRAP = appliance_device_SNMP_V3_TRAP_destinations.get_by_name(SNMP_V3_TRAP.data['destinationAddress'])
pprint(SNMP_V3_TRAP.data)

# Get by URI
print("\n## Find an SNMPv3 trap destination by URI")
SNMP_V3_TRAP = appliance_device_SNMP_V3_TRAP_destinations.get_by_uri(SNMP_V3_TRAP.data['uri'])
pprint(SNMP_V3_TRAP.data)

# Change appliance device SNMP v3 Trap Destination - Only Community String and Port can be changed
SNMPV3_DATA = {"port": 170}
SNMP_V3_TRAP = SNMP_V3_TRAP.update(SNMPV3_DATA)
print("\n## Update appliance SNMPv3 trap destination successfully!")
pprint(SNMP_V3_TRAP.data)

# Delete Created Entry
SNMP_V3_TRAP.delete(SNMP_V3_TRAP)
print("\n## Delete appliance SNMPv3 trap destination successfully!")
