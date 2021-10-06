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
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
STORAGE_POOLs = oneview_client.STORAGE_POOLs
STORAGE_SYSTEMs = oneview_client.STORAGE_SYSTEMs
storage_VOLUME_TEMPLATEs = oneview_client.storage_VOLUME_TEMPLATEs
STORAGE_POOLs = oneview_client.STORAGE_POOLs
fcoe_networks = oneview_client.fcoe_networks
scopes = oneview_client.scopes

FCOE_NETWORK_NAME = "Test_fcoeNetwork"
SCOPE_NAME = "SampleScope"

FCOE_NETWORK_URI = fcoe_networks.get_by_name(FCOE_NETWORK_NAME).data['uri']
SCOPE_URI = scopes.get_by_name(SCOPE_NAME).data['uri']
# Gets the first Root Storage Volume Template available to use in OPTIONS
root_template = oneview_client.storage_VOLUME_TEMPLATEs.get_all(filter="\"isRoot='True'\"")[0]

STORAGE_POOLS_ALL = STORAGE_POOLs.get_all()

# Request body for create operation
# Supported from API version >= 500
OPTIONS = {
    "rootTemplateUri": root_template['uri'],
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
            "default": STORAGE_POOLS_ALL[0]['uri']
        },
        "snapshotPool": {
            "meta": {
                "locked": "true",
                "semanticType": "device-snapshot-storage-pool"
            },
            "type": "string",
            "title": "Snapshot Pool",
            "format": "x-uri-reference",
            "default": STORAGE_POOLS_ALL[0]['uri'],
            "description": "A URI reference to the common provisioning group used to create
	 snapshots"
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
    "name": "test_VOLUME_TEMPLATE",
    "description": "desc"
}

# Find or add storage pool to use in template
print("Find or add storage pool to use in template")
STORAGE_POOLS_ALL = STORAGE_POOLs.get_all()
STORAGE_POOL_ADDED = False
STORAGE_SYSTEM_ADDED = False
if STORAGE_POOLS_ALL:
    STORAGE_POOL_DATA = STORAGE_POOLS_ALL[0]
    STORAGE_POOL = STORAGE_POOLs.get_by_uri(STORAGE_POOL_DATA["uri"])
    print("   Found storage pool '{name}' at uri: '{uri}".format(**STORAGE_POOL.data))
else:
    # Find or add storage system
    STORAGE_POOL_ADDED = True
    print("   Find or add storage system")
    S_SYSTEMS = STORAGE_SYSTEMs.get_all()
    if S_SYSTEMS:
        S_SYSTEM_DATA = S_SYSTEMS[0]
        STORAGE_SYSTEM = STORAGE_SYSTEMs.get_by_uri(S_SYSTEM_DATA["uri"])
        STORAGE_SYSTEM_ADDED = False
        print("      Found storage system '{name}' at uri: {uri}".format(**STORAGE_SYSTEM.data))
    else:
        OPTIONS_storage = {
            "hostname": CONFIG['STORAGE_SYSTEM_hostname'],
            "username": CONFIG['STORAGE_SYSTEM_username'],
            "password": CONFIG['STORAGE_SYSTEM_password'],
            "family": CONFIG['STORAGE_SYSTEM_family']
        }
        STORAGE_SYSTEM = STORAGE_SYSTEMs.add(OPTIONS_storage)
        S_SYSTEM_DATA = STORAGE_SYSTEM.data.copy()
        S_SYSTEM_DATA['managedDomain'] = STORAGE_SYSTEM.data['unmanagedDomains'][0]
        STORAGE_SYSTEM.update(S_SYSTEM_DATA)
        STORAGE_SYSTEM_ADDED = True
        print("      Added storage system '{name}' at uri: {uri}".format(**STORAGE_SYSTEM.data))

    # Find and add unmanaged storage pool for management
    POOL_NAME = ''
    STORAGE_POOL = {}
    print("   Find and add unmanaged storage pool for management")
    for pool in STORAGE_SYSTEM.data['unmanagedPools']:
        if pool['domain'] == STORAGE_SYSTEM.data['managedDomain']:
            POOL_NAME = pool['name']
            break
    if POOL_NAME:
        print("      Found pool '{}'".format(POOL_NAME))
        OPTIONS_pool = {
            "storageSystemUri": STORAGE_SYSTEM.data['uri'],
            "poolName": POOL_NAME
        }
        STORAGE_POOL = STORAGE_POOLs.add(OPTIONS_pool)
        print("      Successfully added pool")
    else:
        print("      No available unmanaged storage pools to add")


# Create storage volume template
print("Create storage volume template")
VOLUME_TEMPLATE = storage_VOLUME_TEMPLATEs.create(OPTIONS)
pprint(VOLUME_TEMPLATE.data)

TEMPLATE_ID = VOLUME_TEMPLATE.data["uri"].split('/')[-1]

# Update storage volume template
if VOLUME_TEMPLATE:
    print("Update '{name}' at uri: {uri}".format(**VOLUME_TEMPLATE.data))
    VOLUME_TEMPLATE_data = VOLUME_TEMPLATE.data.copy()
    VOLUME_TEMPLATE_data['description'] = "updated description"
    VOLUME_TEMPLATE.update(VOLUME_TEMPLATE_data)
    print("   Updated with 'description': '{description}'".format(**VOLUME_TEMPLATE.data))

# Get all storage volume templates
print("Get all storage volume templates")
VOLUME_TEMPLATEs_all = storage_VOLUME_TEMPLATEs.get_all()
for template in VOLUME_TEMPLATEs_all:
    print("   '{name}' at uri: {uri}".format(**template))

# Get storage volume template by uri
if VOLUME_TEMPLATE:
    print("Get storage volume template by uri: '{uri}'".format(**VOLUME_TEMPLATE.data))
    VOLUME_TEMPLATE_by_uri = storage_VOLUME_TEMPLATEs.get_by_uri(VOLUME_TEMPLATE.data['uri'])
    print("   Found '{name}' at uri: {uri}".format(**VOLUME_TEMPLATE_by_uri.data))

# Get storage volume template by name
if VOLUME_TEMPLATE:
    print("Get storage volume template by 'name': '{name}'".format(**VOLUME_TEMPLATE.data))
    VOLUME_TEMPLATE_byname = storage_VOLUME_TEMPLATEs.get_by_name(VOLUME_TEMPLATE.data['name'])
    print("   Found '{name}' at uri: {uri}".format(**VOLUME_TEMPLATE_byname.data))

# Gets the storage templates that are connected on the specified networks
# scoper_uris and private_allowed_only parameters supported only with API version >= 600
if oneview_client.api_version >= 600:
    print("Get storage templates that are connected on the specified networks")
    STORAGE_TEMPLATES = storage_VOLUME_TEMPLATEs.get_reachable_VOLUME_TEMPLATEs(
        networks=FCOE_NETWORK_URI, SCOPE_URIs=SCOPE_URI, private_allowed_only=False)
    print(STORAGE_TEMPLATES)

# Retrieves all storage systems that is applicable to the storage volume template.
print("Get storage systems that is applicable to the storage volume template")
if VOLUME_TEMPLATE:
    STORAGE_SYSTEMs = VOLUME_TEMPLATE.get_compatible_systems()
    print(STORAGE_SYSTEMs)

# Remove storage volume template
print("Delete storage volume template")
if VOLUME_TEMPLATE:
    VOLUME_TEMPLATE.delete()
    print("   Done.")

# Create storage volume template for automation
print("Create storage volume template")
VOLUME_TEMPLATE = storage_VOLUME_TEMPLATEs.create(OPTIONS)
pprint(VOLUME_TEMPLATE.data)
