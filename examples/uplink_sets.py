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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

# To run this example fill the ip and the credentials below or use a CONFIGuration file
CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
UPLINK_SETs = oneview_client.UPLINK_SETs


# To run this example you can define an logical interconnect uri (logicalInterconnectUri), ethernet
# network uri
# and ethernet name or the example will attempt to retrieve those automatically from the appliance.
ETHERNET_NETWORK_NAME = 'OneViewSDK Test Ethernet Network on Logical Interconnect'

# Attempting to get first LI and Ethernet uri and use them for this example
logical_interconnect_uri = oneview_client.logical_interconnects.get_all()[0]['uri']

enet = oneview_client.ethernet_NETWORKS.get_by_name(ETHERNET_NETWORK_NAME)
ETHERNET_NETWORK_URI = enet.data['uri']

OPTIONS = {
    "name": "Uplink Set Demo",
    "status": "OK",
    "logicalInterconnectUri": logical_interconnect_uri,
    "networkUris": [
        ETHERNET_NETWORK_URI
    ],
    "fcNetworkUris": [],
    "fcoeNetworkUris": [],
    "portConfigInfos": [],
    "connectionMode": "Auto",
    "networkType": "Ethernet",
    "manualLoginRedistributionState": "NotSupported",
}

# Get a paginated list of uplink set resources sorting by name ascending and filtering by status
print("\nGet a list of uplink sets")
ALL_UPLINK_SETS = UPLINK_SETs.get_all(0, 15, sort='name:ascending')
for UPLINK_SET in ALL_UPLINK_SETS:
    print('  %s' % UPLINK_SET['name'])

if ALL_UPLINK_SETS:
    # Get an uplink set resource by uri
    print("\nGet an uplink set by uri")
    UPLINK_URI = ALL_UPLINK_SETS[0]['uri']
    UPLINK_SET = UPLINK_SETs.get_by_uri(UPLINK_URI)
    pprint(UPLINK_SET.data)

# Get an uplink set resource by name
print("\nGet uplink set by name")
UPLINK_SET = UPLINK_SETs.get_by_name(OPTIONS["name"])
if UPLINK_SET:
    print("Found uplink set at uri '{uri}'\n  by name = '{name}'".format(**UPLINK_SET.data))
else:
    # Create an uplink set
    print("\nCreate an uplink set")
    UPLINK_SET = UPLINK_SETs.create(OPTIONS)
    print("Created uplink set '{name}' successfully.\n  uri = '{uri}'".format(**UPLINK_SET.data))

# Update an uplink set
print("\nUpdate an uplink set")
if UPLINK_SET:
    UPLINK_SET.data['name'] = 'Renamed Uplink Set Demo'
    UPLINK_SET.update(UPLINK_SET.data)
    print("Updated uplink set name to '{name}' successfully.\n  uri = '{uri}'".format(**UPLINK_SET.data))

# Add an ethernet network to the uplink set
# To run this example you must define an ethernet network uri or ID below
if ETHERNET_NETWORK_NAME and UPLINK_SET:
    print("\nAdd an ethernet network to the uplink set")
    UPLINK_ADDED_ETHERNET = UPLINK_SET.add_ethernet_NETWORKS(ETHERNET_NETWORK_NAME)
    print("The uplink set with name = '{name}' have now the networkUris:\n
	 {networkUris}".format(**UPLINK_ADDED_ETHERNET))

# Remove an ethernet network from the uplink set
# To run this example you must define an ethernet network uri or ID below
if ETHERNET_NETWORK_NAME and UPLINK_SET:
    print("\nRemove an ethernet network of the uplink set")
    UPLINK_REMOVED_ETHERNET = UPLINK_SET.remove_ethernet_NETWORKS(ETHERNET_NETWORK_NAME)
    print("The uplink set with name = '{name}' have now the networkUris:\n
	 {networkUris}".format(**UPLINK_REMOVED_ETHERNET))

# Get the associated ethernet NETWORKS of an uplink set
print("\nGet the associated ethernet NETWORKS of the uplink set")
if UPLINK_SET:
    NETWORKS = UPLINK_SET.get_ethernet_NETWORKS()
    pprint(NETWORKS)

# Delete the recently created uplink set
print("\nDelete the uplink set")
if UPLINK_SET:
    UPLINK_SET.delete()
    print("Successfully deleted the uplink set")
