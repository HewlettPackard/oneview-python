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
sas_interconnect_types = oneview_client.sas_interconnect_types

# Get all
print("\nGet all SAS Interconnect Types")
sas_interconnect_types_all = sas_interconnect_types.get_all()
pprint(sas_interconnect_types_all)

if sas_interconnect_types_all:
    # Get by URI
    print("\nGet a SAS Interconnect Type by URI")
    uri = sas_interconnect_types_all[0]['uri']
    sas_interconnect_type_by_uri = sas_interconnect_types.get_by_uri(uri)
    pprint(sas_interconnect_type_by_uri.data)

    # Get by name
    print("\nGet a SAS Interconnect Type by name")
    name = sas_interconnect_types_all[0]['name']
    sas_interconnect_type_by_name = sas_interconnect_types.get_by_name(name)
    pprint(sas_interconnect_type_by_name.data)
