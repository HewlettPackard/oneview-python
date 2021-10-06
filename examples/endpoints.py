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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# To run this example, you must specify a WWN
WWN = None

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Get all endpoints
print("Get all endpoints")
endpoints_all = oneview_client.endpoints.get_all()
pprint(endpoints_all)

# Get endpoints filtered to only the one with a specified WWN
print("Get endpoints filtered to only the one with a specified WWN")
QUERY = "WWN eq '{}'".format(WWN)
enpoints_with_QUERY = oneview_client.endpoints.get_all(0, -1, QUERY=QUERY)
pprint(enpoints_with_QUERY)
