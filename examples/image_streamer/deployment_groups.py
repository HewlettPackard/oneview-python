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

deployment_groups_information = {
    "name": "OSS",
    "id": "57f2d803-9c11-4f9a-bc02-71804a0fcc3e"
}


# Get all Deployment Groups
print("\nGet all Deployment Groups")
deployment_groups = image_streamer_client.deployment_groups.get_all()
for deployment_group in deployment_groups:
    pprint(deployment_group)


# Get the Deployment Group by ID
print("\nGet the Deployment Group by ID")
response = image_streamer_client.deployment_groups.get(deployment_groups_information['id'])
pprint(response)


# Get the Deployment Group by Name
print("\nGet the Deployment Group by Name")
response = image_streamer_client.deployment_groups.get_by_name(deployment_groups_information['name'])
pprint(response)
