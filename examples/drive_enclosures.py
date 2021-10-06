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
oneview_client = OneViewClient(CONFIG)

print("Get all drive enclosures")
drive_enclosures = oneview_client.drive_enclosures.get_all()
pprint(drive_enclosures)

if drive_enclosures:

    FIRST_DRIVE_ENCLOSURE = drive_enclosures[0]
    DRIVE_ENCLOSURE_URI = FIRST_DRIVE_ENCLOSURE["uri"]

    print("\nGet the drive enclosure by URI")
    drive_enclosure_by_uri = oneview_client.drive_enclosures.get(DRIVE_ENCLOSURE_URI)
    pprint(drive_enclosure_by_uri)

    PRODUCT_NAME = FIRST_DRIVE_ENCLOSURE['productName']

    print("\nGet the drive enclosure by product name")
    drive_enclosure_by_PRODUCT_NAME = oneview_client.drive_enclosures.get_by('productName',
	 PRODUCT_NAME)
    pprint(drive_enclosure_by_PRODUCT_NAME)

    print("\nGet the drive enclosure port map")
    port_map = oneview_client.drive_enclosures.get_port_map(DRIVE_ENCLOSURE_URI)
    pprint(port_map)

    print("\nRefresh the drive enclosure")
    REFRESH_CONFIG = dict(refreshState="RefreshPending")
    refreshed_drive_enclosure = oneview_client.drive_enclosures.refresh_state(DRIVE_ENCLOSURE_URI, REFRESH_CONFIG)
    pprint(refreshed_drive_enclosure)

    print("\nPower off a drive enclosure")
    drive_enclosure_powered_off = oneview_client.drive_enclosures.patch(
        id_or_uri=DRIVE_ENCLOSURE_URI,
        operation="replace",
        path="/powerState",
        value="Off"
    )
    pprint(drive_enclosure_powered_off)
