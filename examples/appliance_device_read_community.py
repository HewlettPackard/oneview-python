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
    "communityString": "public"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file()

oneview_client = OneViewClient(config)

# Lists the appliance device read community
read_community = oneview_client.appliance_device_read_community.get()
print("\n## Got appliance device read community successfully!")
pprint(read_community)

# Backup original values
bkp = {}
bkp['communityString'] = read_community['communityString']

# Update Read Community
# Set to use appliance device read community
read_community['communityString'] = options['communityString']
read_community = oneview_client.appliance_device_read_community.update(read_community)
print("\n## Updated appliance device read community string successfully!")
pprint(read_community)

# Revert the changes made
read_community['communityString'] = bkp['communityString']
read_community = oneview_client.appliance_device_read_community.update(read_community)
print("\n## Reverted appliance device read community string successfully!")
pprint(read_community)
