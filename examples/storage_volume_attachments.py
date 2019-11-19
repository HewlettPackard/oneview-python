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
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run all parts of this example, a server profile uri, volume uri, volume attachment id and
# path id must be defined.
serverProfileUri = None
storageVolumeUri = None
attachment_id = None
path_id = None

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all volume attachments
print("\nGet all volume attachments")
volume_attachments = oneview_client.storage_volume_attachments.get_all()
for attachment in volume_attachments:
    print('\n#### Storage Volume Attachment info:')
    pprint(attachment)

# Get all storage volume attachments filtering by storage volume URI
try:
    print("\nGet all storage volume attachments filtering by storage volume URI")
    filter = "storageVolumeUri='{}'".format(storageVolumeUri)
    volume_attachments_filtered = oneview_client.storage_volume_attachments.get_all(filter=filter)
    for attachment in volume_attachments_filtered:
        print('\n#### Storage Volume Attachment info:')
        pprint(attachment)
except HPOneViewException as e:
    print(e.msg)

# Get the list of extra unmanaged storage volumes
print("\nGet the list of extra unmanaged storage volumes")
unmanaged_storage_volumes = oneview_client.storage_volume_attachments.get_extra_unmanaged_storage_volumes()
pprint(unmanaged_storage_volumes)

# Removes extra presentations from a specified server profile.
try:
    info = {
        "type": "ExtraUnmanagedStorageVolumes",
        "resourceUri": serverProfileUri
    }
    print("\nRemoves extra presentations from a specified server profile at uri: '{}".format(serverProfileUri))
    oneview_client.storage_volume_attachments.remove_extra_presentations(info)
    print("   Done.")
except HPOneViewException as e:
    print(e.msg)

# Get storage volume attachment by id
try:
    print("\nGet storage volume attachment by id: '{}'".format(attachment_id))
    volume_attachment_byid = oneview_client.storage_volume_attachments.get(attachment_id)
    print('\n#### Storage Volume Attachment info:')
    pprint(attachment)
except HPOneViewException as e:
    print(e.msg)

if volume_attachments:
    # Get storage volume attachment by uri
    print("\nGet storage volume attachment by uri: '{uri}'".format(**volume_attachments[0]))
    volume_attachment_byid = oneview_client.storage_volume_attachments.get(volume_attachments[0]['uri'])
    print('\n#### Storage Volume Attachment info:')
    pprint(attachment)

    if oneview_client.api_version < 500:
        # Get all volume attachment paths
        print("\nGet all volume attachment paths for volume attachment at uri: {uri}".format(**volume_attachment_byid))
        paths = oneview_client.storage_volume_attachments.get_paths(volume_attachment_byid['uri'])
        for path in paths:
            print("   Found path at uri: {uri}".format(**path))

        if paths:
            # Get specific volume attachment path by uri
            print("\nGet specific volume attachment path by uri")
            path_byuri = oneview_client.storage_volume_attachments.get_paths(
                volume_attachment_byid['uri'], paths[0]['uri'])
            pprint(path_byuri)

# Get volume attachment path by id
if path_id and oneview_client.api_version < 500:
    try:
        print("\nGet volume attachment path by id: '{}'\n  at attachment with id: '{}'".format(path_id, attachment_id))
        path_byid = oneview_client.storage_volume_attachments.get_paths(attachment_id, path_id)
        pprint(path_byid)
    except HPOneViewException as e:
        print(e.msg)
