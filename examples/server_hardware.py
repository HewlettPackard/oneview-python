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

options = {
    "hostname": config['server_hostname'],
    "username": config['server_username'],
    "password": config['server_password'],
    "licensingIntent": "OneView",
    "configurationState": "Managed"
}
server_name = "0000A66101, bay 3"

oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware

# Get list of all server hardware resources
print("Get list of all server hardware resources")
server_hardware_all = server_hardwares.get_all()
for serv in server_hardware_all:
    print('  %s' % serv['name'])

server = server_hardwares.get_by_name(server_name)
if not server:
    # Create a rack-mount server
    # This is only supported on appliance which support rack mounted servers
    server = server_hardwares.add(options)
    print("Added rack mount server '%s'.\n  uri = '%s'" % (server.data['name'], server.data['uri']))

# Create Multiple rack-mount servers
# This is only supported on appliance which support rack mounted servers
if oneview_client.api_version >= 600:
    options_to_add_multiple_server = {
        "mpHostsAndRanges": config['server_mpHostsAndRanges'],
        "username": config['server_username'],
        "password": config['server_password'],
        "licensingIntent": "OneView",
        "configurationState": "Managed",
    }
    multiple_server = server_hardwares.add_multiple_servers(options_to_add_multiple_server)
    pprint(multiple_server.data)
else:
    print("\nCANNOT CREATE MULTIPLE SERVERS! Endpoint supported for REST API Versions 600 and above only.\n")

# Get recently added server hardware resource by uri
server_byId = server_hardwares.get_by_uri(server.data['uri'])
print("Found server '%s' by uri.\n  uri = '%s'" %
      (server_byId.data['name'], server_byId.data['uri']))

# Get Statistics with defaults
print("Get server-hardware statistics")
server_utilization = server.get_utilization()
pprint(server_utilization)

# Get Statistics specifying parameters
print("Get server-hardware statistics specifying parameters")
server_utilization = server.get_utilization(fields='AveragePower',
                                            filter='startDate=2016-05-30T03:29:42.000Z',
                                            view='day')
pprint(server_utilization)

# Get list of BIOS/UEFI Values
print("Get list of BIOS/UEFI Values")
bios = server.get_bios()
pprint(bios)

# Get the settings that describe the environmental configuration of server
print(
    "Get the settings that describe the environmental configuration of server")
server_envConf = server.get_environmental_configuration()
pprint(server_envConf)

# Set the calibrated max power of an unmanaged or unsupported server
# hardware resource
print("Set the calibrated max power of an unmanaged or unsupported server hardware resource")
configuration = {
    "calibratedMaxPower": 2500
}
server_updated_encConf = server.update_environmental_configuration(configuration)

# Get URL to launch SSO session for iLO web interface
ilo_sso_url = server.get_ilo_sso_url()
print("URL to launch a Single Sign-On (SSO) session for the iLO web interface for server at uri:\n",
      "{}\n   '{}'".format(server.data['uri'], ilo_sso_url))

# Generates a Single Sign-On (SSO) session for the iLO Java Applet console
# and return URL to launch it
java_remote_console_url = server.get_java_remote_console_url()
print("URL to launch a Single Sign-On (SSO) session for the iiLO Java Applet console for server at uri:\n",
      "   {}\n   '{}'".format(
          server.data['uri'], java_remote_console_url))

# Update iLO firmware to minimum version required
server.update_mp_firware_version()
print("Successfully updated iLO firmware on server at\n  uri: '{}'".format(server.data['uri']))

# Request power operation to change the power state of the physical server.
configuration = {
    "powerState": "Off",
    "powerControl": "MomentaryPress"
}
server_power = server.update_power_state(configuration)
print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))

# Refresh server state
configuration = {
    "refreshState": "RefreshPending"
}
server_refresh = server.refresh_state(configuration)
print("Successfully refreshed the state of the server at:\n   'uri': '{}'".format(
      server_refresh['uri']))

# Get URL to launch SSO session for iLO Integrated Remote Console
# Application (IRC)
# You can also specify ip or consoleType if you need, inside function get_remote_console_url()
remote_console_url = server.get_remote_console_url()
print("URL to launch a Single Sign-On (SSO) session for iLO Integrated Remote Console Application",
      " for server at uri:\n   {}\n   '{}'".format(server.data['uri'], remote_console_url))

if oneview_client.api_version >= 300:
    # These functions are only available for the API version 300 or higher

    # Turn the Server Hardware led light On
    server.patch('replace', '/uidState', 'On')
    print("Server Hardware led light turned on")

    # Get a Firmware by Server Hardware ID
    print("Get a Firmware by Server Hardware ID")
    p = server.get_firmware()
    pprint(p)

    # Get all server hardware firmwares
    print("Get all Server Hardware firmwares")
    p = server_hardwares.get_all_firmwares()
    pprint(p)

    # Get server hardware firmwares filtering by server name
    print("Get Server Hardware firmwares filtering by server name")
    p = server_hardwares.get_all_firmwares(filter="serverName='{}'".format(server_name))
    pprint(p)

if oneview_client.api_version >= 500:
    # Get information describing an 'SDX' partition including a list of physical server blades represented by a
    # server hardware. Only supported by SDX enclosures.
    print("Get SDX physical server hardware")
    sdx_server = server.get_physical_server_hardware()
    pprint(sdx_server)

# This operation works from Oneview API Version 1800.
if oneview_client.api_version >= 1800:
    # Gets the updated version 2 local storage resource for the server.
    print("Get updated local storage resource of server hardware")
    local_storage = server.get_local_storage()
    pprint(local_storage)

# Remove rack server
# This operation works till Oneview API Version 500.
server.remove()
print("Server removed successfully")
