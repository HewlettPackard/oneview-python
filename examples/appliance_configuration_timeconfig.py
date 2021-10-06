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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}
# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
time_CONFIG = oneview_client.appliance_CONFIGuration_TIMECONFIG

# Get all the supported locales
TIMECONFIG = time_CONFIG.get_all()
print("\nGot appliance supported locales successfully!")
for timeandlocale in TIMECONFIG:
    print("\nLocale = {}".format(timeandlocale['locale']))
