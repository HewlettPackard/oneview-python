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
volume_attachments = oneview_client.storage_volume_attachments
volumes = oneview_client.volumes
server_profiles = oneview_client.server_profiles

# variable definitions
SP_NAME = "TestProfile"
VOLUME_NAME = "Test_volume"

# To run all parts of this example, a server profile uri, volume uri, volume attachment id and
# path id must be defined.
SERVERPROFILEURI = server_profiles.get_by_name(SP_NAME).data['uri']
STORAGEVOLUMEURI = volumes.get_by_name(VOLUME_NAME).data['uri']

# Get all volume attachments
print("\nGet all volume attachments")
VOLUME_ATTACHMENTS_ALL = volume_attachments.get_all()
for attachment in VOLUME_ATTACHMENTS_ALL:
    print('\n#### Storage Volume Attachment INFO:')
    pprint(attachment)

# Get all storage volume attachments FILTERing by storage volume URI
try:
    print("\nGet all storage volume attachments FILTERing by storage volume URI")
    FILTER = "STORAGEVOLUMEURI='{}'".format(STORAGEVOLUMEURI)
    VOLUME_ATTACHMENTS_FILTERED = volume_attachments.get_all(FILTER=FILTER)
    for attachment in VOLUME_ATTACHMENTS_FILTERED:
        print('\n#### Storage Volume Attachment INFO:')
        pprint(attachment)
except HPEOneViewException as e:
    print(e.msg)

# Get the list of extra unmanaged storage volumes
print("\nGet the list of extra unmanaged storage volumes")
UNMANAGED_STORAGE_VOLUMES = volume_attachments.get_extra_UNMANAGED_STORAGE_VOLUMES()
pprint(UNMANAGED_STORAGE_VOLUMES)

# Removes extra presentations from a specified server profile.
try:
    INFO = {
        "type": "ExtraUnmanagedStorageVolumes",
        "resourceUri": SERVERPROFILEURI
    }
    print("\nRemoves extra presentations from a specified server profile at uri:
	 '{}".format(SERVERPROFILEURI))
    volume_attachments.remove_extra_presentations(INFO)
    print("   Done.")
except HPEOneViewException as e:
    print(e.msg)

if len(VOLUME_ATTACHMENTS_ALL) != 0:
    # Get storage volume attachment by uri
    print("\nGet storage volume attachment by uri: '{uri}'".format(**VOLUME_ATTACHMENTS_ALL[0]))
    VOLUME_ATTACHMENT_BYID = volume_attachments.get_by_uri(VOLUME_ATTACHMENTS_ALL[0]['uri'])
    print('\n#### Storage Volume Attachment INFO:')
    pprint(VOLUME_ATTACHMENT_BYID.data)

    if oneview_client.api_version < 500:
        # Get all volume attachment PATHS
        print("\nGet all volume attachment PATHS for volume attachment at uri:
	 {uri}".format(**VOLUME_ATTACHMENT_BYID.data))
        PATHS = VOLUME_ATTACHMENT_BYID.get_PATHS()
        for path in PATHS:
            print("   Found path at uri: {uri}".format(**path))

        if PATHS:
            # Get specific volume attachment path by uri
            print("\nGet specific volume attachment path by uri")
            PATH_BYURI = VOLUME_ATTACHMENT_BYID.get_PATHS(PATHS[0]['uri'])
            pprint(PATH_BYURI)
