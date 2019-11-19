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

import os
from pprint import pprint
from hpOneView.oneview_client import OneViewClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config.json')

oneview_client = OneViewClient.from_json_file(EXAMPLE_CONFIG_FILE)

image_streamer_client = oneview_client.create_image_streamer_client()

# To run this example set a valid Build Plan URI
deployment_plan_information = {
    "name": "Demo Deployment Plan",
    "description": "",
    "hpProvided": "false",
    "oeBuildPlanURI": "/rest/build-plans/1beb9333-66a8-48d5-82b6-1bda1a81582a",
}

if oneview_client.api_version >= 500:
    deployment_plan_information["type"] = "OEDeploymentPlanV5"

# Create a Deployment Plan
print("Create a Deployment Plan")
deployment_plan_created = image_streamer_client.deployment_plans.create(deployment_plan_information)
pprint(deployment_plan_created)

# Update the Deployment Plan
print("\nUpdate the Deployment Plan")
deployment_plan_created["name"] = "Demo Deployment Plan - Renamed"
deployment_plan_updated = image_streamer_client.deployment_plans.update(deployment_plan_created)
pprint(deployment_plan_updated)

# Get the Deployment Plan by URI
print("\nGet the Deployment Plan by URI")
deployment_plan_by_uri = image_streamer_client.deployment_plans.get(deployment_plan_created['uri'])
pprint(deployment_plan_by_uri)

# Get the Deployment Plan by name
print("\nGet the Deployment Plan by name")
deployment_plan_by_name = image_streamer_client.deployment_plans.get_by('name', deployment_plan_updated['name'])
pprint(deployment_plan_by_name)

# Get all Deployment Plans
print("\nGet all Deployment Plans")
deployment_plans = image_streamer_client.deployment_plans.get_all()
for deployment_plan in deployment_plans:
    print(deployment_plan['name'])

if oneview_client.api_version >= 500:
    # Get the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}
    print("\nGet the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}")
    deployment_usedby = image_streamer_client.deployment_plans.get_usedby(deployment_plan_created['id'])
    pprint(deployment_usedby)

if oneview_client.api_version >= 600:
    # Get the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}
    print("\nGet the OSDP of a Deployment Plan ")
    deployment_osdp = image_streamer_client.deployment_plans.get_osdp(deployment_plan_created['id'])
    pprint(deployment_osdp)

# Delete the Deployment Plan
print("\nDelete the Deployment Plan")
image_streamer_client.deployment_plans.delete(deployment_plan_by_uri)
print("Deployment Plan deleted successfully")
