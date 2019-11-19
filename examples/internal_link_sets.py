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
        "password": "<password>",
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
internal_link_sets = oneview_client.internal_link_sets

# Get all, with defaults
print("Get all internal-link-sets")
internal_links = internal_link_sets.get_all()
pprint(internal_links)

internal_link_set_uri = internal_links[0]['uri']
internal_link_set_name = internal_links[0]['name']

# Find by name
internal_links_by_name = internal_link_sets.get_by_name(internal_links[0]["name"])
print("\nFound the internal-link-sets by name: '{}':".format(internal_links_by_name.data["name"]))
