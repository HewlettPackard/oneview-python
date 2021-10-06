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
VOLUMEs = oneview_client.VOLUMEs
fc_networks = oneview_client.fc_networks
STORAGE_SYSTEMs = oneview_client.STORAGE_SYSTEMs
storage_pools = oneview_client.storage_pools
storage_VOLUME_TEMPLATEs = oneview_client.storage_VOLUME_TEMPLATEs
scopes = oneview_client.scopes

# To run this example, you may set a WWN to add a VOLUME using the WWN of the VOLUME (optional)
UNMANAGED_VOLUME_WWN = ''
SCOPE_NAME = 'SampleScope'

# Defines the storage system and the storage pool which are provided to create the VOLUMEs
STORAGE_SYSTEM = STORAGE_SYSTEMs.get_all()[0]
FC_NETWORK_URI = fc_networks.get_all()[0]['uri']
STORAGE_POOLS_ALL = storage_pools.get_all(filter="\"'isManaged'='True'\"")
STORAGE_POOL_AVAILABLE = False

for sp in STORAGE_POOLS_ALL:
    if sp['storageSystemUri'] == STORAGE_SYSTEM['uri']:
        STORAGE_POOL_AVAILABLE = True
        storage_pool = sp

if not STORAGE_POOL_AVAILABLE:
    raise ValueError("ERROR: No storage pools found attached to the storage system")

VOLUME_TEMPLATE = storage_VOLUME_TEMPLATEs.get_all()[0]

# Create a VOLUME with a Storage Pool
print("\nCreate a VOLUME with a specified Storage Pool and Snapshot Pool")

OPTIONS = {
    "properties": {
        "storagePool": storage_pool['uri'],
        "size": 1024 * 1024 * 1024,  # 1GB
        "isShareable": False,
        "snapshotPool": storage_pool['uri'],
        "provisioningType": "Thin",
        "name": "Test_VOLUME"
    },
    "templateUri": VOLUME_TEMPLATE['uri'],
    "isPermanent": False
}

# Find a VOLUME by name
VOLUME = VOLUMEs.get_by_name(OPTIONS['properties']['name'])

if not VOLUME:
    VOLUME = VOLUMEs.create(OPTIONS)
    print("\nCreated a VOLUME by name: '{name}'.\n  uri = '{uri}'".format(**VOLUME.data))
else:
    print("\nFound a VOLUME by name: '{name}'.\n  uri = '{uri}'".format(**VOLUME.data))

# Add a VOLUME for management by the appliance using the WWN of the VOLUME
if UNMANAGED_VOLUME_WWN:
    print("\nAdd a VOLUME for management by the appliance using the WWN of the VOLUME")

    OPTIONS_WITH_WWN = {
        "type": "AddStorageVolumeV2",
        "name": 'ONEVIEW_SDK_TEST_VOLUME_TYPE_4',
        "description": 'Test VOLUME added for management: Storage System + Storage Pool + WWN',
        "storageSystemUri": STORAGE_SYSTEM['uri'],
        "wwn": UNMANAGED_VOLUME_WWN,
        "provisioningParameters": {
            "shareable": False
        }
    }
    VOLUME_ADDED_WITH_WWN = VOLUMEs.create(OPTIONS_WITH_WWN)
    pprint(VOLUME_ADDED_WITH_WWN.data)

# Get all managed VOLUMEs
print("\nGet a list of all managed VOLUMEs")
VOLUMES_ALL = VOLUMEs.get_all()
for VOLUME_each in VOLUMES_ALL:
    print("Name: {name}".format(**VOLUME_each))

# Update the name of the VOLUME recently found to 'Test_VOLUME'
if VOLUME:
    VOLUME_DATA = VOLUME.data.copy()
    VOLUME_DATA['name'] = 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
    VOLUME.update(VOLUME_DATA)
    print("\nVolume updated successfully.\n  uri = '{uri}'\n  with attribute 'name' =
	 {name}".format(**VOLUME.data))

# Find a VOLUME by URI
VOLUME = VOLUMEs.get_by_uri(VOLUME.data["uri"])
print("\nFind a VOLUME by URI")
pprint(VOLUME.data)

# Create a snapshot
print("\nCreate a snapshot")
SNAPSHOT_OPTIONS = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot"
}
if VOLUME:
    CREATED_SNAPSHOT = VOLUME.create_snapshot(SNAPSHOT_OPTIONS)
    print("Created a snapshot for the VOLUME '{name}'".format(**VOLUME.data))

# Get recently created snapshot resource by name
print("\nGet a snapshot by name")
if VOLUME and CREATED_SNAPSHOT:
    print(CREATED_SNAPSHOT.data)
    SNAPSHOT_BY_NAME = VOLUME.get_SNAPSHOT_BY_NAME(CREATED_SNAPSHOT.data["name"])
    print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**SNAPSHOT_BY_NAME.data))

# Get recently created snapshot resource by uri
if VOLUME and CREATED_SNAPSHOT:
    SNAPSHOT_BY_URI = VOLUME.get_SNAPSHOT_BY_URI(CREATED_SNAPSHOT.data["uri"])
    print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**SNAPSHOT_BY_URI.data))

# Get a paginated list of snapshot resources sorting by name ascending
print("\nGet a list of the first 10 SNAPSHOTS")
if VOLUME:
    SNAPSHOTS = VOLUME.get_SNAPSHOTS(0, 10, sort='name:ascending')
    for snapshot in SNAPSHOTS:
        print('  {name}'.format(**snapshot))

# Delete the recently created snapshot resource
print("\nDelete the recently created snapshot")
if CREATED_SNAPSHOT:
    CREATED_SNAPSHOT.delete()
    print("Snapshot deleted successfully")

# Get the list of all extra managed storage VOLUME paths from the appliance
EXTRA_VOLUMES = VOLUMEs.get_extra_managed_storage_VOLUME_paths()
print("\nGet the list of all extra managed storage VOLUME paths from the appliance")
pprint(EXTRA_VOLUMES)

# Remove extra presentations from the specified VOLUME on the storage system
print("\nRemove extra presentations from the specified VOLUME on the storage system")
if VOLUME:
    VOLUME.repair()
    print("  Done.")

# Get all the attachable VOLUMEs which are managed by the appliance
print("\nGet all the attachable VOLUMEs which are managed by the appliance")
ATTACHABLE_VOLUMES = VOLUMEs.get_ATTACHABLE_VOLUMES()
pprint(ATTACHABLE_VOLUMES)

print("\nGet the attachable VOLUMEs which are managed by the appliance with scopes and CONNECTIONS")
SCOPE_URIS = scopes.get_by_name(SCOPE_NAME).data['uri']

CONNECTIONS = [{'networkUri': FC_NETWORK_URI,
                'proxyName': '20:18:40:EB:1A:0F:0E:C7', 'initiatorName': '10:00:72:01:F8:70:00:0F'}]
ATTACHABLE_VOLUMES = VOLUMEs.get_ATTACHABLE_VOLUMES(SCOPE_URIS=SCOPE_URIS, CONNECTIONS=CONNECTIONS)
pprint(ATTACHABLE_VOLUMES)

print("\nDelete the recently created VOLUMEs")
if VOLUME:
    VOLUME.delete()
    print("The VOLUME, that was previously created with a Storage Pool, was deleted from OneView and
	 storage system")
if UNMANAGED_VOLUME_WWN:
    VOLUME_ADDED_WITH_WWN.delete(export_only=True)
    print("The VOLUME, that was previously added using the WWN of the VOLUME, was deleted from
	 OneView")

# Create VOLUME for automation
NEW_VOLUME = VOLUMEs.create(OPTIONS)
print("Created VOLUME '{}' with uri '{}'".format(NEW_VOLUME.data['name'], NEW_VOLUME.data['uri']))
