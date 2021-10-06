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
from hpeOneView.exceptions import HPEOneViewException
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<user>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
SCOPEs = oneview_client.SCOPEs
ethernet_networks = oneview_client.ethernet_networks

BULK_ETHERNET = {
    "vlanIdRange": "1-3",
    "purpose": "General",
    "namePrefix": "TestNetwork",
    "smartLink": False,
    "privateNetwork": False,
    "bandwidth": {
        "maximumBandwidth": 10000,
        "typicalBandwidth": 2000
    }
}

# Create bulk ethernet networks
BULKNETWORKURIS = []
print("\nCreate bulk ethernet networks")
ETHERNET_NETS_BULK = ethernet_networks.create_bulk(BULK_ETHERNET)

# Set the URI of existent RESOURCEs to be added/removed to/from the SCOPE
RESOURCE_URI_1 = ethernet_networks.get_by_name('TestNetwork_1').data['uri']
RESOURCE_URI_2 = ethernet_networks.get_by_name('TestNetwork_2').data['uri']
RESOURCE_URI_3 = ethernet_networks.get_by_name('TestNetwork_3').data['uri']

OPTIONS = {
    "name": "SampleScope",
    "description": "Sample Scope description"
}
# Find SCOPE by name
print("\n## Getting the SCOPE by name")
SCOPE = SCOPEs.get_by_name(OPTIONS['name'])
if not SCOPE:
    # Create a SCOPE
    print("\n## Create the SCOPE")
    SCOPE = SCOPEs.create(OPTIONS)
pprint(SCOPE.data)

# Update the name of the SCOPE
print("\n## Update the SCOPE")
RESOURCE = SCOPE.data.copy()
RESOURCE['name'] = "SampleScopeRenamed"
SCOPE.update(RESOURCE)
print("\n## SCOPE updated successfully")

# Find the recently created SCOPE by URI
print("\n## Find SCOPE by URI")
SCOPE_BY_URI = SCOPE.get_by_uri(SCOPE.data['uri'])
pprint(SCOPE_BY_URI.data)

# Get all SCOPEs
print("\n## Get all Scopes")
ALL_SCOPES = SCOPE.get_all()
for elem in ALL_SCOPES:
    print(" - {}".format(elem['name']))

# Update the SCOPE RESOURCE assignments (Available only in API300)
if oneview_client.api_version == 300:
    try:
        print("\n## Update the SCOPE RESOURCE assignments, adding two RESOURCEs")
        OPTIONS = {
            "addedResourceUris": [RESOURCE_URI_1, RESOURCE_URI_2]
        }
        SCOPEs.update_RESOURCE_assignments(SCOPE['uri'], OPTIONS)
        print("  Done.")

        print("\n## Update the SCOPE RESOURCE assignments, adding one RESOURCE and removing another
	 previously added")
        OPTIONS = {
            "removedResourceUris": [RESOURCE_URI_1],
            "addedResourceUris": [RESOURCE_URI_3]
        }
        SCOPEs.update_RESOURCE_assignments(SCOPE['uri'], OPTIONS)
        print("  Done.")
    except HPEOneViewException as e:
        print(e.msg)

# Updates the name and description of a SCOPE assigning and unassigning ethernet RESOURCEs
# (Available only from API500)
if oneview_client.api_version >= 500:
    try:
        print("\n## Patch the SCOPE adding two RESOURCE uris")
        EDITED_SCOPE = SCOPE.patch('add', '/addedResourceUris/-', RESOURCE_URI_1)
        pprint(EDITED_SCOPE.data)

        EDITED_SCOPE = SCOPE.patch('add', '/addedResourceUris/-', RESOURCE_URI_2)
        pprint(EDITED_SCOPE.data)

        # Find the recently created SCOPE by name
        print("\n## Find SCOPE by name")
        SCOPE_BY_NAME = SCOPE.get_by_name(SCOPE.data['name'])
        pprint(SCOPE_BY_NAME.data)

        # Get the RESOURCE assignments of SCOPE
        print("\n## Find RESOURCE assignments to SCOPE")
        SCOPE_ASSIGNED_RESOURCE = SCOPEs.get_SCOPE_RESOURCE(RESOURCE_URI_1)
        pprint(SCOPE_ASSIGNED_RESOURCE.data)

        print("\n## Patch the SCOPE removing one of the previously added RESOURCE uris")
        RESOURCE_LIST = [RESOURCE_URI_1]
        EDITED_SCOPE = SCOPE.patch('replace', '/removedResourceUris', RESOURCE_LIST)
        pprint(EDITED_SCOPE.data)

        print("\n## Patch the SCOPE updating the name")
        UPDATE_NAME = "MySampleScope"
        EDITED_SCOPE = SCOPE.patch('replace', '/name', UPDATE_NAME)
        pprint(EDITED_SCOPE.data)

        print("\n## Patch the SCOPE updating the description")
        UPDATE_DESCRIPTION = "Modified SCOPE description"
        EDITED_SCOPE = SCOPE.patch('replace', '/description', UPDATE_DESCRIPTION)
        pprint(EDITED_SCOPE.data)
    except HPEOneViewException as e:
        print(e.msg)

# Get the RESOURCE assignments of SCOPE when unassigned
print("\n## Find RESOURCE assignments to SCOPE when RESOURCE unassigned")
SCOPE_ASSIGNED_RESOURCE = SCOPEs.get_SCOPE_RESOURCE(RESOURCE_URI_1)
pprint(SCOPE_ASSIGNED_RESOURCE.data)

# Delete the SCOPE
SCOPE.delete()
print("\n## Scope deleted successfully.")
