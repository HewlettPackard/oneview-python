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
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": "123456"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# A Uri for a backup to restore must be set to run this example
uri_of_backup_to_restore = "/rest/backups/example_backup_2017-04-25_195515"

# Start a restore
print("Starting a restore")
options = {
    "uriOfBackupToRestore": uri_of_backup_to_restore
}
restore = oneview_client.restores.restore(options)
pprint(restore)

# Get all restores
print("Get all Restores")
restores = oneview_client.restores.get_all()
pprint(restores)

# Get by
print("\nGet a Restore by hostName equals to '{}'".format(restore['hostName']))
restore_by_host_name = oneview_client.restores.get_by("hostName", restore['hostName'])
pprint(restore_by_host_name)

# Get by URI
print("\nGet a Restore by URI")
restore_by_uri = oneview_client.restores.get(restore['uri'])
pprint(restore_by_uri)

# Get Restore Failure
print("\nRetrieving Restore Failure")
failures = oneview_client.restores.get_failure()
pprint(failures)
