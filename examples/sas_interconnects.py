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
oneview_client = OneViewClient(CONFIG)
SAS_INTERCONNECTS = oneview_client.sas_interconnects

# Get all, with defaults
print("\nGet all SAS Interconnects")
ALL_SAS_INTERCONNECTS = SAS_INTERCONNECTS.get_all()
pprint(ALL_SAS_INTERCONNECTS)

# Get the first 10 records
print("\nGet the first ten SAS Interconnects")
SAS_INTERCONNECTS_LIMITED = SAS_INTERCONNECTS.get_all(0, 10)
pprint(SAS_INTERCONNECTS_LIMITED)

if ALL_SAS_INTERCONNECTS:
    SAS_INTERCONNECT_URI = ALL_SAS_INTERCONNECTS[0]['uri']

    # Get by Uri
    print("\nGet a SAS Interconnect by uri")
    SAS_INTERCONNECT_BY_URI = SAS_INTERCONNECTS.get_by_uri(SAS_INTERCONNECT_URI)
    pprint(SAS_INTERCONNECT_BY_URI.data)

    if SAS_INTERCONNECT_BY_URI.data["powerState"] == 'Off':
        print("\nTurn on power for SAS interconnect %s" % SAS_INTERCONNECT_BY_URI.data['name'])
        SAS_INTERCONNECT_BY_URI.patch(
            operation='replace',
            path='/powerState',
            value='On'
        )
        print("Done!")

    print("\nRefresh a SAS interconnect")
    SAS_INTERCONNECT_BY_URI.refresh_state(
        configuration={"refreshState": "RefreshPending"}
    )
    print("Done!")

    print("\nTurn 'On' UID light on SAS interconnect %s" % SAS_INTERCONNECT_BY_URI.data['name'])
    SAS_INTERCONNECT_BY_URI.patch(
        operation='replace',
        path='/uidState',
        value='On'
    )
    print("Done!")

    print("\nSoft Reset SAS interconnect %s" % SAS_INTERCONNECT_BY_URI.data['name'])
    SAS_INTERCONNECT_BY_URI.patch(
        operation='replace',
        path='/softResetState',
        value='Reset'
    )
    print("Done!")

    print("\nReset SAS interconnect %s" % SAS_INTERCONNECT_BY_URI.data['name'])
    SAS_INTERCONNECT_BY_URI.patch(
        operation='replace',
        path='/hardResetState',
        value='Reset'
    )
    print("Done!")

    print("\nTurn off power for SAS interconnect %s" % SAS_INTERCONNECT_BY_URI.data['name'])
    SAS_INTERCONNECT_BY_URI.patch(
        operation='replace',
        path='/powerState',
        value='Off'
    )
    print("Done!")
