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
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<user>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
os_deployment_plans = oneview_client.os_deployment_plans

print("\nGet OS Deployment Plans by Filter:")
plans = os_deployment_plans.get_by('deploymentType', 'I3S')
pprint(plans)

print("\nGet the OS Deployment Plan by Name:")
os_deployment_plan = os_deployment_plans.get_by('name', 'Deployment Plan')
pprint(os_deployment_plan)

print("\nGet all OS Deployment Plans:")
os_deployment_plans_all = os_deployment_plans.get_all()
pprint(os_deployment_plans_all)
