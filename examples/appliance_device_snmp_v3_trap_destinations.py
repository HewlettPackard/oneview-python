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
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# Set api_version to 600, default is 300 and this API has been introduced since API 600.
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 600
}

options = {
    "type": "Destination",
    "destinationAddress": "1.1.1.1",
    "userId": "a8cda396-584b-4b68-98a2-4ff9f4d3c01a",
    "port": 162
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Add appliance device SNMP v3 Trap Destination
snmp_v3_trap = oneview_client.appliance_device_snmp_v3_trap_destinations.create(options)
snmp_v3_trap_uri = snmp_v3_trap['uri']
print("\n## Crate appliance SNMP v3 trap destination successfully!")
pprint(snmp_v3_trap)

# Lists the appliance device read community
snmp_v3_trap_list = oneview_client.appliance_device_snmp_v3_trap_destinations.get_all()
print("\n## Got appliance SNMP v3 trap destination successfully!")
pprint(snmp_v3_trap_list)

# Get first element of the List
snmp_v3_trap = snmp_v3_trap_list.pop()

# Get by URI
print("Find an SNMP v3 trap destination by URI")
snmp_v3_trap = oneview_client.appliance_device_snmp_v3_trap_destinations.get(snmp_v3_trap_uri)
pprint(snmp_v3_trap)

# Change appliance device SNMP v3 Trap Destination - Only Community String and Port can be changed
snmp_v3_trap['destinationAddress'] = "1.1.9.9"
snmp_v3_trap = oneview_client.appliance_device_snmp_v3_trap_destinations.update(snmp_v3_trap)
print("\n## Update appliance SNMP v3 trap destination successfully!")
pprint(snmp_v3_trap)

# Delete Created Entry
del_result = oneview_client.appliance_device_snmp_v1_trap_destinations.delete(snmp_v3_trap)
print("\n## Delete appliance SNMP v3 trap destination successfully!")
pprint(del_result)
