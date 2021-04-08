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

import os
from pprint import pprint
from hpeOneView.oneview_client import OneViewClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config.json')

oneview_client = OneViewClient.from_json_file(EXAMPLE_CONFIG_FILE)
image_streamer_client = oneview_client.create_image_streamer_client()
deployment_plans = image_streamer_client.deployment_plans
build_plans = image_streamer_client.build_plans

# To run this example set a valid Build Plan URI
deployment_plan_information = {
    "name": "Demo Deployment Plan",
    "description": "",
    "hpProvided": "false",
    "oeBuildPlanURI": "/rest/build-plans/134b7e3f-4305-47c4-8d15-44d265697bf0",
}

# Get all build plans
all_build_plans = build_plans.get_all(filter='oeBuildPlanType=capture')
bp_uri = all_build_plans[0]['uri']

# set the "oeBuildPlanURI" in deployment plan payload
deployment_plan_information['oeBuildPlanURI'] = bp_uri

if oneview_client.api_version >= 500:
    deployment_plan_information["type"] = "OEDeploymentPlanV5"

# Create a Deployment Plan
print("Create a Deployment Plan")
deployment_plan_created = deployment_plans.create(deployment_plan_information)
pprint(deployment_plan_created.data)

# Update the Deployment Plan
print("\nUpdate the Deployment Plan")
deployment_plan_data = deployment_plan_created.data.copy()
deployment_plan_data["name"] = "Demo Deployment Plan - Renamed"
deployment_plan_created.update(deployment_plan_data)
pprint(deployment_plan_created.data)

# Get the Deployment Plan by URI
print("\nGet the Deployment Plan by URI")
deployment_plan_by_uri = deployment_plans.get_by_uri(deployment_plan_created.data['uri'])
pprint(deployment_plan_by_uri.data)

# Get the Deployment Plan by name
print("\nGet the Deployment Plan by name")
deployment_plan_by_name = deployment_plans.get_by_name(deployment_plan_created.data['name'])
pprint(deployment_plan_by_name.data)

# Get all Deployment Plans
print("\nGet all Deployment Plans")
deployment_plans_all = deployment_plans.get_all()
for deployment_plan in deployment_plans_all:
    print(deployment_plan['name'])

if oneview_client.api_version >= 500:
    # Get the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}
    print("\nGet the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}")
    deployment_usedby = deployment_plan_created.get_usedby()
    pprint(deployment_usedby)

if oneview_client.api_version >= 600:
    # Get the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}
    print("\nGet the OSDP of a Deployment Plan ")
    deployment_osdp = deployment_plan_created.get_osdp()
    pprint(deployment_osdp)

# Delete the Deployment Plan
print("\nDelete the Deployment Plan")
deployment_plan_created.delete()
print("Deployment Plan deleted successfully")
