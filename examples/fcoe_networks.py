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
from hpOneView.oneview_client import OneViewClient
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
    "name": "OneViewSDK Test FCoE Network",
    "vlanId": "201",
    "connectionTemplateUri": None,
}

options_bulk_delete = {
    "networkUris": [
        "/rest/fcoe-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548",
        "/rest/fcoe-networks/f2f0031b-52bd-4223-9ac1-d91cb519d549",
        "/rest/fcoe-networks/02f0031b-52bd-4223-9ac1-d91cb519d54a"
    ]
}

# Scope name to perform the patch operation
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
fcoe_networks = oneview_client.fcoe_networks

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
resource = fcoe_network.data.copy()
resource['status'] = 'Warning'
resource['name'] = "{}-Renamed".format(options["name"])
fcoe_network.update(resource)
print("\nUpdated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network.data['name'], fcoe_network.data['uri']))
print("  with attribute {'status': %s}" % fcoe_network.data['status'])

# Get by Uri
print("\nGet a fcoe-network by uri")
fcoe_nets_by_uri = fcoe_networks.get_by_uri(fcoe_network.data['uri'])
pprint(fcoe_nets_by_uri.data)

# Adds FCOE network to scope defined only for V300 and V500
if scope_name and 300 <= oneview_client.api_version <= 500:
    print("\nGet scope then add the network to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    fcoe_with_scope = fcoe_network.patch('replace',
                                         '/scopeUris',
                                         [scope.data['uri']])
    pprint(fcoe_with_scope.data)

# Delete the created network
fcoe_network.delete()
print("\nSuccessfully deleted fcoe-network")

# Delete bulk fcoe networks
if oneview_client.api_version >= 1600:
    print("\nDelete bulk fcoe networks")
    fcoe_network.delete_bulk(options_bulk_delete)
    print("Successfully deleted bulk fcoe networks")
