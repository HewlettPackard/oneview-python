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
        "userName": "<userNAME>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Get all
print("\nGet all SAS logical JBOD attachments")
SAS_LOGICAL_JBOD_ATTACHMENTS = oneview_client.SAS_LOGICAL_JBOD_ATTACHMENTS.get_all()
pprint(SAS_LOGICAL_JBOD_ATTACHMENTS)

if SAS_LOGICAL_JBOD_ATTACHMENTS:
    # Get by URI
    print("\nGet a SAS logical JBOD attachment by URI")
    URI = SAS_LOGICAL_JBOD_ATTACHMENTS[0]['URI']
    SAS_URI = oneview_client.SAS_LOGICAL_JBOD_ATTACHMENTS.get(URI)
    pprint(SAS_URI)

    # Get by NAME
    print("\nGet a SAS logical JBOD attachment by NAME")
    NAME = SAS_LOGICAL_JBOD_ATTACHMENTS[0]['NAME']
    SAS_NAME = oneview_client.SAS_LOGICAL_JBOD_ATTACHMENTS.get_by(\
            'NAME', NAME)
    pprint(SAS_NAME)
