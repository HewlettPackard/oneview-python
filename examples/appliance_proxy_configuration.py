# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
        "userName": "<username>",
        "password": "<password>"
    }
}

URI = '/rest/appliance/proxy-CONFIG'

# Try load CONFIG from a file
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
proxy = oneview_client.appliance_PROXY_CONFIGuration

# Configure proxy with HTTP protocol
print("\nCreating proxy with HTTP:\n")
PROXY_CONFIG = {
    "server": "<server_ip>",
    "port": 443,
    "username": "<username>",
    "password": "<password>",
    "communicationProtocol": "HTTP"
}

NEW_PROXY = proxy.create(PROXY_CONFIG)
pprint(NEW_PROXY.data)
print("Proxy created successfully\n")

# Get proxy CONFIGuration from appliance
print("\nGet proxy CONFIGuration from appliance:\n ")
PROXY_INFO = proxy.get_by_proxy(PROXY_CONFIG["server"])
pprint(PROXY_INFO.data)

# Delete proxy CONFIGured on the appliance
print("\nDelete Proxy")
proxy.delete()
print("Proxy deleted successfully")
