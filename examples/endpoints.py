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

from config_loader import try_load_from_file
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

ONEVIEW_CLIENT = OneViewClient(CONFIG)

# Get all endpoints
print("Get all endpoints")
ENDPOINTS_ALL = ONEVIEW_CLIENT.endpoints.get_all()
pprint(ENDPOINTS_ALL)

# Get endpoints filtered to only the one with a specified WWN
print("Get endpoints filtered to only the one with a specified WWN")
QUERY = "WWN eq '{}'".format(WWN)
ENPOINTS_WITH_QUERY = ONEVIEW_CLIENT.endpoints.get_all(0, -1, QUERY=QUERY)
pprint(ENPOINTS_WITH_QUERY)
