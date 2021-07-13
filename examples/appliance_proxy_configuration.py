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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

uri = '/rest/appliance/proxy-config'

# Try load config from a file
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
proxy = oneview_client.appliance_proxy_configuration

# Configure proxy with HTTP protocol
print("\nCreating proxy with HTTP:\n")
proxy_config = {
    "server": "16.85.88.10",
    "port": 8080,
    "username": "dcs",
    "password": "dcs",
    "communicationProtocol": "HTTP"
}

new_proxy = proxy.create(proxy_config)
pprint(new_proxy.data)
print("Proxy created successfully\n")

# Get proxy configuration from appliance
print("\nGet proxy configuration from appliance:\n ")
proxy_info = proxy.get_by_uri(uri)
pprint(proxy_info.data)

# Delete proxy configured on the appliance
print("\nDelete Proxy")
proxy.delete
print("Proxy deleted successfully")
