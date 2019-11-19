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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# NOTE: This example requires a SPP and a hotfix inside the appliance.

options = {
    "customBaselineName": "FirmwareDriver1_Example"
}

firmware_name = "HPE Synergy Frame Link Module"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# Get a firmware by name
print("\nGet firmware by name.")
firmware = oneview_client.firmware_drivers.get_by('name', firmware_name)[0]
firmware_uri = firmware['uri']
print("Found a firmware by name: '{name}'.\n  uri = '{uri}'".format(**firmware))

# Get by Uri
print("\nGet firmware resource by URI.")
firmware = oneview_client.firmware_drivers.get(firmware_uri)
print("Found a firmware by uri: '{0}'.".format(firmware_name))

# Get all firmwares
print("\nGet list of firmwares managed by the appliance.")
all_firmwares = oneview_client.firmware_drivers.get_all()
for firmware in all_firmwares:
    print('  {name}'.format(**firmware))

# Getting a SPP and a hotfix from within the Appliance to use in the custom SPP creation.
try:
    hotfix = oneview_client.firmware_drivers.get_by('bundleType', "Hotfix")[0]
    options['hotfixUris'] = [hotfix['uri']]
    print("\nHotfix named %s found within appliance. Saving for custom SPP." % hotfix['name'])
except IndexError:
    raise HPOneViewException('No available hotfixes found within appliance. Stopping run.')

try:
    spp = oneview_client.firmware_drivers.get_by('bundleType', "SPP")[0]
    options['baselineUri'] = spp['uri']
    print("\nSPP named %s found within appliance. Saving for custom SPP." % spp['name'])
except IndexError:
    raise HPOneViewException('No available SPPs found within appliance. Stopping run.')

# Create the custom SPP
print("\nCreate the custom SPP '%s'" % options['customBaselineName'])
firmware = oneview_client.firmware_drivers.create(options)
print("  Custom SPP '%s' created successfully" % options['customBaselineName'])

# Remove the firmware
print("\nDelete the custom SPP '%s'" % options['customBaselineName'])
oneview_client.firmware_drivers.delete(firmware)
print("  Custom SPP '%s' deleted successfully" % options['customBaselineName'])
