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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
RESTOREs = oneview_client.RESTOREs

# A uri for a backup to RESTORE must be set to run this example
URI_OF_BACKUP_TO_RESTORE = "/rest/backups/example_backup_2017-04-25_195515"

# Start a RESTORE
print("Starting a RESTORE")
OPTIONS = {
    "uriOfBackupToRestore": URI_OF_BACKUP_TO_RESTORE
}
RESTORE = RESTOREs.RESTORE(OPTIONS)
pprint(RESTORE.data)

# Get all RESTOREs
print("Get all Restores")
RESTORE_ALL = RESTOREs.get_all()
for restr in RESTORE_ALL:
    print('  - {}'.format(restr['hostName']))

# Get by hostname
print("\nGet a Restore by hostName equals to '{}'".format(RESTORE['hostName']))
RESTORE_BY_HOST_NAME = RESTOREs.get_by("hostName", RESTORE['hostName'])
pprint(RESTORE_BY_HOST_NAME)

# Get by URI
print("\nGet a Restore by URI")
RESTORE_BY_URI = RESTOREs.get_by_uri(RESTORE['uri'])
pprint(RESTORE_BY_URI.data)

# Get Restore Failure
print("\nRetrieving Restore Failure")
FAILURES = RESTOREs.get_failure()
pprint(FAILURES)
