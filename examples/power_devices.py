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
    "hostname": CONFIG['POWER_DEVICE_hostname'],
    "username": CONFIG['POWER_DEVICE_username'],
    "password": CONFIG['POWER_DEVICE_password'],
}

# Add a Power Device
POWER_DEVICE_ADDED = oneview_client.POWER_DEVICEs.add(POWER_DEVICE_INFORMATION)
print('Added Power Device {name} successfully'.format(**POWER_DEVICE_ADDED))

# Add and Discover an iPDU
IPDU = oneview_client.POWER_DEVICEs.add_IPDU(POWER_DEVICE_INFORMATION_IPDU)
print('Added iPDU {name} successfully'.format(**IPDU))

# Retrieve Power Device by URI
POWER_DEVICE = oneview_client.POWER_DEVICEs.get(POWER_DEVICE_ADDED['uri'])
print('Get power device by URI, retrieved {name} successfully'.format(**POWER_DEVICE))

# Update the Power Device
POWER_DEVICE['name'] = "New Power Device Name"
POWER_DEVICE = oneview_client.POWER_DEVICEs.update(POWER_DEVICE)
print('Power device {name} updated successfully'.format(**POWER_DEVICE))

# Update the Power Device State
POWER_DEVICE = oneview_client.POWER_DEVICEs.get_by('deviceType', 'HPIpduOutlet')
POWER_DEVICE_state = oneview_client.POWER_DEVICEs.update_power_state(POWER_DEVICE[0]['uri'],
	 {"powerState": "Off"})
print('Power device state updated successfully:')
pprint(POWER_DEVICE_state)

# Get the Power Device state
POWER_DEVICE_state = oneview_client.POWER_DEVICEs.get_power_state(POWER_DEVICE[0]['uri'])
print('Getting the new power device state:')
pprint(POWER_DEVICE_state)

# Update the Device Refresh State
POWER_DEVICE_refresh = oneview_client.POWER_DEVICEs.update_refresh_state(POWER_DEVICE[0]['uri'],
                                                                         {"refreshState":
	 "RefreshPending"})
print('Power device state refreshed successfully:')
pprint(POWER_DEVICE_refresh)

# Update the Power Device UID State
POWER_DEVICE_state = oneview_client.POWER_DEVICEs.update_uid_state(POWER_DEVICE[0]['uri'],
	 {"uidState": "On"})
print('Power device UID state updated successfully')

# Get the Power Device UID State
POWER_DEVICE_uid_state = oneview_client.POWER_DEVICEs.get_uid_state(POWER_DEVICE[0]['uri'])
print('Getting the new power device UID state: ' + POWER_DEVICE_uid_state)

# Get power device utilization with defaults
print("Get power device utilization")
try:
    POWER_DEVICEs_utilization = oneview_client.POWER_DEVICEs.get_utilization(POWER_DEVICE[0]['uri'])
    pprint(POWER_DEVICEs_utilization)
except HPEOneViewException as e:
    print(e.msg)

# Get power device utilization specifying parameters
print("Get power device statistics with parameters")
try:
    POWER_DEVICEs_utilization = oneview_client.POWER_DEVICEs.get_utilization(
        POWER_DEVICE[0]['uri'],
        fields='AveragePower',
        filter='startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z',
        view='hour')
    pprint(POWER_DEVICEs_utilization)
except HPEOneViewException as e:
    print(e.msg)

# Remove added power devices
oneview_client.POWER_DEVICEs.remove(IPDU)
oneview_client.POWER_DEVICEs.remove_synchronous(POWER_DEVICE_ADDED)
print("Successfully removed power devices")
