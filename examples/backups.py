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
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a new appliance backup
print("\n## Create a new appliance backup")
backup_details = oneview_client.backups.create()
pprint(backup_details)

filename = backup_details['id']

# Download the backup archive
print("\n## Download the previously created backup archive")
response = oneview_client.backups.download(backup_details['downloadUri'], filename)
print(response)

# Upload the backup archive
print("\n## Upload the previously downloaded backup archive")
backup_details = oneview_client.backups.upload(filename)
pprint(backup_details)

# Get by URI
print("\n## Find recently created backup by URI")
backup_by_uri = oneview_client.backups.get(backup_details['uri'])
pprint(backup_by_uri)

# Get all backups
print("\n## Get all backups")
backups = oneview_client.backups.get_all()
pprint(backups)

# Get the details of the backup configuration
print("\n## Get the details of the backup configuration for the remote server and automatic backup schedule")
config = oneview_client.backups.get_config()
pprint(config)

# Update the backup configuration
try:
    print("\n## Update the backup configuration")
    config['scheduleTime'] = '23:00'
    updated_config = oneview_client.backups.update_config(config)
    pprint(updated_config)
except HPOneViewException as e:
    print(e.msg)

# Save the backup file to a previously-configured remote location
try:
    print("\n## Save the backup file to a previously-configured remote location")
    backup_details = oneview_client.backups.update_remote_archive(backup_details['saveUri'])
    pprint(backup_details)
except HPOneViewException as e:
    print(e.msg)
