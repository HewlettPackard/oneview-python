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

from examples.CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)

# To run this example you must set valid URI of the network RESOURCE and of the image streamer
# APPLIANCE
MANAGEMENT_NETWORK_URI = ""
APPLIANCE_URI = ""

print("Add an Os Deployment Server:")
RESOURCE = {
    "description": "OS Deployment Server",
    "name": "I3s-Deployment Server",
    "mgmtNetworkUri": MANAGEMENT_NETWORK_URI,
    "APPLIANCEUri": APPLIANCE_URI,
}
OS_DEPLOYMENT_SERVER_ADDED = oneview_client.OS_DEPLOYMENT_SERVERs.add(RESOURCE)
pprint(OS_DEPLOYMENT_SERVER_ADDED)

print("Get all Os Deployment Servers:")
OS_DEPLOYMENT_SERVERS_ALL = oneview_client.OS_DEPLOYMENT_SERVERs.get_all(start=0, count=-1,
	 filter='state=Connected')
pprint(OS_DEPLOYMENT_SERVERS_ALL)

OS_DEPLOYMENT_SERVER_URI = OS_DEPLOYMENT_SERVER_ADDED['uri']

print("Get an Os Deployment Server by URI:")
OS_DEPLOYMENT_SERVER = oneview_client.OS_DEPLOYMENT_SERVERs.get(OS_DEPLOYMENT_SERVER_URI)
pprint(OS_DEPLOYMENT_SERVER)

print("Get Os Deployment Servers by Filter:")
OS_DEPLOYMENT_SERVERs = oneview_client.OS_DEPLOYMENT_SERVERs.get_by('state', 'Connected')
pprint(OS_DEPLOYMENT_SERVERs)

print("Get the Os Deployment Server by Name:")
OS_DEPLOYMENT_SERVERs = oneview_client.OS_DEPLOYMENT_SERVERs.get_by_name("OS Deployment Server")
pprint(OS_DEPLOYMENT_SERVERs)

print("Get all Deployment Servers Networks:")
NETWORKS = oneview_client.OS_DEPLOYMENT_SERVERs.get_NETWORKS()
pprint(NETWORKS)

print("List all the Image Streamer RESOURCEs associated with deployment-server:")
APPLIANCES = oneview_client.OS_DEPLOYMENT_SERVERs.get_APPLIANCES()
pprint(APPLIANCES)

print("List the particular Image Streamer RESOURCE with an given URI:")
APPLIANCE = oneview_client.OS_DEPLOYMENT_SERVERs.get_APPLIANCE(APPLIANCES[0]['uri'], 'name')
pprint(APPLIANCE)

print("Update the Deployment Server description:")
OS_DEPLOYMENT_SERVER_ADDED['description'] = "Description Updated"
OS_DEPLOYMENT_SERVER_updated = oneview_client.OS_DEPLOYMENT_SERVERs.update(OS_DEPLOYMENT_SERVER_ADDED)
pprint(OS_DEPLOYMENT_SERVER_updated)

print("Delete the added Deployment Server:")
oneview_client.OS_DEPLOYMENT_SERVERs.delete(OS_DEPLOYMENT_SERVER_updated)
print("Done")
