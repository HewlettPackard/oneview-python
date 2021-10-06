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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
internal_link_sets = oneview_client.internal_link_sets

# Get all, with defaults
print("Get all internal-link-sets")
INTERNAL_LINKS = internal_link_sets.get_all()
pprint(INTERNAL_LINKS)

INTERNAL_LINK_SET_URI = INTERNAL_LINKS[0]['uri']
INTERNAL_LINK_SET_NAME = INTERNAL_LINKS[0]['name']

# Find by name
INTERNAL_LINKS_BY_NAME = internal_link_sets.get_by_name(INTERNAL_LINKS[0]["name"])
print("\nFound the internal-link-sets by name: '{}':".format(INTERNAL_LINKS_BY_NAME.data["name"]))
