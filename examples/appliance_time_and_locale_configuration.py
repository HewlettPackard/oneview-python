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
from hpeOneView.oneview_client import OneViewClient
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

OPTIONS = {
    "locale": "en_US.UTF-8",
    "timezone": "UTC",
    "ntpServers": ["127.0.0.1"],
}


# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
TIME_AND_LOCALEs = oneview_client.appliance_TIME_AND_LOCALE_CONFIGuration

# Lists the appliance time and locale CONFIGuration
TIME_AND_LOCALE = TIME_AND_LOCALEs.get_all()
if TIME_AND_LOCALE:
    print("\n## Got appliance time and locale CONFIGurations successfully!")
    pprint(TIME_AND_LOCALE.data)
else:
    # Create a time and locale with the OPTIONS provided
    TIME_AND_LOCALE = TIME_AND_LOCALEs.create(data=OPTIONS)
    print("\n## Created appliance time and locale CONFIGurations successfully!")
    pprint(TIME_AND_LOCALE.data)

TIME_AND_LOCALE = TIME_AND_LOCALE.data
# Set to use appliance local time and date server
TIME_AND_LOCALE['ntpServers'] = ['127.0.0.1']
# Set locale to Chinese (China) with charset UTF-8
TIME_AND_LOCALE['locale'] = 'zh_CN.UTF-8'
# Remove the date and time, we do not want to update it manually
TIME_AND_LOCALE.pop('dateTime')
TIME_AND_LOCALE = TIME_AND_LOCALEs.create(data=TIME_AND_LOCALE)
print("\n## Created appliance time and locale CONFIGurations successfully!")
pprint(TIME_AND_LOCALE.data)
# Note: Changing the time and locale will only be fully effective after resetting the appliance.
# Until then we cannot run the below create function

'''
try:
    # Revert the changes made
    TIME_AND_LOCALE = TIME_AND_LOCALEs.create(data=OPTIONS)
    print("\n## Reverted appliance time and locale CONFIGurations successfully!")
    pprint(TIME_AND_LOCALE.data)
except HPEOneViewTaskError:
    print("\n## Appliance will be rebooted to make the changes made previously.")

'''
