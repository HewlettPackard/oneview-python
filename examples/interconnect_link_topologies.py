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

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all interconnect link topologies
print("Get all interconnect link topologies")
interconnect_link_topologies = oneview_client.interconnect_link_topologies.get_all()
pprint(interconnect_link_topologies)

# Get all sorting by name descending
print("Get all interconnect link topologies sorting by name")
interconnect_link_topologies_sorted = oneview_client.interconnect_link_topologies.get_all(sort='name:descending')
pprint(interconnect_link_topologies_sorted)

# Get by uri
if interconnect_link_topologies:
    print("Get an interconnect link topology by uri")
    ilt_uri = interconnect_link_topologies[0]['uri']
    ilt_byuri = oneview_client.interconnect_link_topologies.get(ilt_uri)
    print("   Found '{name}' at uri: {uri}".format(**ilt_byuri))

# Get by Id
if interconnect_link_topologies:
    print("Get an interconnect link topology by id")
    ilt_id = re.sub("/rest/interconnect-link-topologies/", '', interconnect_link_topologies[0]['uri'])
    ilt_byid = oneview_client.interconnect_link_topologies.get(ilt_id)
    print("   Found '{name}' at uri: {uri}".format(**ilt_byid))

# Get by name
if interconnect_link_topologies:
    print("Get an interconnect link topology by name")
    ilt_byname = oneview_client.interconnect_link_topologies.get_by(
        'name', interconnect_link_topologies[0]['name'])[0]
    print("   Found '{name}' at uri: {uri}".format(**ilt_byname))
