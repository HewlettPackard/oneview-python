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
ALL_SAS_LOGICAL_JBODS = oneview_client.sas_logical_jbods.get_all()
pprint(ALL_SAS_LOGICAL_JBODS)

if ALL_SAS_LOGICAL_JBODS:

    SAS_LOGICAL_JBOD_URI = ALL_SAS_LOGICAL_JBODS[0]["uri"]

    print("\nGet the SAS logical JBOD by uri")
    SAS_LOGICAL_JBOD_BY_URI = oneview_client.sas_logical_jbods.get(id_or_uri=SAS_LOGICAL_JBOD_URI)
    pprint(SAS_LOGICAL_JBOD_BY_URI)

    print("\nGet the list of DRIVES allocated to this SAS logical JBOD")
    DRIVES = oneview_client.sas_logical_jbods.get_DRIVES(id_or_uri=SAS_LOGICAL_JBOD_URI)
    pprint(DRIVES)
