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

from CONFIG_loader import try_load_from_file
from hpeOneView.exceptions import HPEOneViewException
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

POWER_DEVICE_INFORMATION = {
    "name": "MyPdd",
    "ratedCapacity": 40
}

POWER_DEVICE_INFORMATION_IPDU = {
    "hostname": CONFIG['power_device_hostname'],
    "username": CONFIG['power_device_username'],
    "password": CONFIG['power_device_password'],
}

# Add a Power Device
power_device_added = oneview_client.power_devices.add(POWER_DEVICE_INFORMATION)
print('Added Power Device {name} successfully'.format(**power_device_added))

# Add and Discover an iPDU
ipdu = oneview_client.power_devices.add_ipdu(POWER_DEVICE_INFORMATION_IPDU)
print('Added iPDU {name} successfully'.format(**ipdu))

# Retrieve Power Device by URI
power_device = oneview_client.power_devices.get(power_device_added['uri'])
print('Get power device by URI, retrieved {name} successfully'.format(**power_device))

# Update the Power Device
power_device['name'] = "New Power Device Name"
power_device = oneview_client.power_devices.update(power_device)
print('Power device {name} updated successfully'.format(**power_device))

# Update the Power Device State
power_device = oneview_client.power_devices.get_by('deviceType', 'HPIpduOutlet')
power_device_state = oneview_client.power_devices.update_power_state(power_device[0]['uri'],
	 {"powerState": "Off"})
print('Power device state updated successfully:')
pprint(power_device_state)

# Get the Power Device state
power_device_state = oneview_client.power_devices.get_power_state(power_device[0]['uri'])
print('Getting the new power device state:')
pprint(power_device_state)

# Update the Device Refresh State
power_device_refresh = oneview_client.power_devices.update_refresh_state(power_device[0]['uri'],
                                                                         {"refreshState":
	 "RefreshPending"})
print('Power device state refreshed successfully:')
pprint(power_device_refresh)

# Update the Power Device UID State
power_device_state = oneview_client.power_devices.update_uid_state(power_device[0]['uri'],
	 {"uidState": "On"})
print('Power device UID state updated successfully')

# Get the Power Device UID State
power_device_uid_state = oneview_client.power_devices.get_uid_state(power_device[0]['uri'])
print('Getting the new power device UID state: ' + power_device_uid_state)

# Get power device utilization with defaults
print("Get power device utilization")
try:
    power_devices_utilization = oneview_client.power_devices.get_utilization(power_device[0]['uri'])
    pprint(power_devices_utilization)
except HPEOneViewException as e:
    print(e.msg)

# Get power device utilization specifying parameters
print("Get power device statistics with parameters")
try:
    power_devices_utilization = oneview_client.power_devices.get_utilization(
        power_device[0]['uri'],
        fields='AveragePower',
        filter='startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z',
        view='hour')
    pprint(power_devices_utilization)
except HPEOneViewException as e:
    print(e.msg)

# Remove added power devices
oneview_client.power_devices.remove(ipdu)
oneview_client.power_devices.remove_synchronous(power_device_added)
print("Successfully removed power devices")
