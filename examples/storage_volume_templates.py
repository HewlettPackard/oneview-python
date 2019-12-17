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
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

config = {
    "ip": "10.30.9.143",
    "credentials": {
        "userName": "administrator",
        "password": "sijeadmin"
    },
    'api_version': 500,
    'storage_system_hostname': '172.18.11.11',
    'storage_system_username': 'dcs',
    'storage_system_password': 'dcs',
    'storage_system_family': 'StoreServ'
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

networks = "/rest/fcoe-networks/7f0f74a0-4957-47ac-81c1-f573aa6d83de"
scope_uris = "/rest/scopes/63d1ca81-95b3-41f1-a1ee-f9e1bc2d635f"

# Request body for create operation
# Supported from API version >= 500
options = {
    "rootTemplateUri": "/rest/storage-volume-templates/b8c4489e-4a19-4bfe-857c-aab8006478a7",
    "properties": {
        "name": {
            "title": "Volume name",
            "description": "A volume name between 1 and 100 characters",
            "meta": {"locked": "false"},
            "type": "string",
            "required": "true",
            "maxLength": 100,
            "minLength": 1},

        "size": {
            "meta": {
                "locked": "false",
                "semanticType": "capacity"
            },
            "type": "integer",
            "title": "Capacity",
            "default": 1073741824,
            "maximum": 17592186044416,
            "minimum": 268435456,
            "required": "true",
            "description": "The capacity of the volume in bytes"
        },
        "description": {
            "meta": {
                "locked": "false"
            },
            "type": "string",
            "title": "Description",
            "default": "",
            "maxLength": 2000,
            "minLength": 0,
            "description": "A description for the volume"
        },
        "isShareable": {
            "meta": {
                "locked": "false"
            },
            "type": "boolean",
            "title": "Is Shareable",
            "default": "false",
            "description": "The shareability of the volume"
        },
        "storagePool": {
            "meta": {
                "locked": "false",
                "createOnly": "true",
                "semanticType": "device-storage-pool"
            },
            "type": "string",
            "title": "Storage Pool",
            "format": "x-uri-reference",
            "required": "true",
            "description": "A common provisioning group URI reference",
            "default": "/rest/storage-pools/628C1EBD-5BA7-40F2-A856-A93C0143AC73"
        },
        "snapshotPool": {
            "meta": {
                "locked": "true",
                "semanticType": "device-snapshot-storage-pool"
            },
            "type": "string",
            "title": "Snapshot Pool",
            "format": "x-uri-reference",
            "default": "/rest/storage-pools/628C1EBD-5BA7-40F2-A856-A93C0143AC73",
            "description": "A URI reference to the common provisioning group used to create snapshots"
        },
        "provisioningType": {
            "enum": [
                "Thin",
                "Full",
                "Thin Deduplication"
            ],
            "meta": {
                "locked": "true",
                "createOnly": "true"
            },
            "type": "string",
            "title": "Provisioning Type",
            "default": "Thin",
            "description": "The provisioning type for the volume"
        }
    },
    "name": "test_02",
    "description": "desc"
}

oneview_client = OneViewClient(config)
storage_pools = oneview_client.storage_pools
storage_systems = oneview_client.storage_systems
storage_volume_templates = oneview_client.storage_volume_templates

# Find or add storage pool to use in template
print("Find or add storage pool to use in template")
storage_pools_all = storage_pools.get_all()
storage_pool_added = False
storage_system_added = False
if storage_pools_all:
    storage_pool_data = storage_pools_all[0]
    storage_pool = storage_pools.get_by_uri(storage_pool_data["uri"])
    print("   Found storage pool '{name}' at uri: '{uri}".format(**storage_pool.data))
else:
    # Find or add storage system
    storage_pool_added = True
    print("   Find or add storage system")
    s_systems = storage_systems.get_all()
    if s_systems:
        s_system_data = s_systems[0]
        storage_system = storage_systems.get_by_uri(s_system_data["uri"])
        storage_system_added = False
        print("      Found storage system '{name}' at uri: {uri}".format(**storage_system.data))
    else:
        options_storage = {
            "hostname": config['storage_system_hostname'],
            "username": config['storage_system_username'],
            "password": config['storage_system_password'],
            "family": config['storage_system_family']
        }
        storage_system = storage_systems.add(options_storage)
        s_system_data = storage_system.data.copy()
        s_system_data['managedDomain'] = s_system.data['unmanagedDomains'][0]
        storage_system.update(s_system_data)
        storage_system_added = True
        print("      Added storage system '{name}' at uri: {uri}".format(**storage_system.data))

    # Find and add unmanaged storage pool for management
    pool_name = ''
    storage_pool = {}
    print("   Find and add unmanaged storage pool for management")
    for pool in storage_system.data['unmanagedPools']:
        if pool['domain'] == storage_system.data['managedDomain']:
            pool_name = pool['name']
            break
    if pool_name:
        print("      Found pool '{}'".format(pool_name))
        options_pool = {
            "storageSystemUri": storage_system.data['uri'],
            "poolName": pool_name
        }
        storage_pool = storage_pools.add(options_pool)
        print("      Successfully added pool")
    else:
        print("      No available unmanaged storage pools to add")

# Create storage volume template
print("Create storage volume template")
volume_template = storage_volume_templates.create(options)
pprint(volume_template.data)

template_id = volume_template.data["uri"].split('/')[-1]

# Update storage volume template
print("Update '{name}' at uri: {uri}".format(**volume_template.data))
volume_template_data = volume_template.data.copy()
volume_template_data['description'] = "updated description"
volume_template.update(volume_template_data)
print("   Updated with 'description': '{description}'".format(**volume_template.data))

# Get all storage volume templates
print("Get all storage volume templates")
volume_templates_all = storage_volume_templates.get_all()
for template in volume_templates_all:
    print("   '{name}' at uri: {uri}".format(**template))

# Get storage volume template by uri
print("Get storage volume template by uri: '{uri}'".format(**volume_template.data))
volume_template_by_uri = storage_volume_templates.get_by_uri(volume_template.data['uri'])
print("   Found '{name}' at uri: {uri}".format(**volume_template_by_uri.data))

# Get storage volume template by name
print("Get storage volume template by 'name': '{name}'".format(**volume_template.data))
volume_template_byname = storage_volume_templates.get_by_name(volume_template.data['name'])
print("   Found '{name}' at uri: {uri}".format(**volume_template_byname.data))

# Gets the storage templates that are connected on the specified networks
# scoper_uris and private_allowed_only parameters supported only with API version >= 600
print("Get torage templates that are connected on the specified networks")
storage_templates = storage_volume_templates.get_reachable_volume_templates(
    networks=networks, scope_uris=scope_uris, private_allowed_only=False)
print(storage_templates)

# Retrieves all storage systems that is applicable to the storage volume template.
print("Get storage systems that is applicable to the storage volume template")
storage_systems = volume_template.get_compatible_systems()
print(storage_systems)

# Remove storage volume template
print("Delete storage volume template")
volume_template.delete()
print("   Done.")

# Remove storage pool
if storage_pool_added:
    print("Remove recently added storage pool")
    storage_pool.remove()
    print("   Done.")

# Remove storage system, if it was added
if storage_system_added:
    print("Remove recently added storage system")
    storage_system.remove()
    print("   Done.")
