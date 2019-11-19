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
from hpOneView.exceptions import HPOneViewException
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

# An existent Logical Downlink ID is required to run this example
logical_downlink_id = '5b0f2e7a-394f-47e9-aed0-e4be225e0e19'
logical_downlink_name = 'LD49f094dd-1732-48c5-9aa8-2ff827578887 (HP VC FlexFabric-20/40 F8 Module)'

# Get logical downlink by id
try:
    print("\nGet logical downlink by id")
    log_downlink = oneview_client.logical_downlinks.get(logical_downlink_id)
    pprint(log_downlink)
except HPOneViewException as e:
    print(e.msg)

# Get logical downlink by id without Ethernet networks
try:
    print("\nGet logical downlink by id without Ethernet networks")
    log_downlink_without_ethernet = oneview_client.logical_downlinks.get_without_ethernet(logical_downlink_id)
    pprint(log_downlink_without_ethernet)
except HPOneViewException as e:
    print(e.msg)

# Get logical downlink by name
try:
    print("\nGet logical downlink by name")
    log_downlink_by_name = oneview_client.logical_downlinks.get_by('name', logical_downlink_name)
    pprint(log_downlink_by_name)
except HPOneViewException as e:
    print(e.msg)

# Get all logical downlinks
print("\nGet all logical downlinks")
log_downlinks = oneview_client.logical_downlinks.get_all()
pprint(log_downlinks)

# Get all sorting by name descending
print("\nGet all logical downlinks sorting by name")
log_downlinks_sorted = oneview_client.logical_downlinks.get_all(sort='name:descending')
pprint(log_downlinks_sorted)

# Get all logical downlinks without Ethernet
print("\nGet all logical downlinks without Ethernet")
log_downlinks_without_ethernet = oneview_client.logical_downlinks.get_all_without_ethernet()
pprint(log_downlinks_without_ethernet)
