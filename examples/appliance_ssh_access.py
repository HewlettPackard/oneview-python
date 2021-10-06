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

OPTIONS = {
    "allowSshAccess": False
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
ssh_access = oneview_client.appliance_ssh_access

# Get the SSH access CONFIGuration for the appliance.
SSH_CONFIG = ssh_access.get_all()
print("\nGot SSH access CONFIGuration successfully!")
pprint(SSH_CONFIG.data)

# Set the SSH access CONFIGuration for the appliance as False.
SSH_CONFIG = SSH_CONFIG.update(data=OPTIONS)
print("\nUpdated SSH access CONFIGuration successfully!")

# Set the SSH access CONFIGuration for the appliance as True.
OPTIONS["allowSshAccess"] = True
SSH_CONFIG = SSH_CONFIG.update(data=OPTIONS)
print("\nUpdated SSH access CONFIGuration successfully!")
