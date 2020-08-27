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
from hpeOneView.oneview_client import OneViewClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config.json')

oneview_client = OneViewClient.from_json_file(EXAMPLE_CONFIG_FILE)

image_streamer_client = oneview_client.create_image_streamer_client()

build_plan_information = {
    "name": "Demo Build Plan",
    "oeBuildPlanType": "deploy"
}

# Create a Build Plan
print("Create an OS Build Plan")
build_plan_created = image_streamer_client.build_plans.create(build_plan_information)
pprint(build_plan_created)

# Update the Build Plan
print("\nUpdate the OS Build Plan")
build_plan_created["name"] = "Demo Build Plan - Renamed"
build_plan_updated = image_streamer_client.build_plans.update(build_plan_created)
pprint(build_plan_updated)

# Get the Build Plan by URI
print("\nGet the OS Build Plan by URI")
build_plan_by_uri = image_streamer_client.build_plans.get(build_plan_updated['uri'])
pprint(build_plan_by_uri)

# Get all Build Plans
print("\nGet all OS Build Plans")
build_plans = image_streamer_client.build_plans.get_all()
for build_plan in build_plans:
    print(build_plan['name'])

# Delete the Build Plan
print("\nDelete the OS Build Plan")
image_streamer_client.build_plans.delete(build_plan_by_uri)
print("OS Build Plan deleted successfully")
