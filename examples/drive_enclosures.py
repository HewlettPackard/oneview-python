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

print("Get all drive enclosures")
drive_enclosures = oneview_client.drive_enclosures.get_all()
pprint(drive_enclosures)

if drive_enclosures:

    first_drive_enclosure = drive_enclosures[0]
    drive_enclosure_uri = first_drive_enclosure["uri"]

    print("\nGet the drive enclosure by URI")
    drive_enclosure_by_uri = oneview_client.drive_enclosures.get(drive_enclosure_uri)
    pprint(drive_enclosure_by_uri)

    product_name = first_drive_enclosure['productName']

    print("\nGet the drive enclosure by product name")
    drive_enclosure_by_product_name = oneview_client.drive_enclosures.get_by('productName', product_name)
    pprint(drive_enclosure_by_product_name)

    print("\nGet the drive enclosure port map")
    port_map = oneview_client.drive_enclosures.get_port_map(drive_enclosure_uri)
    pprint(port_map)

    print("\nRefresh the drive enclosure")
    refresh_config = dict(refreshState="RefreshPending")
    refreshed_drive_enclosure = oneview_client.drive_enclosures.refresh_state(drive_enclosure_uri, refresh_config)
    pprint(refreshed_drive_enclosure)

    print("\nPower off a drive enclosure")
    drive_enclosure_powered_off = oneview_client.drive_enclosures.patch(
        id_or_uri=drive_enclosure_uri,
        operation="replace",
        path="/powerState",
        value="Off"
    )
    pprint(drive_enclosure_powered_off)
