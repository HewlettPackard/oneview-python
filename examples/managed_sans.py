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
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
managed_sans = oneview_client.managed_sans

imported_san = None
internally_managed_san = None

# You must set the value of the WWN to run the API 300 example
wwn = None

# Get all, with defaults
print("\nGet all Managed SANs")
managed_sans_all = managed_sans.get_all()

if managed_sans_all:
    for managed_san in managed_sans_all:
        print('  Name: {name} - Manager: {deviceManagerName} - Imported: {imported}'.format(**managed_san))
        if managed_san['imported']:
            imported_san = managed_sans.get_by_uri(managed_san["uri"])
        else:
            internally_managed_san = managed_sans.get_by_uri(managed_san["uri"])

    # Get a Managed SAN by name
    print("\nGet a Managed SAN by name")
    managed_san_by_name = managed_sans.get_by_name(managed_san['name'])
    pprint(managed_san_by_name.data)

    # Get a Managed SAN by URI
    print("\nGet a Managed SAN by URI")
    managed_san_by_uri = managed_sans.get_by_uri(managed_san['uri'])
    pprint(managed_san_by_uri.data)

    if internally_managed_san:
        # Update the Managed SAN's publicAttributes
        print("\nUpdate the Internally Managed SAN's publicAttributes")
        public_attributes = {
            "publicAttributes": [{
                "name": "MetaSan",
                "value": "Neon SAN",
                "valueType": "String",
                "valueFormat": "None"
            }]
        }
        internally_managed_san.update(public_attributes)
        pprint(internally_managed_san.data)

        # Update the Managed SAN's policy
        print("\nUpdate the Internally Managed SAN's policy")
        policy = {
            "sanPolicy": {
                "zoningPolicy": "SingleInitiatorAllTargets",
                "zoneNameFormat": "{hostName}_{initiatorWwn}",
                "enableAliasing": True,
                "initiatorNameFormat": "{hostName}_{initiatorWwn}",
                "targetNameFormat": "{storageSystemName}_{targetName}",
                "targetGroupNameFormat": "{storageSystemName}_{targetGroupName}"
            }
        }
        internally_managed_san.update(policy)
        pprint(internally_managed_san.data)

    if imported_san:
        # Refresh the Managed SAN
        print("\nRefresh the Imported Managed SAN")
        refresh_config = {
            "refreshState": "RefreshPending"
        }
        imported_san.update(refresh_config)
        pprint(imported_san.data)

        # Create a SAN endpoints CSV file
        print("\nCreate a SAN endpoints CSV file")
        csv_file_response = imported_san.create_endpoints_csv_file()
        pprint(csv_file_response)

        # Retrieve the endpoints for a SAN
        print("\nGet the list of endpoints in the Imported Managed SAN")
        endpoints = imported_san.get_endpoints()
        pprint(endpoints)

        # Create an unexpected zoning report
        print("\nCreate an unexpected zoning report")
        issues_response = imported_san.create_issues_report()
        pprint(issues_response)

else:
    print("\nNo Managed SANs found.")

# This method is available for API version 300
if oneview_client.api_version == 300 and wwn is not None:
    # Retrieves an association between the provided WWN and the SAN (if any) on which it resides
    print("\nGet a list of associations between provided WWNs and the SANs on which they reside")
    wwns = managed_sans.get_wwn(wwn)
    pprint(wwns)
