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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

# To run this example fill the ip and the credentials bellow or use a configuration file
config = {
    "ip": "10.50.9.33",
    "credentials": {
        "userName": "Administrator",
        "password": "admin123",
    },
    "api_version": 1800
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
uplink_sets = oneview_client.uplink_sets


# To run this example you can define an logical interconnect uri (logicalInterconnectUri), ethernet network uri
# and ethernet name or the example will attempt to retrieve those automatically from the appliance.
logical_interconnect_uri = None
ethernet_network_uri = None
ethernet_network_name = None

# Attempting to get first LI and Ethernet uri and use them for this example
if logical_interconnect_uri is None:
    logical_interconnect_uri = oneview_client.logical_interconnects.get_all()[0]['uri']
if ethernet_network_uri is None:
    enet = oneview_client.ethernet_networks.get_all()
    ethernet_network_uri = enet[0]['uri']

    # Ethernet name to test add/remove of network uris
    if not ethernet_network_name:
        ethernet_network_name = enet[1]['name']

options = {
    "name": "Uplink Set Demo",
    "status": "OK",
    "logicalInterconnectUri": logical_interconnect_uri,
    "networkUris": [
    #    ethernet_network_uri
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
all_uplink_sets = uplink_sets.get_all(0, 15, sort='name:ascending')
for uplink_set in all_uplink_sets:
    print('  %s' % uplink_set['name'])

if all_uplink_sets:
    # Get an uplink set resource by uri
    print("\nGet an uplink set by uri")
    uplink_uri = all_uplink_sets[0]['uri']
    uplink_set = uplink_sets.get_by_uri(uplink_uri)
    pprint(uplink_set.data)

# Get an uplink set resource by name
print("\nGet uplink set by name")
uplink_set = uplink_sets.get_by_name(options["name"])
if uplink_set:
    print("Found uplink set at uri '{uri}'\n  by name = '{name}'".format(**uplink_set.data))
else:
    # Create an uplink set
    print("\nCreate an uplink set")
    uplink_set = uplink_sets.create(options)
    print("Created uplink set '{name}' successfully.\n  uri = '{uri}'".format(**uplink_set.data))

# Update an uplink set
print("\nUpdate an uplink set")
uplink_set.data['name'] = 'Renamed Uplink Set Demo'
uplink_set.update(uplink_set.data)
print("Updated uplink set name to '{name}' successfully.\n  uri = '{uri}'".format(**uplink_set.data))

# Add an ethernet network to the uplink set
# To run this example you must define an ethernet network uri or ID below
if ethernet_network_name:
    print("\nAdd an ethernet network to the uplink set")
    uplink_added_ethernet = uplink_set.add_ethernet_networks(ethernet_network_name)
    print("The uplink set with name = '{name}' have now the networkUris:\n {networkUris}".format(**uplink_added_ethernet))

# Remove an ethernet network from the uplink set
# To run this example you must define an ethernet network uri or ID below
if ethernet_network_name:
    print("\nRemove an ethernet network of the uplink set")
    uplink_removed_ethernet = uplink_set.remove_ethernet_networks(ethernet_network_name)
    print("The uplink set with name = '{name}' have now the networkUris:\n {networkUris}".format(**uplink_removed_ethernet))

# Get the associated ethernet networks of an uplink set
print("\nGet the associated ethernet networks of the uplink set")
networks = uplink_set.get_ethernet_networks()
pprint(networks)

# Delete the recently created uplink set
print("\nDelete the uplink set")
uplink_set.delete()
print("Successfully deleted the uplink set")
