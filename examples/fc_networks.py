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
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
    "linkStabilityTime": 30,
}

# Scope name to perform the patch operation
SCOPE_NAME = "test_SCOPE"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
FC_NETWORKs = oneview_client.FC_NETWORKs
SCOPEs = oneview_client.SCOPEs

# Get all, with defaults
print("\nGet all fc-networks")
FC_NETS = FC_NETWORKs.get_all()
pprint(FC_NETS)

# Get the first 10 records
print("\nGet the first ten fc-networks")
FC_NETS_LIMITED = FC_NETWORKs.get_all(0, 10)
pprint(FC_NETS_LIMITED)

# Filter by name
print("\nGet all fc-networks filtering by name")
FC_NETS_FILTERED = FC_NETWORKs.get_all(filter="\"'name'='Updated FC'\"")
pprint(FC_NETS_FILTERED)

# Get all sorting by name descending
print("\nGet all fc-networks sorting by name")
FC_NETS_SORTED = FC_NETWORKs.get_all(sort='name:descending')
pprint(FC_NETS_SORTED)

# Find recently created network by name
print("\nGet FC Network by name")
FC_NETWORK = FC_NETWORKs.get_by_name(OPTIONS['name'])

if FC_NETWORK:
    print("\nFound fc-network by name: '%s'.\n  uri = '%s'" % (FC_NETWORK.data['name'],
	 FC_NETWORK.data['uri']))
else:
    # Create a FcNetWork with the OPTIONS provided
    FC_NETWORK = FC_NETWORKs.create(data=OPTIONS)
    print("\nCreated a fc-network with name: '%s'.\n  uri = '%s'" % (FC_NETWORK.data['name'],
	 FC_NETWORK.data['uri']))

# Get by uri
print("\nGet a fc-network by uri")
FC_NETS_BY_URI = FC_NETWORKs.get_by_uri(FC_NETWORK.data['uri'])
pprint(FC_NETS_BY_URI.data)

# Update autoLoginRedistribution from recently created network
DATA_TO_UPDATE = {'autoLoginRedistribution': False,
                  'name': 'Updated FC'}
FC_NETWORK.update(data=DATA_TO_UPDATE)
print("\nUpdated fc-network '%s' successfully.\n  uri = '%s'" % (FC_NETWORK.data['name'],
	 FC_NETWORK.data['uri']))
print("  with attribute {'autoLoginRedistribution': %s}" % FC_NETWORK.data['autoLoginRedistribution'])

# Adds fc-network to SCOPE defined only for V300 and V500
if SCOPE_NAME and 300 <= oneview_client.api_version <= 500:
    print("\nGet SCOPE then add the network to it")
    SCOPE = SCOPEs.get_by_name(SCOPE_NAME)
    print(SCOPE['uri'])
    try:
        FC_WITH_SCOPE = FC_NETWORK.patch('replace',
                                         '/SCOPEUris',
                                         [SCOPE.data['uri']])
        pprint(FC_WITH_SCOPE)
    except HPEOneViewException as e:
        print(e)

# Delete the created network
FC_NETWORK.delete()
print("\nSuccessfully deleted fc-network")

# Creates bulk fc-networks
for i in range(4):
    FC_NETWORK_body = OPTIONS.copy()
    FC_NETWORK_body['name'] = "OneViewSDK Test FC Network" + str(i)
    bulk_FC_NETWORK = FC_NETWORKs.create(data=FC_NETWORK_body)
    print("\nCreated bulk fc-networks with name: '%s'.\n  uri = '%s'" %
	 (bulk_FC_NETWORK.data['name'], bulk_FC_NETWORK.data['uri']))

# Delete bulk fcnetworks
if oneview_client.api_version >= 1600:
    BULK_NETWORK_URIS = []
    for i in range(4):
        FC_NETWORK_name = "OneViewSDK Test FC Network" + str(i)
        bulk_FC_NETWORK = FC_NETWORKs.get_by_name(FC_NETWORK_name)
        BULK_NETWORK_URIS.append(bulk_FC_NETWORK.data['uri'])
    print("\nDelete bulk fc-networks")
    OPTIONS_BULK_DELETE = {"networkUris": BULK_NETWORK_URIS}
    FC_NETWORK.delete_bulk(OPTIONS_BULK_DELETE)
    print("Successfully deleted bulk fc-networks")

# Automation tasks for FC networks
FC_NETWORK_body['name'] = "FC_fabric_nw"
FC_NETWORK = FC_NETWORKs.create(data=FC_NETWORK_body)
print("\nCreated fc-networks with name: '%s'.\n  uri = '%s'" % (FC_NETWORK.data['name'],
	 FC_NETWORK.data['uri']))
