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

from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}
# Try load config from a file (if there is a config file)
config = try_load_from_file()
oneview_client = OneViewClient(config)
time_config = oneview_client.appliance_configuration_timeconfig

# Get all the supported locales
timeconfig = time_config.get_all()
print("\nGot appliance supported locales successfully!")
for timeandlocale in timeconfig:
    print("\nLocale = {}".format(timeandlocale['locale']))
