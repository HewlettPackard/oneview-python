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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<user>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
scopes = oneview_client.scopes
ethernet_networks = oneview_client.ethernet_networks

bulk_ethernet = {
    "vlanIdRange": "1-3",
    "purpose": "General",
    "namePrefix": "TestNetwork",
    "smartLink": False,
    "privateNetwork": False,
    "bandwidth": {
        "maximumBandwidth": 10000,
        "typicalBandwidth": 2000
    }
}

# Create bulk ethernet networks
bulkNetworkUris = []
print("\nCreate bulk ethernet networks")
ethernet_nets_bulk = ethernet_networks.create_bulk(bulk_ethernet)

# Set the URI of existent resources to be added/removed to/from the scope
resource_uri_1 = ethernet_networks.get_by_name('TestNetwork_1').data['uri']
resource_uri_2 = ethernet_networks.get_by_name('TestNetwork_2').data['uri']
resource_uri_3 = ethernet_networks.get_by_name('TestNetwork_3').data['uri']

options = {
    "name": "SampleScope",
    "description": "Sample Scope description"
}
# Find scope by name
print("\n## Getting the scope by name")
scope = scopes.get_by_name(options['name'])
if not scope:
    # Create a scope
    print("\n## Create the scope")
    scope = scopes.create(options)
pprint(scope.data)

# Update the name of the scope
print("\n## Update the scope")
resource = scope.data.copy()
resource['name'] = "SampleScopeRenamed"
scope.update(resource)
print("\n## scope updated successfully")

# Find the recently created scope by URI
print("\n## Find scope by URI")
scope_by_uri = scope.get_by_uri(scope.data['uri'])
pprint(scope_by_uri.data)

# Get all scopes
print("\n## Get all Scopes")
all_scopes = scope.get_all()
for elem in all_scopes:
    print(" - {}".format(elem['name']))

# Update the scope resource assignments (Available only in API300)
if oneview_client.api_version == 300:
    try:
        print("\n## Update the scope resource assignments, adding two resources")
        options = {
            "addedResourceUris": [resource_uri_1, resource_uri_2]
        }
        scopes.update_resource_assignments(scope['uri'], options)
        print("  Done.")

        print("\n## Update the scope resource assignments, adding one resource and removing another previously added")
        options = {
            "removedResourceUris": [resource_uri_1],
            "addedResourceUris": [resource_uri_3]
        }
        scopes.update_resource_assignments(scope['uri'], options)
        print("  Done.")
    except HPEOneViewException as e:
        print(e.msg)

# Updates the name and description of a scope assigning and unassigning ethernet resources
# (Available only from API500)
if oneview_client.api_version >= 500:
    try:
        print("\n## Patch the scope adding two resource uris")
        edited_scope = scope.patch('add', '/addedResourceUris/-', resource_uri_1)
        pprint(edited_scope.data)

        edited_scope = scope.patch('add', '/addedResourceUris/-', resource_uri_2)
        pprint(edited_scope.data)

        # Find the recently created scope by name
        print("\n## Find scope by name")
        scope_by_name = scope.get_by_name(scope.data['name'])
        pprint(scope_by_name.data)

        # Get the resource assignments of scope
        print("\n## Find resource assignments to scope")
        scope_assigned_resource = scopes.get_scope_resource(resource_uri_1)
        pprint(scope_assigned_resource.data)

        print("\n## Patch the scope removing one of the previously added resource uris")
        resource_list = [resource_uri_1]
        edited_scope = scope.patch('replace', '/removedResourceUris', resource_list)
        pprint(edited_scope.data)

        print("\n## Patch the scope updating the name")
        update_name = "MySampleScope"
        edited_scope = scope.patch('replace', '/name', update_name)
        pprint(edited_scope.data)

        print("\n## Patch the scope updating the description")
        update_description = "Modified scope description"
        edited_scope = scope.patch('replace', '/description', update_description)
        pprint(edited_scope.data)
    except HPEOneViewException as e:
        print(e.msg)

# Get the resource assignments of scope when unassigned
print("\n## Find resource assignments to scope when resource unassigned")
scope_assigned_resource = scopes.get_scope_resource(resource_uri_1)
pprint(scope_assigned_resource.data)

# Delete the scope
scope.delete()
print("\n## Scope deleted successfully.")
# Create a scopes for automation
scope = scopes.get_by_name(options['name'])
if not scope:
    # Create a scope
    print("\n## Create the scope")
    scope = scopes.create(options)
