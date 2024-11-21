# -*- coding: utf-8 -*-
###
# (C) Copyright [2023] Hewlett Packard Enterprise Development LP
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

variant = 'Synergy'
options = {
    "hostname": config['server_hostname'],
    "username": config['server_username'],
    "password": config['server_password'],
    "licensingIntent": "OneView",
    "configurationState": "Managed"
}

oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware

# Get list of all server hardware resources
servers = []
print("Get list of all server hardware resources")
server_hardware_all = server_hardwares.get_all()
for serv in server_hardware_all:
    print('  %s' % serv['name'])
    servers.append(serv['name'])

# Get recently added server hardware resource by name
if server_hardware_all:
    server = server_hardwares.get_by_name(servers[0])
    print(server.data)

# Request power operation to change the power state of the physical server.
configuration = {
    "powerState": "Off",
    "powerControl": "MomentaryPress"
}
if server:
    server_power = server.update_power_state(configuration)
    print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))

# Perform a firmware update on server
# Firmware update can only be done on server hardware(Gen10 and later) with no server profile assigned, and server hardware
# should be in powered off state
compliance_configuration = {
    "firmwareBaselineId": config['server_hardware']['firmware_baseline_id'],
    "serverUUID": server.data['uuid']
}
firmware_update_configuration = [{"op": "replace", "value": {"baselineUri": "/rest/firmware-drivers/" + config['server_hardware']['firmware_baseline_id'],
                                  "firmwareInstallType": "FirmwareOnlyOfflineMode", "installationPolicy": "LowerThanBaseline"}
                                  }]
if server and oneview_client.api_version >= 4600:
    firmware_compliance = server.check_firmware_compliance(compliance_configuration)
    if firmware_compliance['serverFirmwareUpdateRequired']:
        print("Updating firmware for the server hardware..")
        server.perform_firmware_update(firmware_update_configuration)
