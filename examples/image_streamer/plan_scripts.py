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

plan_script_information = {
    "description": "Description of this plan script",
    "name": "Demo Plan Script",
    "hpProvided": False,
    "planType": "deploy",
    "content": 'echo "test script"'
}

# plan script which is used by buils plans and is readonly
plan_script_id_readyonly = "590746df-7354-42aa-8887-e1ea122f7ed6"

# Create a Plan Script
print("Create a Plan Script")
plan_script = image_streamer_client.plan_scripts.create(plan_script_information)
pprint(plan_script)
print("***** done *****\n")

# Update the Plan Script
print("Update the Plan Script")
plan_script["description"] = "New description"
plan_script["content"] = 'echo "Commands"\necho "Command 2"'
plan_script = image_streamer_client.plan_scripts.update(plan_script)
pprint(plan_script)
print("***** done *****\n")

# Get the Plan Script by URI
print("Get the Plan Script by URI")
plan_script = image_streamer_client.plan_scripts.get(plan_script['uri'])
pprint(plan_script)
print("***** done *****\n")

# Retrieve the modified contents of the Plan Script
print("Retrieves the modified contents of the Plan Script")
differences = image_streamer_client.plan_scripts.retrieve_differences(plan_script['uri'], "Script content")
pprint(differences)
print("***** done *****\n")

# Get all Plan Scripts
print("Get all Plan Scripts")
plan_scripts = image_streamer_client.plan_scripts.get_all()
for plan_script_item in plan_scripts:
    print(plan_script_item['name'])
print("***** done *****\n")

# Get used by and read only
print("Gets builds plans which uses a particular read only plan script")
build_plans = image_streamer_client.plan_scripts.get_usedby_and_readonly(plan_script_id_readyonly)
for build_plan_item in build_plans:
    print(build_plan_item["name"])
print("**********done***********\n")

# Delete the Plan Script
print("Delete the Plan Script")
image_streamer_client.plan_scripts.delete(plan_script)
print("Plan Script deleted successfully")
