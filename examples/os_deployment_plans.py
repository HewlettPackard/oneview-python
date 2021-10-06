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
        "userName": "<user>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
os_deployment_PLANS = oneview_client.os_deployment_PLANS

print("\nGet OS Deployment Plans by Filter:")
PLANS = os_deployment_PLANS.get_by('deploymentType', 'I3S')
pprint(PLANS)

print("\nGet the OS Deployment Plan by Name:")
OS_DEPLOYMENT_PLAN = os_deployment_PLANS.get_by('name', 'Deployment Plan')
pprint(OS_DEPLOYMENT_PLAN)

print("\nGet all OS Deployment Plans:")
OS_DEPLOYMENT_PLANS_ALL = os_deployment_PLANS.get_all()
pprint(OS_DEPLOYMENT_PLANS_ALL)
