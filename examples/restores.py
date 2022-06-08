# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
restores = oneview_client.restores
# Start a restore
print("Starting a restore")
print("\n## Create a new appliance backup")
backup_details = oneview_client.backups.create()
# A uri for a backup to restore must be set to run this example
uri_of_backup_to_restore = backup_details['uri']
options = {
    "uriOfBackupToRestore": uri_of_backup_to_restore
}
restore = restores.restore(options)
pprint(restore.data)

# Get all restores
print("Get all Restores")
restore_all = restores.get_all()
for restore in restore_all:
    print('  - {}'.format(restore['hostName']))

# Get by hostname
print("\nGet a Restore by hostName equals to '{}'".format(restore['hostName']))
restore_by_host_name = restores.get_by("hostName", restore['hostName'])
pprint(restore_by_host_name)

# Get by URI
print("\nGet a Restore by URI")
restore_by_uri = restores.get_by_uri(restore['uri'])
pprint(restore_by_uri.data)

# Get Restore Failure
print("\nRetrieving Restore Failure")
failures = restores.get_failure()
pprint(failures)
