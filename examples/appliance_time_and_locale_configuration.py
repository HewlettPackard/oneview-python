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
from hpOneView.oneview_client import OneViewClient
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

oneview_client = OneViewClient(config)

# Lists the appliance time and locale configuration
time_and_locale = oneview_client.appliance_time_and_locale_configuration.get()
print("\n## Got appliance time and locale configurations successfully!")
pprint(time_and_locale)

# Backup original values
bkp = {}
bkp['ntpServers'] = time_and_locale['ntpServers']
bkp['locale'] = time_and_locale['locale']

# Update NTP servers and locale
# Set to use appliance local time and date server
time_and_locale['ntpServers'] = ['127.0.0.1']
# Set locale to Chinese (China) with charset UTF-8
time_and_locale['locale'] = 'zh_CN.UTF-8'
# Remove the date and time, we do not want to update it manually
time_and_locale.pop('dateTime')
time_and_locale = oneview_client.appliance_time_and_locale_configuration.update(time_and_locale)
print("\n## Updated appliance time and locale configurations successfully!")
pprint(time_and_locale)

# Note: Changing the locale will only be fully effective after resetting the appliance

# Revert the changes made
time_and_locale['ntpServers'] = bkp['ntpServers']
time_and_locale['locale'] = bkp['locale']
time_and_locale.pop('dateTime')
time_and_locale = oneview_client.appliance_time_and_locale_configuration.update(time_and_locale)
print("\n## Reverted appliance time and locale configurations successfully!")
pprint(time_and_locale)
