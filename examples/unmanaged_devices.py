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

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

UNMANAGED_DEVICE_INFORMATION = {
    "name": "MyUnmanagedDevice",
    "model": "Procurve 4200VL",
    "deviceType": "Server"
}

# Add an Unmanaged Device
UNMANAGED_DEVICE_ADDED = oneview_client.unmanaged_devices.add(UNMANAGED_DEVICE_INFORMATION)
print('Added Unmanaged Device "{name}" successfully\n'.format(**UNMANAGED_DEVICE_ADDED))

# Retrieve Unmanaged Device by URI
UNMANAGED_DEVICE = oneview_client.unmanaged_devices.get(UNMANAGED_DEVICE_ADDED['uri'])
print('Get unmanaged device by URI, retrieved "{name}" successfully\n'.format(**UNMANAGED_DEVICE))

# Update the Unmanaged Device
UNMANAGED_DEVICE['name'] = "New Unmanaged Device Name"
UNMANAGED_DEVICE = oneview_client.unmanaged_devices.update(UNMANAGED_DEVICE)
print('Unmanaged Device "{name}" updated successfully\n'.format(**UNMANAGED_DEVICE))

# Get all Unmanaged Devices
print("Get all Unmanaged Devices:")
UNMANAGED_DEVICES_ALL = oneview_client.unmanaged_devices.get_all()
for unm_dev in UNMANAGED_DEVICES_ALL:
    print(" - " + unm_dev['name'])

# Get unmanaged device environmental CONFIGuration
env_CONFIG = oneview_client.unmanaged_devices.get_environmental_configuration(UNMANAGED_DEVICE_\
        ADDED['uri'])
print('Get Environmental Configuration result:')
pprint(env_CONFIG)

# Remove added unmanaged device
oneview_client.unmanaged_devices.remove(UNMANAGED_DEVICE_ADDED)
print("Successfully removed the unmanaged device")

# Add another unmanaged device and remove all
UNMANAGED_DEVICE_ADDED = oneview_client.unmanaged_devices.add(UNMANAGED_DEVICE_INFORMATION)
oneview_client.unmanaged_devices.remove_all("name matches '%'")
print("Successfully removed all the unmanaged device")
