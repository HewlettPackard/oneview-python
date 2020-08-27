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

from config_loader import try_load_from_file
from hpeOneView.exceptions import HPEOneViewException
from hpeOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run the get operations by ID, an ID must be defined bellow
fabric_id = 'a7896ce7-c11d-4658-829d-142bc66a85e4'

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all fabrics
print("Get all fabrics")
fabrics = oneview_client.fabrics.get_all()
pprint(fabrics)

# Get all sorting by name descending
print("\nGet all fabrics sorting by name")
fabrics_sorted = oneview_client.fabrics.get_all(sort='name:descending')
pprint(fabrics_sorted)

# Get by Id
try:
    print("\nGet a fabric by id")
    fabrics_byid = oneview_client.fabrics.get(fabric_id)
    pprint(fabrics_byid)
except HPEOneViewException as e:
    print(e.msg)

# Get by name
print("\nGet a fabrics by name")
fabric_byname = oneview_client.fabrics.get_by('name', 'DefaultFabric')[0]
pprint(fabric_byname)

# These methods are available for API version 300 or later
if oneview_client.api_version >= 300:
    # Get reserved vlan ID range for the fabric.
    print("\nGet reserved vlan ID range for the fabric '%s'." % fabric_byname['name'])
    vlan_pool = oneview_client.fabrics.get_reserved_vlan_range(fabric_byname['uri'])
    pprint(vlan_pool)

    # Update the reserved vlan ID range for the fabric
    vlan_pool_data = {
        "start": 100,
        "length": 100
    }
    print("\nUpdate the reserved vlan ID range for the fabric '%s'." % fabric_byname['name'])
    fabric_byname = oneview_client.fabrics.update_reserved_vlan_range(fabric_byname['uri'], vlan_pool_data)
    pprint(fabric_byname)
