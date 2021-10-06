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
        "userName": "<userNAME>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
sas_interconnect_types = oneview_client.sas_interconnect_types

# Get all
print("\nGet all SAS Interconnect Types")
SAS_INTERCONNECT_TYPES_ALL = sas_interconnect_types.get_all()
pprint(SAS_INTERCONNECT_TYPES_ALL)

if SAS_INTERCONNECT_TYPES_ALL:
    # Get by URI
    print("\nGet a SAS Interconnect Type by URI")
    URI = SAS_INTERCONNECT_TYPES_ALL[0]['URI']
    SAS_INTERCONNECT_TYPE_BY_URI = sas_interconnect_types.get_by_URI(URI)
    pprint(SAS_INTERCONNECT_TYPE_BY_URI.data)

    # Get by NAME
    print("\nGet a SAS Interconnect Type by NAME")
    NAME = SAS_INTERCONNECT_TYPES_ALL[0]['NAME']
    SAS_INTERCONNECT_TYPE_BY_NAME = sas_interconnect_types.get_by_NAME(NAME)
    pprint(SAS_INTERCONNECT_TYPE_BY_NAME.data)
