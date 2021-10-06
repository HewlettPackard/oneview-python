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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
managed_sans = oneview_client.managed_sans

IMPORTED_SAN = None
INTERNALLY_MANAGED_SAN = None

# You must set the value of the WWN to run the API 300 example
WWN = None

# Get all, with defaults
print("\nGet all Managed SANs")
MANAGED_SANS_ALL = managed_sans.get_all()

if MANAGED_SANS_ALL:
    for managed_san in MANAGED_SANS_ALL:
        print('  Name: {name} - Manager: {deviceManagerName} - Imported:
	 {imported}'.format(**managed_san))
        if managed_san['imported']:
            IMPORTED_SAN = managed_sans.get_by_uri(managed_san["uri"])
        else:
            INTERNALLY_MANAGED_SAN = managed_sans.get_by_uri(managed_san["uri"])

    # Get a Managed SAN by name
    print("\nGet a Managed SAN by name")
    MANAGED_SAN_BY_NAME = managed_sans.get_by_name(managed_san['name'])
    pprint(MANAGED_SAN_BY_NAME.data)

    # Get a Managed SAN by URI
    print("\nGet a Managed SAN by URI")
    MANAGED_SAN_BY_URI = managed_sans.get_by_uri(managed_san['uri'])
    pprint(MANAGED_SAN_BY_URI.data)

    if INTERNALLY_MANAGED_SAN:
        # Update the Managed SAN's publicAttributes
        print("\nUpdate the Internally Managed SAN's publicAttributes")
        PUBLIC_ATTRIBUTES = {
            "publicAttributes": [{
                "name": "MetaSan",
                "value": "Neon SAN",
                "valueType": "String",
                "valueFormat": "None"
            }]
        }
        INTERNALLY_MANAGED_SAN.update(PUBLIC_ATTRIBUTES)
        pprint(INTERNALLY_MANAGED_SAN.data)

        # Update the Managed SAN's POLICY
        print("\nUpdate the Internally Managed SAN's POLICY")
        POLICY = {
            "sanPolicy": {
                "zoningPolicy": "SingleInitiatorAllTargets",
                "zoneNameFormat": "{hostName}_{initiatorWwn}",
                "enableAliasing": True,
                "initiatorNameFormat": "{hostName}_{initiatorWwn}",
                "targetNameFormat": "{storageSystemName}_{targetName}",
                "targetGroupNameFormat": "{storageSystemName}_{targetGroupName}"
            }
        }
        INTERNALLY_MANAGED_SAN.update(POLICY)
        pprint(INTERNALLY_MANAGED_SAN.data)

    if IMPORTED_SAN:
        # Refresh the Managed SAN
        print("\nRefresh the Imported Managed SAN")
        refresh_CONFIG = {
            "refreshState": "RefreshPending"
        }
        IMPORTED_SAN.update(refresh_CONFIG)
        pprint(IMPORTED_SAN.data)

        # Create a SAN ENDPOINTS CSV file
        print("\nCreate a SAN ENDPOINTS CSV file")
        CSV_FILE_RESPONSE = IMPORTED_SAN.create_ENDPOINTS_csv_file()
        pprint(CSV_FILE_RESPONSE)

        # Retrieve the ENDPOINTS for a SAN
        print("\nGet the list of ENDPOINTS in the Imported Managed SAN")
        ENDPOINTS = IMPORTED_SAN.get_ENDPOINTS()
        pprint(ENDPOINTS)

        # Create an unexpected zoning report
        print("\nCreate an unexpected zoning report")
        ISSUES_RESPONSE = IMPORTED_SAN.create_issues_report()
        pprint(ISSUES_RESPONSE)

else:
    print("\nNo Managed SANs found.")

# This method is available for API version 300
if oneview_client.api_version == 300 and WWN is not None:
    # Retrieves an association between the provided WWN and the SAN (if any) on which it resides
    print("\nGet a list of associations between provided WWNs and the SANs on which they reside")
    WWNs = managed_sans.get_WWN(WWN)
    pprint(WWNs)
