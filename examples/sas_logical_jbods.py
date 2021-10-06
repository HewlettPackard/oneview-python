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

print("\nGet all SAS logical JBODs")
all_sas_logical_jbods = oneview_client.sas_logical_jbods.get_all()
pprint(all_sas_logical_jbods)

if all_sas_logical_jbods:

    SAS_LOGICAL_JBOD_URI = all_sas_logical_jbods[0]["uri"]

    print("\nGet the SAS logical JBOD by uri")
    sas_logical_jbod_by_uri = oneview_client.sas_logical_jbods.get(id_or_uri=SAS_LOGICAL_JBOD_URI)
    pprint(sas_logical_jbod_by_uri)

    print("\nGet the list of drives allocated to this SAS logical JBOD")
    drives = oneview_client.sas_logical_jbods.get_drives(id_or_uri=SAS_LOGICAL_JBOD_URI)
    pprint(drives)
