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

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# NOTE: This example requires a SPP and a hotfix inside the appliance.

options = {
    "customBaselineName": "Service Pack for Synergy",
}
version = "SY-2021.02.01"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
firmware_drivers = oneview_client.firmware_drivers

# Get all firmwares
print("\nGet list of firmwares managed by the appliance.")
all_firmwares = firmware_drivers.get_all()
for firmware in all_firmwares:
    print('  - {}'.format(firmware['name']))

# Get firmware driver schema
firmware_schema = firmware_drivers.get_schema()
pprint(firmware_schema)

# Get a firmware by name (version is optional)
print("\nGet firmware by name.")
if all_firmwares:
    firmware_driver = firmware_drivers.get_by_name(options["customBaselineName"], version)

if firmware_driver:
    print("\nFound a firmware by name: '{}'.\n  uri = '{}'".format(firmware_driver.data['name'], firmware_driver.data['uri']))
else:
    # Getting a SPP and a hotfix from within the Appliance to use in the custom SPP creation.
    try:
        spp = firmware_drivers.get_by('bundleType', "ServicePack")[0]
        options['baselineUri'] = spp['uri']
        print("\nSPP named '{}' found within appliance. Saving for custom SPP.".format(spp['name']))
    except IndexError:
        raise HPEOneViewException('No available SPPs found within appliance. Stopping run.')

    try:
        hotfix = firmware_drivers.get_by('bundleType', "Hotfix")[0]
        options['hotfixUris'] = [hotfix['uri']]
        print("\nHotfix named '{}' found within appliance. Saving for custom SPP.".format(hotfix['name']))
    except IndexError:
        raise HPEOneViewException('No available hotfixes found within appliance. Stopping run.')

    # Create the custom SPP
    print("\nCreate the custom SPP '{}'".format(options['customBaselineName']))
    firmware_driver = firmware_drivers.create(options)
    print("\nCustom SPP '%s' created successfully" % options['customBaselineName'])

# Get by Uri
print("\nGet firmware resource by URI.")
firmware_data = firmware_drivers.get_by_uri(firmware_driver.data['uri'])
pprint(firmware_data.data)

# Remove the firmware driver
firmware_driver.delete()
print("\nCustom SPP '{}' deleted successfully".format(firmware_driver.data['name']))
