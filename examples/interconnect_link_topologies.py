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
import re
from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# This resource is only available on HPE Synergy

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

# Get all interconnect link topologies
print("Get all interconnect link topologies")
INTERCONNECT_LINK_TOPOLOGIES = ONEVIEW_CLIENT.interconnect_link_topologies.get_all()
pprint(INTERCONNECT_LINK_TOPOLOGIES)

# Get all sorting by name descending
print("Get all interconnect link topologies sorting by name")
INTERCONNECT_LINK_TOPOLOGIES_SORTED = ONEVIEW_CLIENT.interconnect_link_topologies.get_all\
        (sort='name:descending')
pprint(INTERCONNECT_LINK_TOPOLOGIES_SORTED)

# Get by uri
if INTERCONNECT_LINK_TOPOLOGIES:
    print("Get an interconnect link topology by uri")
    ILT_URI = INTERCONNECT_LINK_TOPOLOGIES[0]['uri']
    ILT_BYURI = ONEVIEW_CLIENT.interconnect_link_topologies.get(ILT_URI)
    print("   Found '{name}' at uri: {uri}".format(**ILT_BYURI))

# Get by Id
if INTERCONNECT_LINK_TOPOLOGIES:
    print("Get an interconnect link topology by id")
    ILT_ID = re.sub("/rest/interconnect-link-topologies/", '', INTERCONNECT_LINK_TOPOLOGIES\
            [0]['uri'])
    ILT_BYID = ONEVIEW_CLIENT.interconnect_link_topologies.get(ILT_ID)
    print("   Found '{name}' at uri: {uri}".format(**ILT_BYID))

# Get by name
if INTERCONNECT_LINK_TOPOLOGIES:
    print("Get an interconnect link topology by name")
    ILT_BYNAME = ONEVIEW_CLIENT.interconnect_link_topologies.get_by(
        'name', INTERCONNECT_LINK_TOPOLOGIES[0]['name'])[0]
    print("   Found '{name}' at uri: {uri}".format(**ILT_BYNAME))
