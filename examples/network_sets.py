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
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "name": "OneViewSDK Test Network Set"
}

options_ethernet1 = {
    "name": "OneViewSDK Test Ethernet Network1",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

options_ethernet2 = {
    "name": "OneViewSDK Test Ethernet Network2",
    "vlanId": 201,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

# Scope name to perform the patch operation
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create two Ethernet networks
ethernet_network1 = oneview_client.ethernet_networks.create(options_ethernet1)
ethernet_network2 = oneview_client.ethernet_networks.create(options_ethernet2)
print("Created ethernet-networks successfully.\n  uri = '%s' and \n\t'%s'" %
      (ethernet_network1['uri'], ethernet_network2['uri']))

# create Network set containing Ethernet networks
options['networkUris'] = [
    ethernet_network1['uri'],
    ethernet_network2['uri']
]
network_set = oneview_client.network_sets.create(options)
print('Created network-set {} successfully'.format(network_set['name']))

# Find recently created network set by name
network_set = oneview_client.network_sets.get_by(
    'name', 'OneViewSDK Test Network Set')[0]
print("Found network set by name: '%s'.\n  uri = '%s'" %
      (network_set['name'], network_set['uri']))

# Get network set without Ethernet networks
try:
    print("Get network-set without Ethernet:")
    net_set_without_ethernet = oneview_client.network_sets.get_without_ethernet(network_set['uri'])
    pprint(net_set_without_ethernet)
except HPOneViewException as e:
    print(e.msg)

# Update name of recently created network set
network_set['name'] = 'OneViewSDK Test Network Set Re-named'
network_set = oneview_client.network_sets.update(network_set)
print("Updated network set '%s' successfully.\n  uri = '%s'" %
      (network_set['name'], network_set['uri']))
print("  with attribute {'name': %s}" %
      network_set['name'])

# Get all network sets
print("Get all network sets")
net_sets = oneview_client.network_sets.get_all()
pprint(net_sets)

# Get all network sets without Ethernet
print("Get all network sets without Ethernet")
net_sets_without_ethernet = oneview_client.network_sets.get_all_without_ethernet()
pprint(net_sets_without_ethernet)

# Adds network set to scope defined only for V300 and V500
if scope_name and 300 <= oneview_client.api_version <= 500:
    print("\nGet scope then add the network set to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    net_set_with_scope = oneview_client.network_sets.patch(network_set['uri'],
                                                           'replace',
                                                           '/scopeUris',
                                                           [scope['uri']])
    pprint(net_set_with_scope)

# Delete network set
oneview_client.network_sets.delete(network_set)
print("Successfully deleted network set")

# Delete Ethernet networks
oneview_client.ethernet_networks.delete(ethernet_network1)
oneview_client.ethernet_networks.delete(ethernet_network2)
print("Successfully deleted Ethernet networks")
