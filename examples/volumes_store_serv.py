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

from CONFIG_loader import try_load_from_file
from hpeOneView.exceptions import HPEOneViewException
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

# To run this example, you may set a name to add the volume to management in HPE OneView (optional)
STORAGE_POOL_NAME = 'CPG-SSD'

# To run this example, you may set a name to add the volume to management in HPE OneView (optional)
UNMANAGED_VOLUME_NAME = ''

oneview_client = OneViewClient(CONFIG)

print("\nGet the storage system and the storage pool to create the volumes")
storage_system = oneview_client.storage_systems.get_by_hostname(CONFIG['storage_system_hostname'])
print("    Got storage system '{name}' with hostname '{hostname}' in {uri}".format(**storage_system))
storage_pools = oneview_client.storage_pools.get_all()
STORAGE_POOL_AVAILABLE = False
for sp in storage_pools:
    if sp['storageSystemUri'] == storage_system['uri']:
        if (STORAGE_POOL_NAME and sp['name'] == STORAGE_POOL_NAME) or (not STORAGE_POOL_NAME):
            STORAGE_POOL_AVAILABLE = True
            storage_pool = sp
            print("    Got storage pool '{name}' from storage system '{storageSystemUri}'".format(**storage_pool))
if not STORAGE_POOL_AVAILABLE:
    raise ValueError("ERROR: No storage pools found attached to the storage system")

print("    Get template to be used in the new volume")
volume_template = oneview_client.storage_volume_templates.get_by('storagePoolUri',
	 storage_pool['uri'])[0]

# Create a volume with a Storage Pool
print("\nCreate a volume with a specified Storage Pool")

OPTIONS_WITH_STORAGE_POOL = {
    "properties": {
        "name": 'ONEVIEW_SDK_TEST_VOLUME_STORE_SERV',
        "description": 'Test volume with common creation: Storage Pool',
        "storagePool": storage_pool['uri'],
        "size": 1024 * 1024 * 1024,  # 1GB
        "provisioningType": 'Thin',
        "isShareable": True,
        "snapshotPool": storage_pool['uri']
    },
    "templateUri": volume_template['uri'],
    "isPermanent": True
}
volume = oneview_client.volumes.create(OPTIONS_WITH_STORAGE_POOL)
pprint(volume)

MANAGED_VOLUME = None
if UNMANAGED_VOLUME_NAME:
    print("\nAdd a volume for management to the appliance using the name of the volume")

    UNMANAGED_ADD_OPTIONS = {
        "deviceVolumeName": UNMANAGED_VOLUME_NAME,
        "description": 'Unmanaged test volume added for management: Storage System + Storage Pool +
	 Name',
        "storageSystemUri": storage_system['uri'],
        "isShareable": True
    }
    MANAGED_VOLUME = oneview_client.volumes.add_from_existing(UNMANAGED_ADD_OPTIONS)
    pprint(MANAGED_VOLUME)

# Get all managed volumes
print("\nGet a list of all managed volumes")
volumes = oneview_client.volumes.get_all()
for found_volume in volumes:
    print('  Name: {name}').format(**found_volume)

# Create a snapshot
print("\nCreate a snapshot")

SNAPSHOT_OPTIONS = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot",
}
volume = oneview_client.volumes.create_snapshot(volume['uri'], SNAPSHOT_OPTIONS)
print("Created a snapshot for the volume '{name}'".format(**volume))

# Get recently created snapshot resource by name
print("\nGet a snapshot by name")
created_snapshot = oneview_client.volumes.get_snapshot_by(volume['uri'], 'name', 'Test Snapshot')[0]
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**created_snapshot))

SNAPSHOT_URI = created_snapshot['uri']

# Get recently created snapshot resource by uri
print("\nGet a snapshot")
try:
    snapshot = oneview_client.volumes.get_snapshot(SNAPSHOT_URI, volume['uri'])
    pprint(snapshot)
except HPEOneViewException as e:
    print(e.msg)

print("\nCreate a new volume from the snapshot")
from_SNAPSHOT_OPTIONS = {
    "properties": {
        "name": 'TEST_VOLUME_FROM_SNAPSHOT',
        "description": 'Create volume from snapshot and template {name}'.format(**volume_template),
        "provisioningType": 'Thin',
        "isShareable": True,
        "size": 1024 * 1024 * 1024,  # 1GB
        "storagePool": storage_pool['uri']
    },
    "templateUri": volume_template['uri'],
    "snapshotUri": SNAPSHOT_URI,
    "isPermanent": True
}

try:
    volume_from_snapshot = oneview_client.volumes.create_from_snapshot(from_SNAPSHOT_OPTIONS)
    print("Created volume '{name}': {description}. URI: {uri}".format(**volume_from_snapshot))
except HPEOneViewException as e:
    print(e.msg)

# Get all the attachable volumes which are managed by the appliance
print("\nGet all the attachable volumes which are managed by the appliance")
attachable_volumes = oneview_client.volumes.get_attachable_volumes()
pprint(attachable_volumes)

print("\nDelete the recently created volumes")
if oneview_client.volumes.delete(volume):
    print("The volume that was previously created with a Storage Pool was deleted from OneView and
	 storage system")

if oneview_client.volumes.delete(volume_from_snapshot):
    print("The volume that was previously created with from Snaphsot was deleted from OneView and
	 storage system")

if MANAGED_VOLUME and oneview_client.volumes.delete(MANAGED_VOLUME, suppress_device_updates=True):
    print("The unamanged volume that was previously added using the name was deleted from OneView
	 only")
