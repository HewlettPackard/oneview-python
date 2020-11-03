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
from copy import deepcopy

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
    "name": "OneViewSDK Test FCoE Network",
    "vlanId": "201",
    "connectionTemplateUri": None,
}

# Scope name to perform the patch operation
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
fcoe_networks = oneview_client.fcoe_networks
scopes = oneview_client.scopes

# Get all, with defaults
print("\nGet all fcoe-networks")
fcoe_nets = fcoe_networks.get_all()
pprint(fcoe_nets)

# Filter by name
print("\nGet all fcoe-networks filtering by name")
fcoe_nets_filtered = fcoe_networks.get_all(filter="\"'name'='OneViewSDK Test FCoE Network'\"")
pprint(fcoe_nets_filtered)

# Get all sorting by name descending
print("\nGet all fcoe-networks sorting by name")
fcoe_nets_sorted = fcoe_networks.get_all(sort='name:descending')
pprint(fcoe_nets_sorted)

# Get the first 10 records
print("\nGet the first ten fcoe-networks")
fcoe_nets_limited = fcoe_networks.get_all(0, 10)
pprint(fcoe_nets_limited)

# Get by name
fcoe_network = fcoe_networks.get_by_name(options['name'])
if fcoe_network:
    print("\nGot fcoe-network by name uri={}".format(fcoe_network.data['uri']))
else:
    # Create a FC Network
    fcoe_network = fcoe_networks.create(options)
    print("\nCreated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network.data['name'], fcoe_network.data['uri']))

# Update autoLoginRedistribution from recently created network
resource = deepcopy(fcoe_network.data)
resource['status'] = 'Warning'
resource['name'] = "{}-Renamed".format(options["name"])
fcoe_network_updated = fcoe_network.update(resource)
print("\nUpdated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network_updated.data['name'], fcoe_network_updated.data['uri']))
print("  with attribute {'status': %s}" % fcoe_network_updated.data['status'])

# Get by Uri
print("\nGet a fcoe-network by uri")
fcoe_nets_by_uri = fcoe_networks.get_by_uri(fcoe_network.data['uri'])
pprint(fcoe_nets_by_uri.data)

# Adds FCOE network to scope defined only for V300 and V500
if scope_name and 300 <= oneview_client.api_version <= 500:
    print("\nGet scope then add the network to it")
    scope = scopes.get_by_name(scope_name)
    fcoe_with_scope = fcoe_network.patch('replace',
                                         '/scopeUris',
                                         [scope.data['uri']])
    pprint(fcoe_with_scope.data)

# Delete the created network
fcoe_network.delete()
print("\nSuccessfully deleted fcoe-network")

# Creates bulk fcoe-networks
for i in range(4):
    options = {
        "name": "OneViewSDK Test FCoE Network" + str(i),
        "vlanId": int("201") + int(i),
        "connectionTemplateUri": None,
    }
    bulk_fcoe_network = fcoe_networks.create(options)
    print("\nCreated bulk fcoe-networks with name: '%s'.\n  uri = '%s'" % (bulk_fcoe_network.data['name'], bulk_fcoe_network.data['uri']))

# Delete bulk fcoe-networks
if oneview_client.api_version >= 1600:
    bulk_network_uris = []
    for i in range(4):
        fcoe_network_name = "OneViewSDK Test FCoE Network" + str(i)
        bulk_fcoe_network = fcoe_networks.get_by_name(fcoe_network_name)
        bulk_network_uris.append(bulk_fcoe_network.data['uri'])
    print("\nDelete bulk fcoe-networks")
    options_bulk_delete = {"networkUris": bulk_network_uris}
    fcoe_network.delete_bulk(options_bulk_delete)
    print("Successfully deleted bulk fcoe-networks")

# Create a FCoE Network for automation
options['name'] = "Test_fcoeNetwork"
fcoe_network = fcoe_networks.create(options)
print("\nCreated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network.data['name'], fcoe_network.data['uri']))
