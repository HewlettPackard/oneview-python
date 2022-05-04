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

from hpeOneView.oneview_client import OneViewClient
from hpeOneView.resources.servers.migratable_vc_domains import MigratableVcDomains
from hpeOneView.exceptions import HPEOneViewTaskError
from config_loader import try_load_from_file
from pprint import PrettyPrinter


config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "Administrator",
        "password": ""
    },
    "enclosure_hostname": "172.178.209.32",
    "enclosure_username": "Administrator",
    "enclosure_password": "",
    "vcmUsername": "Administrator",
    "vcmPassword": "",
    "enclosure_group_uri": None
}

pp = PrettyPrinter()

# Try load config from a file (if there is a config file)
print("Loading configuration.")
config = try_load_from_file(config)

# Obtain the master OneView client
print("Setting up OneView client.")
oneview_client = OneViewClient(config)

# Create the dict that VC Migration Manager requires to start the process
migrationInformation = MigratableVcDomains.make_migration_information(config['enclosure_hostname'],
                                                                      config['enclosure_username'],
                                                                      config['enclosure_password'],
                                                                      config['vcmUsername'], config['vcmPassword'],
                                                                      enclosureGroupUri=config['enclosure_group_uri'])

# Start a migration by first creating a compatibility report
print("Create a compatibility report for enclosure '%s'." % migrationInformation['credentials']['oaIpAddress'])
compatibility_report = oneview_client.migratable_vc_domains.test_compatibility(migrationInformation)
print("Complete.  Created a compatibility report for enclosure '%s'.\n  uri = '%s'" %
      (compatibility_report['credentials']['oaIpAddress'], compatibility_report['uri']))

# We got the compatibility report as part of the previous call, but one may need to get it later on
print("Get the '%s' compatibility report." % compatibility_report['credentials']['oaIpAddress'])
compatibility_report = oneview_client.migratable_vc_domains.get_migration_report(compatibility_report['uri'])
print("Complete.  Obtained the compatibility report for '%s'.\n  Here is the compatibility report:" %
      compatibility_report['credentials']['oaIpAddress'])
pp.pprint(compatibility_report)

# One would now resolve all the critical issues and however many lesser severity issues found in the compatibility
# report before continuing.
# Now is the time to initiate the migration
print("Attempting to migrate enclosure '%s'.  The migration state before is '%s'.  This could take a while." %
      (compatibility_report['credentials']['oaIpAddress'], compatibility_report['migrationState']))
try:
    compatibility_report = oneview_client.migratable_vc_domains.migrate(compatibility_report['uri'])
    print("Complete.  Migration state afterward is '%s'." % compatibility_report['migrationState'])
except HPEOneViewTaskError:
    print("Failure.  The enclosure failed to migrate.  Perhaps there was a critical issue that was unresolved before \
migrating?")

# One now may decide to delete the compatibility report if they so choose
print("Deleting the compatibility report for '%s'." % compatibility_report['credentials']['oaIpAddress'])
successful_deletion = oneview_client.migratable_vc_domains.delete(compatibility_report['uri'])
print("Complete.  Deletion was successful for compatibility report '%s'?  %s." %
      (compatibility_report['credentials']['oaIpAddress'], successful_deletion))
