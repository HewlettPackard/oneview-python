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
from config_loader import try_load_from_file

CONFIG = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)

# Create a new appliance backup
print("\n## Create a new appliance backup")
BACKUP_DETAILS = ONEVIEW_CLIENT.backups.create()
pprint(BACKUP_DETAILS)

FILENAME = BACKUP_DETAILS['id']

# Download the backup archive
print("\n## Download the previously created backup archive")
RESPONSE = ONEVIEW_CLIENT.backups.download(BACKUP_DETAILS['downloadUri'], FILENAME)
print(RESPONSE)

# Upload the backup archive
print("\n## Upload the previously downloaded backup archive")
BACKUP_DETAILS = ONEVIEW_CLIENT.backups.upload(FILENAME)
pprint(BACKUP_DETAILS)

# Get by URI
print("\n## Find recently created backup by URI")
BACKUP_BY_URI = ONEVIEW_CLIENT.backups.get(BACKUP_DETAILS['uri'])
pprint(BACKUP_BY_URI)

# Get all backups
print("\n## Get all backups")
BACKUPS = ONEVIEW_CLIENT.backups.get_all()
pprint(BACKUPS)

# Get the details of the backup CONFIGuration
print("\nGet the details of the backup configuration for the remote server and automatic backup\
	 schedule")
CONFIG = ONEVIEW_CLIENT.backups.get_config()
pprint(CONFIG)

# Update the backup CONFIGuration
try:
    print("\n## Update the backup CONFIGuration")
    CONFIG['scheduleTime'] = '23:00'
    UPDATED_CONFIG = ONEVIEW_CLIENT.backups.update_config(CONFIG)
    pprint(UPDATED_CONFIG)
except HPEOneViewException as err:
    print(err.msg)

# Save the backup file to a previously-CONFIGured remote location
try:
    print("\n## Save the backup file to a previously-CONFIGured remote location")
    BACKUP_DETAILS = ONEVIEW_CLIENT.backups.update_remote_archive(BACKUP_DETAILS['saveUri'])
    pprint(BACKUP_DETAILS)
except HPEOneViewException as err:
    print(err.msg)
