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

from copy import deepcopy

from config_loader import try_load_from_file
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

OPTIONS = {
    "name": "OneViewSDK Test Ethernet Network",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None
}

OPTIONS_BULK = {
    "vlanIdRange": "1-5,7",
    "purpose": "General",
    "namePrefix": "TestNetwork",
    "smartLink": False,
    "privateNetwork": False,
    "bandwidth": {
        "maximumBandwidth": 10000,
        "typicalBandwidth": 2000
    }
}


# Scope name to perform the patch operation
SCOPE_NAME = ""
ETHERNET_NAME = "OneViewSDK Test Ethernet Network"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)
ETHERNET_NETWORKS = ONEVIEW_CLIENT.ethernet_networks
SCOPES = ONEVIEW_CLIENT.scopes

# Filter by name
print("\nGet all ethernet-networks filtering by name")
ETHERNET_NETS_FILTERED = ETHERNET_NETWORKS.get_all(
    filter="\"'name'='OneViewSDK Test Ethernet Network'\"")
for net in ETHERNET_NETS_FILTERED:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Get all sorting by name descending
print("\nGet all ethernet-networks sorting by name")
ETHERNET_NETS_SORTED = ETHERNET_NETWORKS.get_all(sort='name:descending')
for net in ETHERNET_NETS_SORTED:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Get the first 10 records
print("\nGet the first ten ethernet-networks")
ETHERNET_NETS_LIMITED = ETHERNET_NETWORKS.get_all(0, 10)
for net in ETHERNET_NETS_LIMITED:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Find network by name
print("\nFind network by name")
ETHERNET_NETWORK = ETHERNET_NETWORKS.get_by_name(ETHERNET_NAME)
if ETHERNET_NETWORK:
    print("Found ethernet-network by name: '{name}'.\n   uri = '{uri}'"\
	 .format(**ETHERNET_NETWORK.data))
else:
    # Create an ethernet Network
    print("\nCreate an ethernet network")
    ETHERNET_NETWORK = ETHERNET_NETWORKS.create(OPTIONS)
    print("Created ethernet-network '{name}' successfully.\n   uri = '{uri}'"\
	 .format(**ETHERNET_NETWORK.data))

# Create bulk ethernet networks
BULKNETWORKURIS = []
print("\nCreate bulk ethernet networks")
ETHERNET_NETS_BULK = ETHERNET_NETWORKS.create_bulk(OPTIONS_BULK)
for eth in ETHERNET_NETS_BULK:
    BULKNETWORKURIS.append(eth['uri'])
pprint(ETHERNET_NETS_BULK)

# Get all, with defaults
print("\nGet all ethernet-networks")
ETHERNET_NETS = ETHERNET_NETWORKS.get_all()
for net in ETHERNET_NETS:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Get by Uri
print("\nGet an ethernet-network by uri")
ETHERNET_NETWORK_URI = ETHERNET_NETS[0]['uri']
ETHERNET_NETS_BY_URI = ETHERNET_NETWORKS.get_by_uri(ETHERNET_NETWORK_URI)
pprint(ETHERNET_NETS_BY_URI.data)

# Update purpose recently created network
print("\nUpdate the purpose attribute from the recently created network")
ETHERNET_DATA_COPY = deepcopy(ETHERNET_NETWORK.data)
ETHERNET_DATA_COPY['purpose'] = 'Management'
ETHERNET_NETWORK_UPDATE = ETHERNET_NETWORK.update(ETHERNET_DATA_COPY)
print("Updated ethernet-network '{name}' successfully.\n   uri = '{uri}'\n with attribute\
	 ['purpose': {purpose}]".format(**ETHERNET_NETWORK_UPDATE.data))

# Get URIs of associated profiles
print("\nGet associated profiles uri(s)")
if ETHERNET_NETWORK:
    ASSOCIATED_PROFILES = ETHERNET_NETWORK.get_ASSOCIATED_PROFILES()
    pprint(ASSOCIATED_PROFILES)

# Get URIs of uplink port group
print("\nGet uplink port group uri(s)")
if ETHERNET_NETWORK:
    UPLINK_GROUP_URIS = ETHERNET_NETWORK.get_associated_uplink_groups()
    pprint(UPLINK_GROUP_URIS)

# Get the associated uplink set resources
print("\nGet associated uplink sets")
UPLINK_SETS = ONEVIEW_CLIENT.uplink_sets
for uri in UPLINK_GROUP_URIS:
    uplink = UPLINK_SETS.get_by_uri(uri)
    pprint(uplink.data)

# Adds Ethernet network to SCOPE defined only for V300 and V500
if SCOPE_NAME and 300 <= ONEVIEW_CLIENT.api_version <= 500:
    print("\nGet SCOPE then add the network to it")
    SCOPE = SCOPES.get_by_name(SCOPE_NAME)
    ETHERNET_WITH_SCOPE = ETHERNET_NETWORK.patch('replace',
                                                 '/SCOPEUris',
                                                 [SCOPE.data['uri']])
    pprint(ETHERNET_WITH_SCOPE)

# Delete bulk ethernet networks
if ONEVIEW_CLIENT.api_version >= 1600:
    OPTIONS_BULK_DELETE = {"networkUris": BULKNETWORKURIS}
    ETHERNET_NETWORK.delete_bulk(OPTIONS_BULK_DELETE)
    print("Successfully deleted bulk ethernet networks")

# Delete the created network
print("\nDelete the ethernet network")
ETHERNET_NETWORK.delete()
print("Successfully deleted ethernet-network")

# Create networks for automation 'mgmt_nw' and 'iscsi_nw'
MGMT_SUBNET = '10.1.0.0'
ISCSI_SUBNET = '192.168.10.0'
ALL_SUBNETS = ONEVIEW_CLIENT.id_pools_ipv4_subnets.get_all()

for subnet in ALL_SUBNETS:
    if subnet['networkId'] == MGMT_SUBNET:
        MGMT_SUBNET_uri = subnet['uri']
    if subnet['networkId'] == ISCSI_SUBNET:
        ISCSI_SUBNET_uri = subnet['uri']

MGMT_NETWORK_BODY = OPTIONS.copy()
MGMT_NETWORK_BODY['name'] = 'mgmt_nw'
MGMT_NETWORK_BODY['ethernetNetworkType'] = "Untagged"
MGMT_NETWORK_BODY['purpose'] = "Management"
MGMT_NETWORK_BODY['subnetUri'] = MGMT_SUBNET_uri
MANAGEMENT_NETWORK = ETHERNET_NETWORKS.create(MGMT_NETWORK_BODY)
print("Created ethernet-network '{name}' successfully.\n   uri = '{uri}'"\
	 .format(**MANAGEMENT_NETWORK.data))

ISCSI_NETWORK_BODY = OPTIONS.copy()
ISCSI_NETWORK_BODY['name'] = 'iscsi_nw'
ISCSI_NETWORK_BODY['ethernetNetworkType'] = "Tagged"
ISCSI_NETWORK_BODY['vlanId'] = 1209
ISCSI_NETWORK_BODY['purpose'] = "ISCSI"
ISCSI_NETWORK_BODY['subnetUri'] = ISCSI_SUBNET_uri
ISCSI_NETWORK = ETHERNET_NETWORKS.create(ISCSI_NETWORK_BODY)
print("Created ethernet-network '{name}' successfully.\n   uri = '{uri}'"\
	 .format(**ISCSI_NETWORK.data))
