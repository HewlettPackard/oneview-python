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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "destination": "1.1.1.1",
    "communityString": "testOne",
    "port": 162
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Add appliance device SNMP v1 Trap Destination
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.create(options)
snmp_v1_trap_uri = snmp_v1_trap['uri']
print("\n## Create appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Add appliance device SNMP v1 Trap Destination with ID
trap_id = 9
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.create(options, trap_id)
print("\n## Create appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Lists the appliance device SNMP v1 Trap Destination
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.get_all()
print("\n## Got appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Lists the appliance device SNMP v1 Trap Destination by destination (unique)
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.get_by('destination', '1.1.1.1')
print("\n## Got appliance SNMP v1 trap by destination successfully!")
pprint(snmp_v1_trap)

# Get by URI
print("Find an SNMP v1 trap destination by URI")
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.get(snmp_v1_trap_uri)
pprint(snmp_v1_trap)

# Change appliance device SNMP v1 Trap Destination - Only Community String and Port can be changed
snmp_v1_trap['communityString'] = 'testTwo'
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.update(snmp_v1_trap)
print("\n## Update appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Delete Created Entry
del_result = oneview_client.appliance_device_snmp_v1_trap_destinations.delete(snmp_v1_trap)
print("\n## Delete appliance SNMP v1 trap destination successfully!")
pprint(del_result)
