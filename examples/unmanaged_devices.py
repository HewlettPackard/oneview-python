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
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

unmanaged_device_information = {
    "name": "MyUnmanagedDevice",
    "model": "Procurve 4200VL",
    "deviceType": "Server"
}

# Add an Unmanaged Device
unmanaged_device_added = oneview_client.unmanaged_devices.add(unmanaged_device_information)
print('Added Unmanaged Device "{name}" successfully\n'.format(**unmanaged_device_added))

# Retrieve Unmanaged Device by URI
unmanaged_device = oneview_client.unmanaged_devices.get(unmanaged_device_added['uri'])
print('Get unmanaged device by URI, retrieved "{name}" successfully\n'.format(**unmanaged_device))

# Update the Unmanaged Device
unmanaged_device['name'] = "New Unmanaged Device Name"
unmanaged_device = oneview_client.unmanaged_devices.update(unmanaged_device)
print('Unmanaged Device "{name}" updated successfully\n'.format(**unmanaged_device))

# Get all Unmanaged Devices
print("Get all Unmanaged Devices:")
unmanaged_devices_all = oneview_client.unmanaged_devices.get_all()
for unm_dev in unmanaged_devices_all:
    print(" - " + unm_dev['name'])

# Get unmanaged device environmental configuration
env_config = oneview_client.unmanaged_devices.get_environmental_configuration(unmanaged_device_added['uri'])
print('Get Environmental Configuration result:')
pprint(env_config)

# Remove added unmanaged device
oneview_client.unmanaged_devices.remove(unmanaged_device_added)
print("Successfully removed the unmanaged device")

# Add another unmanaged device and remove all
unmanaged_device_added = oneview_client.unmanaged_devices.add(unmanaged_device_information)
oneview_client.unmanaged_devices.remove_all("name matches '%'")
print("Successfully removed all the unmanaged device")
