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
sas_interconnects = oneview_client.sas_interconnects

# Get all, with defaults
print("\nGet all SAS Interconnects")
all_sas_interconnects = sas_interconnects.get_all()
pprint(all_sas_interconnects)

# Get the first 10 records
print("\nGet the first ten SAS Interconnects")
sas_interconnects_limited = sas_interconnects.get_all(0, 10)
pprint(sas_interconnects_limited)

if all_sas_interconnects:
    sas_interconnect_uri = all_sas_interconnects[0]['uri']

    # Get by Uri
    print("\nGet a SAS Interconnect by uri")
    sas_interconnect_by_uri = sas_interconnects.get_by_uri(sas_interconnect_uri)
    pprint(sas_interconnect_by_uri.data)

    if sas_interconnect_by_uri.data["powerState"] == 'Off':
        print("\nTurn on power for SAS interconnect %s" % sas_interconnect_by_uri.data['name'])
        sas_interconnect_by_uri.patch(
            operation='replace',
            path='/powerState',
            value='On'
        )
        print("Done!")

    print("\nRefresh a SAS interconnect")
    sas_interconnect_by_uri.refresh_state(
        configuration={"refreshState": "RefreshPending"}
    )
    print("Done!")

    print("\nTurn 'On' UID light on SAS interconnect %s" % sas_interconnect_by_uri.data['name'])
    sas_interconnect_by_uri.patch(
        operation='replace',
        path='/uidState',
        value='On'
    )
    print("Done!")

    print("\nSoft Reset SAS interconnect %s" % sas_interconnect_by_uri.data['name'])
    sas_interconnect_by_uri.patch(
        operation='replace',
        path='/softResetState',
        value='Reset'
    )
    print("Done!")

    print("\nReset SAS interconnect %s" % sas_interconnect_by_uri.data['name'])
    sas_interconnect_by_uri.patch(
        operation='replace',
        path='/hardResetState',
        value='Reset'
    )
    print("Done!")

    print("\nTurn off power for SAS interconnect %s" % sas_interconnect_by_uri.data['name'])
    sas_interconnect_by_uri.patch(
        operation='replace',
        path='/powerState',
        value='Off'
    )
    print("Done!")
