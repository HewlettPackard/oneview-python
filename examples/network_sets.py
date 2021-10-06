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
    "name": "OneViewSDK Test Network Set"
}

OPTIONS_ETHERNET1 = {
    "name": "OneViewSDK Test Ethernet Network1",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

OPTIONS_ETHERNET2 = {
    "name": "OneViewSDK Test Ethernet Network2",
    "vlanId": 201,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

# Scope name to perform the patch operation
SCOPE_NAME = ""

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

ethernet_networks = oneview_client.ethernet_networks
NETWORK_SETS = oneview_client.network_sets
SCOPES = oneview_client.scopes

# Get all network sets
print("Get all network sets")
NET_SETS = NETWORK_SETS.get_all()
pprint(NET_SETS)

# Get all network sets without Ethernet
print("Get all network sets without Ethernet")
NET_SETS_WITHOUT_ETHERNET = NETWORK_SETS.get_all_without_ethernet()
pprint(NET_SETS_WITHOUT_ETHERNET)

# Create two Ethernet networks
ETHERNET_NETWORK1 = ethernet_networks.create(OPTIONS_ETHERNET1)
ETHERNET_NETWORK2 = ethernet_networks.create(OPTIONS_ETHERNET2)
print("Created ethernet-networks successfully.\n  uri = '%s' and \n\t'%s'" %
      (ETHERNET_NETWORK1.data['uri'], ETHERNET_NETWORK2.data['uri']))

# create Network set containing Ethernet networks
OPTIONS['networkUris'] = [
    ETHERNET_NETWORK1.data['uri'],
    ETHERNET_NETWORK2.data['uri']
]
NETWORK_SET = NETWORK_SETS.create(OPTIONS)
print('Created network-set {} successfully'.format(NETWORK_SET.data['name']))

# Find recently created network set by name
NETWORK_SET = NETWORK_SETS.get_by_name(OPTIONS["name"])
print("Found network set by name: '%s'.\n  uri = '%s'" %
      (NETWORK_SET.data['name'], NETWORK_SET.data['uri']))

# Get network set without Ethernet networks
print("Get network-set without Ethernet:")
if NETWORK_SET:
    NET_SET_WITHOUT_ETHERNET = NETWORK_SET.get_without_ethernet()
    pprint(NET_SET_WITHOUT_ETHERNET)
else:
    print("No network set '%s' found.\n" % (NETWORK_SET.data['name']))

# Update name of recently created network set
NETWORK_SET_UPDATE = {'name': 'OneViewSDK Test Network Set Re-named'}
if NETWORK_SET:
    NETWORK_SET = NETWORK_SET.update(NETWORK_SET_UPDATE)
    print("Updated network set '%s' successfully.\n" % (NETWORK_SET.data['name']))

# Adds network set to SCOPE defined only for V300 and V500
if SCOPE_NAME and 300 <= oneview_client.api_version <= 500:
    print("\nGet SCOPE then add the network set to it")
    SCOPE = SCOPES.get_by_name(SCOPE_NAME)
    NET_SET_WITH_SCOPE = NETWORK_SETS.patch('replace',
                                            '/SCOPEUris',
                                            [SCOPE.data['uri']])
    pprint(NET_SET_WITH_SCOPE)

# Delete network set
NETWORK_SET.delete()
print("Successfully deleted network set")

# Delete Ethernet networks
ETHERNET_NETWORK1.delete()
ETHERNET_NETWORK2.delete()
print("Successfully deleted Ethernet networks")
