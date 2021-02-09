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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "locale": "en_US.UTF-8",
    "timezone": "UTC",
    "ntpServers": ["127.0.0.1"],
}


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
time_and_locales = oneview_client.appliance_time_and_locale_configuration

# Lists the appliance time and locale configuration
time_and_locale = time_and_locales.get_all()
if time_and_locale:
    print("\n## Got appliance time and locale configurations successfully!")
    pprint(time_and_locale)
else:
    # Create a time and locale with the options provided
    time_and_locale = time_and_locales.create(data=options)
    print("\n## Created appliance time and locale configurations successfully!")
    pprint(time_and_locale.data)

time_and_locale = time_and_locale.data
# Set to use appliance local time and date server
time_and_locale['ntpServers'] = ['127.0.0.1']
# Set locale to Chinese (China) with charset UTF-8
time_and_locale['locale'] = 'zh_CN.UTF-8'
# Remove the date and time, we do not want to update it manually
time_and_locale.pop('dateTime')
time_and_locale = time_and_locales.create(data=time_and_locale)
print("\n## Created appliance time and locale configurations successfully!")
pprint(time_and_locale.data)
# Note: Changing the locale will only be fully effective after resetting the appliance

# Revert the changes made
time_and_locale = time_and_locales.create(data=options)
print("\n## Reverted appliance time and locale configurations successfully!")
pprint(time_and_locale.data)
