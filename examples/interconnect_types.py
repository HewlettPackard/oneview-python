# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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
INTERCONNECT_TYPES = oneview_client.INTERCONNECT_TYPES

# Get all supported interconnect types
print(">>> Get all supported interconnect types")
ALL_INTERCONNECT_TYPES = INTERCONNECT_TYPES.get_all()
for interconn in ALL_INTERCONNECT_TYPES:
    print(" - {}".format(interconn['NAME']))

# Get all sorting by NAME descending
print(">>> Get all interconnect-types sorting by NAME")
INTERCONNECT_TYPES_SORTED = INTERCONNECT_TYPES.get_all(sort='NAME:descending')
for interconn in INTERCONNECT_TYPES_SORTED:
    print(" - {}".format(interconn['NAME']))

# Get by NAME
print("Get an interconnect_type by NAME")
if INTERCONNECT_TYPES_SORTED:
    NAME = INTERCONNECT_TYPES_SORTED[0]["NAME"]
    INTERCONNECT_TYPE_BYNAME = INTERCONNECT_TYPES.get_by_NAME(NAME)
    pprint(INTERCONNECT_TYPE_BYNAME.data, depth=1)
