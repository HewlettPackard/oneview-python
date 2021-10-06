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

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# NOTE: This example requires a SPP and a HOTFIX inside the appliance.

OPTIONS = {
    "customBaselineName": "Service Pack for Synergy",
}
VERSION = "SY-2021.02.01"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
ONEVIEW_CLIENT = OneViewClient(CONFIG)
FIRMWARE_DRIVERS = ONEVIEW_CLIENT.firmware_drivers

# Get all firmwares
print("\nGet list of firmwares managed by the appliance.")
ALL_FIRMWARES = FIRMWARE_DRIVERS.get_all()
for firmware in ALL_FIRMWARES:
    print('  - {}'.format(firmware['name']))

# Get firmware driver schema
FIRMWARE_SCHEMA = FIRMWARE_DRIVERS.get_schema()
pprint(FIRMWARE_SCHEMA)

# Get a firmware by name (VERSION is optional)
print("\nGet firmware by name.")
if ALL_FIRMWARES:
    FIRMWARE_DRIVER = FIRMWARE_DRIVERS.get_by_name(OPTIONS["customBaselineName"], VERSION)

if FIRMWARE_DRIVER:
    print("\nFound a firmware by name: '{}'.\n  uri = '{}'".format(FIRMWARE_DRIVER.data['name'],\
	 FIRMWARE_DRIVER.data['uri']))
else:
    # Getting a SPP and a HOTFIX from within the Appliance to use in the custom SPP creation.
    try:
        SPP = FIRMWARE_DRIVERS.get_by('bundleType', "ServicePack")[0]
        OPTIONS['baselineUri'] = SPP['uri']
        print("\nSPP named '{}' found within appliance. Saving for custom SPP.".format(SPP['name']))
    except IndexError:
        raise HPEOneViewException('No available SPPs found within appliance. Stopping run.')

    try:
        HOTFIX = FIRMWARE_DRIVERS.get_by('bundleType', "Hotfix")[0]
        OPTIONS['HOTFIXUris'] = [HOTFIX['uri']]
        print("\nHotfix named '{}' found within appliance. Saving for custom\
	 SPP.".format(HOTFIX['name']))
    except IndexError:
        raise HPEOneViewException('No available HOTFIXes found within appliance. Stopping run.')

    # Create the custom SPP
    print("\nCreate the custom SPP '{}'".format(OPTIONS['customBaselineName']))
    FIRMWARE_DRIVER = FIRMWARE_DRIVERS.create(OPTIONS)
    print("\nCustom SPP '%s' created successfully" % OPTIONS['customBaselineName'])

# Get by Uri
print("\nGet firmware resource by URI.")
FIRMWARE_DATA = FIRMWARE_DRIVERS.get_by_uri(FIRMWARE_DRIVER.data['uri'])
pprint(FIRMWARE_DATA.data)

# Remove the firmware driver
FIRMWARE_DRIVER.delete()
print("\nCustom SPP '{}' deleted successfully".format(FIRMWARE_DRIVER.data['name']))
