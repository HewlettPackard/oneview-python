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
from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# Create a new appliance backup
print("\n## Create a new appliance backup")
backup_details = oneview_client.backups.create()
pprint(backup_details)

FILENAME = backup_details['id']

# Download the backup archive
print("\n## Download the previously created backup archive")
response = oneview_client.backups.download(backup_details['downloadUri'], FILENAME)
print(response)

# Upload the backup archive
print("\n## Upload the previously downloaded backup archive")
backup_details = oneview_client.backups.upload(FILENAME)
pprint(backup_details)

# Get by URI
print("\n## Find recently created backup by URI")
backup_by_uri = oneview_client.backups.get(backup_details['uri'])
pprint(backup_by_uri)

# Get all backups
print("\n## Get all backups")
backups = oneview_client.backups.get_all()
pprint(backups)

# Get the details of the backup CONFIGuration
print("\n## Get the details of the backup CONFIGuration for the remote server and automatic backup
	 schedule")
CONFIG = oneview_client.backups.get_CONFIG()
pprint(CONFIG)

# Update the backup CONFIGuration
try:
    print("\n## Update the backup CONFIGuration")
    CONFIG['scheduleTime'] = '23:00'
    updated_CONFIG = oneview_client.backups.update_CONFIG(CONFIG)
    pprint(updated_CONFIG)
except HPEOneViewException as e:
    print(e.msg)

# Save the backup file to a previously-CONFIGured remote location
try:
    print("\n## Save the backup file to a previously-CONFIGured remote location")
    backup_details = oneview_client.backups.update_remote_archive(backup_details['saveUri'])
    pprint(backup_details)
except HPEOneViewException as e:
    print(e.msg)
