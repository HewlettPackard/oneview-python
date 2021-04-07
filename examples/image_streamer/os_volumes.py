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

os_volumes_information = {
    "name": "OSVolume-52",
}
destination_archive_path = './archive_log.txt'

# Get all OS Volumes
print("\nGet all OS Volumes")
os_volumes = image_streamer_client.os_volumes.get_all()
for os_volume in os_volumes:
    pprint(os_volume)

# Get the OS Volume id
if os_volumes:
    os_volumes_information['id'] = os_volumes[0]['uri'].split('/')[-1]

# Get the OS Volume by ID
print("\nGet the OS Volumes by ID")
os_volume = image_streamer_client.os_volumes.get(os_volumes_information['id'])
pprint(os_volume)

# Get the OS Volume by Name
print("\nGet the OS Volumes by Name")
os_volume = image_streamer_client.os_volumes.get_by_name(os_volumes_information['name'])
pprint(os_volume)

# Get storage details (available only with API version 600 and above)
print("Get storage details")
storage = image_streamer_client.os_volumes.get_storage(os_volumes_information['id'])
pprint(storage)

# Retrieve archived logs of the OS Volume
print("Retrieve archived logs of the OS Volume")
if image_streamer_client.os_volumes.download_archive(os_volume['id'], destination_archive_path):
    print("  File downloaded successfully.")
else:
    print("  Error downloading the file.")
