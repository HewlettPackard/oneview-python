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

options = {
    "allowSshAccess": False
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
ssh_access = oneview_client.appliance_ssh_access

# Get the SSH access configuration for the appliance.
ssh_config = ssh_access.get_all()
print("\nGot SSH access configuration successfully!")
pprint(ssh_config.data)

# Set the SSH access configuration for the appliance as False.
ssh_config = ssh_config.update(data=options)
print("\nUpdated SSH access configuration successfully!")

# Set the SSH access configuration for the appliance as True.
options["allowSshAccess"] = True
ssh_config = ssh_config.update(data=options)
print("\nUpdated SSH access configuration successfully!")
