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
from hpOneView.exceptions import HPOneViewException
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

default_options = {
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

# Set the URI of existent resources to be added/removed to/from the scope
resource_uri_1 = ethernet_networks.get_by('name', 'TestNetwork_1')[0]['uri']
resource_uri_2 = ethernet_networks.get_by('name', 'TestNetwork_2')[0]['uri']
resource_uri_3 = ethernet_networks.get_by('name', 'TestNetwork_3')[0]['uri']

# Create a scope
print("\n## Create the scope")
options = {
    "name": "SampleScope",
    "description": "Sample Scope description"
}
scope = scopes.create(options)
pprint(scope)

# Update the name of the scope
print("\n## Update the scope")
scope['name'] = "SampleScopeRenamed"
scope = scopes.update(scope)
pprint(scope)

# Find the recently created scope by name
scope_by_name = scopes.get_by_name('SampleScopeRenamed')
print("\n## Found scope by name: '{name}'.\n  uri = '{uri}'".format(**scope_by_name))

# Find the recently created scope by URI
scope_by_uri = scopes.get(scope['uri'])
print("\n## Found scope by URI: '{uri}'.\n  name = '{name}'".format(**scope_by_uri))

# Get all scopes
print("\n## Get all Scopes")
all_scopes = scopes.get_all()
pprint(all_scopes)

# Update the scope resource assignments (Available only in API300)
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
except HPOneViewException as e:
    print(e.msg)

# Patch the scope assigning and unassigning two ethernet resources (Available only in API500)
try:
    print("\n## Patch the scope adding two resource uris")
    resource_list = [resource_uri_1, resource_uri_2]
    edited_scope = scopes.patch(scope['uri'], 'replace', '/addedResourceUris', resource_list)
    pprint(edited_scope)

    print("\n## Patch the scope removing the two previously added resource uris")
    edited_scope = scopes.patch(scope['uri'], 'replace', '/removedResourceUris', resource_list)
    pprint(edited_scope)
except HPOneViewException as e:
    print(e.msg)

# Delete the scope
scopes.delete(scope)
print("\n## Scope deleted successfully.")
