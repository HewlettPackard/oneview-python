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
from copy import deepcopy

# To run this example fill the ip and the credentials below or use a CONFIGuration file
CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

OPTIONS = {
    "name": "OneViewSDK Test FCoE Network",
    "vlanId": "201",
    "connectionTemplateUri": None,
}

# Scope name to perform the patch operation
SCOPE_NAME = ""

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
FCOE_NETWORKs = oneview_client.FCOE_NETWORKs
SCOPEs = oneview_client.SCOPEs

# Get all, with defaults
print("\nGet all fcoe-networks")
FCOE_NETS = FCOE_NETWORKs.get_all()
pprint(FCOE_NETS)

# Filter by name
print("\nGet all fcoe-networks filtering by name")
FCOE_NETS_FILTERED = FCOE_NETWORKs.get_all(filter="\"'name'='OneViewSDK Test FCoE Network'\"")
pprint(FCOE_NETS_FILTERED)

# Get all sorting by name descending
print("\nGet all fcoe-networks sorting by name")
FCOE_NETS_SORTED = FCOE_NETWORKs.get_all(sort='name:descending')
pprint(FCOE_NETS_SORTED)

# Get the first 10 records
print("\nGet the first ten fcoe-networks")
FCOE_NETS_LIMITED = FCOE_NETWORKs.get_all(0, 10)
pprint(FCOE_NETS_LIMITED)

# Get by name
FCOE_NETWORK = FCOE_NETWORKs.get_by_name(OPTIONS['name'])
if FCOE_NETWORK:
    print("\nGot fcoe-network by name uri={}".format(FCOE_NETWORK.data['uri']))
else:
    # Create a FC Network
    FCOE_NETWORK = FCOE_NETWORKs.create(OPTIONS)
    print("\nCreated fcoe-network '%s' successfully.\n  uri = '%s'" % (FCOE_NETWORK.data['name'],
	 FCOE_NETWORK.data['uri']))

# Update autoLoginRedistribution from recently created network
RESOURCE = deepcopy(FCOE_NETWORK.data)
RESOURCE['status'] = 'Warning'
RESOURCE['name'] = "{}-Renamed".format(OPTIONS["name"])
FCOE_NETWORK_UPDATED = FCOE_NETWORK.update(RESOURCE)
print("\nUpdated fcoe-network '%s' successfully.\n  uri = '%s'" % (FCOE_NETWORK_UPDATED.data['name'], FCOE_NETWORK_UPDATED.data['uri']))
print("  with attribute {'status': %s}" % FCOE_NETWORK_UPDATED.data['status'])

# Get by Uri
print("\nGet a fcoe-network by uri")
FCOE_NETS_BY_URI = FCOE_NETWORKs.get_by_uri(FCOE_NETWORK.data['uri'])
pprint(FCOE_NETS_BY_URI.data)

# Adds FCOE network to SCOPE defined only for V300 and V500
if SCOPE_NAME and 300 <= oneview_client.api_version <= 500:
    print("\nGet SCOPE then add the network to it")
    SCOPE = SCOPEs.get_by_name(SCOPE_NAME)
    FCOE_WITH_SCOPE = FCOE_NETWORK.patch('replace',
                                         '/SCOPEUris',
                                         [SCOPE.data['uri']])
    pprint(FCOE_WITH_SCOPE.data)

# Delete the created network
FCOE_NETWORK.delete()
print("\nSuccessfully deleted fcoe-network")

# Creates bulk fcoe-networks
for i in range(4):
    OPTIONS = {
        "name": "OneViewSDK Test FCoE Network" + str(i),
        "vlanId": int("201") + int(i),
        "connectionTemplateUri": None,
    }
    bulk_FCOE_NETWORK = FCOE_NETWORKs.create(OPTIONS)
    print("\nCreated bulk fcoe-networks with name: '%s'.\n  uri = '%s'" %
	 (bulk_FCOE_NETWORK.data['name'], bulk_FCOE_NETWORK.data['uri']))

# Delete bulk fcoe-networks
if oneview_client.api_version >= 1600:
    BULK_NETWORK_URIS = []
    for i in range(4):
        FCOE_NETWORK_name = "OneViewSDK Test FCoE Network" + str(i)
        bulk_FCOE_NETWORK = FCOE_NETWORKs.get_by_name(FCOE_NETWORK_name)
        BULK_NETWORK_URIS.append(bulk_FCOE_NETWORK.data['uri'])
    print("\nDelete bulk fcoe-networks")
    OPTIONS_BULK_DELETE = {"networkUris": BULK_NETWORK_URIS}
    FCOE_NETWORK.delete_bulk(OPTIONS_BULK_DELETE)
    print("Successfully deleted bulk fcoe-networks")

# Create a FCoE Network for automation
OPTIONS['name'] = "Test_fcoeNetwork"
FCOE_NETWORK = FCOE_NETWORKs.create(OPTIONS)
print("\nCreated fcoe-network '%s' successfully.\n  uri = '%s'" % (FCOE_NETWORK.data['name'],
	 FCOE_NETWORK.data['uri']))
