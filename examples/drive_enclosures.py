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

# This resource is only available on HPE Synergy

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
ONEVIEW_CLIENT = OneViewClient(CONFIG)

print("Get all drive enclosures")
DRIVE_ENCLOSURES = ONEVIEW_CLIENT.drive_enclosures.get_all()
pprint(DRIVE_ENCLOSURES)

if DRIVE_ENCLOSURES:

    FIRST_DRIVE_ENCLOSURE = DRIVE_ENCLOSURES[0]
    DRIVE_ENCLOSURE_URI = FIRST_DRIVE_ENCLOSURE["uri"]

    print("\nGet the drive enclosure by URI")
    DRIVE_ENCLOSURE_BY_URI = ONEVIEW_CLIENT.drive_enclosures.get(DRIVE_ENCLOSURE_URI)
    pprint(DRIVE_ENCLOSURE_BY_URI)

    PRODUCT_NAME = FIRST_DRIVE_ENCLOSURE['productName']

    print("\nGet the drive enclosure by product name")
    DRIVE_ENCLOSURE_BY_PRODUCT_NAME = ONEVIEW_CLIENT.drive_enclosures.get_by('productName',\
	 PRODUCT_NAME)
    pprint(DRIVE_ENCLOSURE_BY_PRODUCT_NAME)

    print("\nGet the drive enclosure port map")
    PORT_MAP = ONEVIEW_CLIENT.drive_enclosures.get_port_map(DRIVE_ENCLOSURE_URI)
    pprint(PORT_MAP)

    print("\nRefresh the drive enclosure")
    REFRESH_CONFIG = dict(refreshState="RefreshPending")
    REFRESHED_DRIVE_ENCLOSURE = ONEVIEW_CLIENT.drive_enclosures.refresh_state(DRIVE_ENCLOSURE_URI,\
	 REFRESH_CONFIG)
    pprint(REFRESHED_DRIVE_ENCLOSURE)

    print("\nPower off a drive enclosure")
    DRIVE_ENCLOSURE_POWERED_OFF = ONEVIEW_CLIENT.drive_enclosures.patch(
        id_or_uri=DRIVE_ENCLOSURE_URI,
        operation="replace",
        path="/powerState",
        value="Off"
    )
    pprint(DRIVE_ENCLOSURE_POWERED_OFF)
