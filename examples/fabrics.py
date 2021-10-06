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

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run the get operations by ID, an ID must be defined bellow
FABRIC_ID = 'a7896ce7-c11d-4658-829d-142bc66a85e4'

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

# Get all fabrics
print("Get all fabrics")
FABRICS = ONEVIEW_CLIENT.fabrics.get_all()
pprint(FABRICS)

# Get all sorting by name descending
print("\nGet all fabrics sorting by name")
FABRICS_SORTED = ONEVIEW_CLIENT.fabrics.get_all(sort='name:descending')
pprint(FABRICS_SORTED)

# Get by Id
try:
    print("\nGet a fabric by id")
    FABRICS_BYID = ONEVIEW_CLIENT.fabrics.get(FABRIC_ID)
    pprint(FABRICS_BYID)
except HPEOneViewException as err:
    print(err.msg)

# Get by name
print("\nGet a fabrics by name")
FABRIC_BYNAME = ONEVIEW_CLIENT.fabrics.get_by('name', 'DefaultFabric')[0]
pprint(FABRIC_BYNAME)

# These methods are available for API version 300 or later
if ONEVIEW_CLIENT.api_version >= 300:
    # Get reserved vlan ID range for the fabric.
    print("\nGet reserved vlan ID range for the fabric '%s'." % FABRIC_BYNAME['name'])
    VLAN_POOL = ONEVIEW_CLIENT.fabrics.get_reserved_vlan_range(FABRIC_BYNAME['uri'])
    pprint(VLAN_POOL)

    # Update the reserved vlan ID range for the fabric
    VLAN_POOL_DATA = {
        "start": 100,
        "length": 100
    }
    print("\nUpdate the reserved vlan ID range for the fabric '%s'." % FABRIC_BYNAME['name'])
    FABRIC_BYNAME = ONEVIEW_CLIENT.fabrics.update_reserved_vlan_range(FABRIC_BYNAME['uri'],\
	 VLAN_POOL_DATA)
    pprint(FABRIC_BYNAME)
