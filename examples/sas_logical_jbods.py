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

print("\nGet all SAS logical JBODs")
all_sas_logical_jbods = oneview_client.sas_logical_jbods.get_all()
pprint(all_sas_logical_jbods)

if all_sas_logical_jbods:

    sas_logical_jbod_uri = all_sas_logical_jbods[0]["uri"]

    print("\nGet the SAS logical JBOD by uri")
    sas_logical_jbod_by_uri = oneview_client.sas_logical_jbods.get(id_or_uri=sas_logical_jbod_uri)
    pprint(sas_logical_jbod_by_uri)

    print("\nGet the list of drives allocated to this SAS logical JBOD")
    drives = oneview_client.sas_logical_jbods.get_drives(id_or_uri=sas_logical_jbod_uri)
    pprint(drives)
