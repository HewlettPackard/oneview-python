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
from config_loader import try_load_from_file

# To run this example fill the ip and the credentials below or use a configuration file
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
    "linkStabilityTime": 30,
}

# Scope name to perform the patch operation
scope_name = "test_scope"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
fc_networks = oneview_client.fc_networks

# Get all, with defaults
print("\nGet all fc-networks")
fc_nets = fc_networks.get_all()
pprint(fc_nets)

# Get the first 10 records
print("\nGet the first ten fc-networks")
fc_nets_limited = fc_networks.get_all(0, 10)
pprint(fc_nets_limited)

# Filter by name
print("\nGet all fc-networks filtering by name")
fc_nets_filtered = fc_networks.get_all(filter="\"'name'='Updated FC'\"")
pprint(fc_nets_filtered)

# Get all sorting by name descending
print("\nGet all fc-networks sorting by name")
fc_nets_sorted = fc_networks.get_all(sort='name:descending')
pprint(fc_nets_sorted)

# Find recently created network by name
print("\nGet FC Network by name")
fc_network = fc_networks.get_by_name(options['name'])

if fc_network:
    print("\nFound fc-network by name: '%s'.\n  uri = '%s'" % (fc_network.data['name'], fc_network.data['uri']))
else:
    # Create a FcNetWork with the options provided
    fc_network = fc_networks.create(data=options)
    print("\nCreated a fc-network with name: '%s'.\n  uri = '%s'" % (fc_network.data['name'], fc_network.data['uri']))

# Get by uri
print("\nGet a fc-network by uri")
fc_nets_by_uri = fc_networks.get_by_uri(fc_network.data['uri'])
pprint(fc_nets_by_uri.data)

# Update autoLoginRedistribution from recently created network
data_to_update = {'autoLoginRedistribution': False,
                  'name': 'Updated FC'}
fc_network.update(data=data_to_update)
print("\nUpdated fc-network '%s' successfully.\n  uri = '%s'" % (fc_network.data['name'], fc_network.data['uri']))
print("  with attribute {'autoLoginRedistribution': %s}" % fc_network.data['autoLoginRedistribution'])

# Adds fc-network to scope defined only for V300 and V500
if scope_name and 300 <= oneview_client.api_version <= 500:
    print("\nGet scope then add the network to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    print(scope['uri'])
    try:
        fc_with_scope = fc_network.patch('replace',
                                         '/scopeUris',
                                         [scope.data['uri']])
        pprint(fc_with_scope)
    except HPEOneViewException as e:
        print(e)

# Delete the created network
fc_network.delete()
print("\nSuccessfully deleted fc-network")

# Creates bulk fc-networks
for i in range(2):
    options = {
        "name": "OneViewSDK Test FC Network" + str(i),
        "connectionTemplateUri": None,
        "autoLoginRedistribution": True,
        "fabricType": "FabricAttach",
        "linkStabilityTime": 30,
    }
    bulk_fc_network = fc_networks.create(data=options)
    print("\nCreated bulk fc-networks with name: '%s'.\n  uri = '%s'" % (bulk_fc_network.data['name'], bulk_fc_network.data['uri']))

# Delete bulk fcnetworks
if oneview_client.api_version >= 1600:
    bulk_network_uris = []
    for i in range(2):
        fc_network_name = "OneViewSDK Test FC Network" + str(i)
        bulk_fc_network = fc_networks.get_by_name(fc_network_name)
        bulk_network_uris.append(bulk_fc_network.data['uri'])
    print("\nDelete bulk fcnetworks")
    options_bulk_delete = {"networkUris": bulk_network_uris}
    fc_network.delete_bulk(options_bulk_delete)
    print("Successfully deleted bulk fcnetworks")
