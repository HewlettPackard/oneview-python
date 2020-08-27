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
from hpeOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
volumes = oneview_client.volumes
storage_systems = oneview_client.storage_systems
storage_pools = oneview_client.storage_pools

# To run this example, you may set a WWN to add a volume using the WWN of the volume (optional)
unmanaged_volume_wwn = ''

# Defines the storage system and the storage pool which are provided to create the volumes
storage_system = storage_systems.get_all()[0]
storage_pools_all = storage_pools.get_all()
storage_pool_available = False

for sp in storage_pools_all:
    if sp['storageSystemUri'] == storage_system['uri']:
        storage_pool_available = True
        storage_pool = sp

if not storage_pool_available:
    raise ValueError("ERROR: No storage pools found attached to the storage system")

# Create a volume with a Storage Pool
print("\nCreate a volume with a specified Storage Pool and Snapshot Pool")

options = {
    "properties": {
        "storagePool": '/rest/storage-pools/547F8659-BD66-4775-9943-A93C0143AC70',
        "size": 1024 * 1024 * 1024,  # 1GB
        "isShareable": False,
        "snapshotPool": '/rest/storage-pools/547F8659-BD66-4775-9943-A93C0143AC70',
        "provisioningType": "Thin",
        "name": "ONEVIEW_SDK_TEST_VOLUME_TYPE_1"
    },
    "templateUri": "/rest/storage-volume-templates/b8c4489e-4a19-4bfe-857c-aab8006478a7",
    "isPermanent": False
}

new_volume = volumes.create(options)
pprint(new_volume.data)

# Add a volume for management by the appliance using the WWN of the volume
if unmanaged_volume_wwn:
    print("\nAdd a volume for management by the appliance using the WWN of the volume")

    options_with_wwn = {
        "type": "AddStorageVolumeV2",
        "name": 'ONEVIEW_SDK_TEST_VOLUME_TYPE_4',
        "description": 'Test volume added for management: Storage System + Storage Pool + WWN',
        "storageSystemUri": storage_system['uri'],
        "wwn": unmanaged_volume_wwn,
        "provisioningParameters": {
            "shareable": False
        }
    }
    volume_added_with_wwn = volumes.create(options_with_wwn)
    pprint(volume_added_with_wwn.data)

# Get all managed volumes
print("\nGet a list of all managed volumes")
volumes_all = volumes.get_all()
for volume in volumes_all:
    print("Name: {name}".format(**volume))

# Find a volume by name
volume = volumes.get_by_name(new_volume.data['name'])
print("\nFound a volume by name: '{name}'.\n  uri = '{uri}'".format(**volume.data))

# Update the name of the volume recently found to 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
volume_data = volume.data.copy()
volume_data['name'] = 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
volume.update(volume_data)
print("\nVolume updated successfully.\n  uri = '{uri}'\n  with attribute 'name' = {name}".format(**volume.data))

# Find a volume by URI
volume = volumes.get_by_uri(volume.data["uri"])
print("\nFind a volume by URI")
pprint(volume.data)

# Create a snapshot
print("\nCreate a snapshot")
snapshot_options = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot"
}
created_snapshot = volume.create_snapshot(snapshot_options)
print("Created a snapshot for the volume '{name}'".format(**volume.data))

# Get recently created snapshot resource by name
print("\nGet a snapshot by name")
print(created_snapshot.data)
snapshot_by_name = volume.get_snapshot_by_name(created_snapshot.data["name"])
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**snapshot_by_name.data))

# Get recently created snapshot resource by uri
snapshot_by_uri = volume.get_snapshot_by_uri(created_snapshot.data["uri"])
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**snapshot_by_uri.data))

# Get a paginated list of snapshot resources sorting by name ascending
print("\nGet a list of the first 10 snapshots")
snapshots = volume.get_snapshots(0, 10, sort='name:ascending')
for snapshot in snapshots:
    print('  {name}'.format(**snapshot))

# Delete the recently created snapshot resource
print("\nDelete the recently created snapshot")
created_snapshot.delete()
print("Snapshot deleted successfully")

# Get the list of all extra managed storage volume paths from the appliance
extra_volumes = volumes.get_extra_managed_storage_volume_paths()
print("\nGet the list of all extra managed storage volume paths from the appliance")
pprint(extra_volumes)

# Remove extra presentations from the specified volume on the storage system
print("\nRemove extra presentations from the specified volume on the storage system")
volume.repair()
print("  Done.")

# Get all the attachable volumes which are managed by the appliance
print("\nGet all the attachable volumes which are managed by the appliance")
attachable_volumes = volumes.get_attachable_volumes()
pprint(attachable_volumes)

print("\nGet the attachable volumes which are managed by the appliance with scopes and connections")
scope_uris = '/rest/scopes/e4a23533-9a72-4375-8cd3-a523016df852'

connections = [{'networkUri': '/rest/fc-networks/90bd0f63-3aab-49e2-a45f-a52500b46616',
                'proxyName': '20:19:50:EB:1A:0F:0E:B6', 'initiatorName': '10:00:62:01:F8:70:00:0E'},
               {'networkUri': '/rest/fc-networks/8acd0f62-1aab-49e2-a45a-d22500b4acdb',
                'proxyName': '20:18:40:EB:1A:0F:0E:C7', 'initiatorName': '10:00:72:01:F8:70:00:0F'}]
attachable_volumes = volumes.get_attachable_volumes(scope_uris=scope_uris, connections=connections)
pprint(attachable_volumes)

print("\nDelete the recently created volumes")
new_volume.delete()
print("The volume, that was previously created with a Storage Pool, was deleted from OneView and storage system")
if unmanaged_volume_wwn:
    volume_added_with_wwn.delete(export_only=True)
    print("The volume, that was previously added using the WWN of the volume, was deleted from OneView")
