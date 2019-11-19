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

# Get all
print("\nGet all SAS logical JBOD attachments")
sas_logical_jbod_attachments = oneview_client.sas_logical_jbod_attachments.get_all()
pprint(sas_logical_jbod_attachments)

if sas_logical_jbod_attachments:
    # Get by URI
    print("\nGet a SAS logical JBOD attachment by URI")
    uri = sas_logical_jbod_attachments[0]['uri']
    sas_logical_jbod_attachment_by_uri = oneview_client.sas_logical_jbod_attachments.get(uri)
    pprint(sas_logical_jbod_attachment_by_uri)

    # Get by name
    print("\nGet a SAS logical JBOD attachment by name")
    name = sas_logical_jbod_attachments[0]['name']
    sas_logical_jbod_attachment_by_name = oneview_client.sas_logical_jbod_attachments.get_by('name', name)
    pprint(sas_logical_jbod_attachment_by_name)
