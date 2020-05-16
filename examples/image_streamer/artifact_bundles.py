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

import os
from pprint import pprint
from hpOneView.oneview_client import OneViewClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config.json')

oneview_client = OneViewClient.from_json_file(EXAMPLE_CONFIG_FILE)
image_streamer_client = oneview_client.create_image_streamer_client()
artifact_bundles = image_streamer_client.artifact_bundles

artifact_bundles_to_be_created = {
    "name": "Artifact Bundles Test",
    "description": "Description of Artifact Bundles Test",
    "buildPlans": [
        {
            "resourceUri": "/rest/build-plans/81088ef9-631d-4c5c-9de1-026afa234bc8",
            "readOnly": "false"
        }
    ]
}

artifact_bundles_deployment_group = {
    "deploymentGroupURI": "/rest/deployment-groups/2117634b-d911-4673-98ac-1a7e19f3b40f"
}

artifact_bundle_file_path = {
    "download": "./artifact_bundle.zip",
    "download_archive": "./archive.zip",
    "upload": "./artifact_bundle.zip",
    "upload_backup": "./archive.zip"
}

artifact_bundle_new_name = "Artifact Bundles Test Updated"

# Get all Artifacts Bundle
print("\nGet all Artifact Bundles")
all_artifact_bundles = artifact_bundles.get_all()
for artifacts_bundle in all_artifact_bundles:
    print(" - {}".format(artifacts_bundle['name']))

# Get the Artifacts Bundle by Name
print("\nGet Artifact Bundles by Name")
artifact_bundle = artifact_bundles.get_by_name(artifact_bundles_to_be_created['name'])

if artifact_bundle:
    print("Found artifact bundle with name- {} and uri- {}".format(artifact_bundle.data['name'], artifact_bundle.data['uri']))
else:
    # Create an Artifact Bundle
    print("\nCreate an Artifact Bundle")
    artifact_bundle = artifact_bundles.create(artifact_bundles_to_be_created)
    print("Created artifact bundle with name- {} and uri- {}".format(artifact_bundle.data['name'], artifact_bundle.data['uri']))

# Get the Artifacts Bundle by uri
print("\nGet the Artifact Bundle by uri")
ab_by_uri = artifact_bundles.get_by_uri(artifact_bundle.data['uri'])
print(ab_by_uri.data)

# Download the Artifact Bundle
print("\nDownload the Artifact Bundle")
response = artifact_bundle.download(artifact_bundle_file_path['download'])
print(response)

# Update name of an Artifact Bundle
print("\nUpdate an Artifact Bundle")
data_to_update = {'name': artifact_bundle_new_name}
artifact_bundle.update(data=data_to_update)
pprint(artifact_bundle.data)

# Extract an Artifact Bundle
print("\nExtract an Artifact Bundle")
response = artifact_bundle.extract()
pprint(response)

# Delete an Artifact Bundle
print("\nDelete an Artifact Bundle")
artifact_bundle.delete()

# Create a Backup for all the Artifact Bundle
print("\nCreate a Backup for all Artifact Bundles")
ab_backup = artifact_bundles.create_backup(artifact_bundles_deployment_group)
print(ab_backup.data)

# Get all Backups Bundles
print("\nGet all Backups Bundles")
backup_artifact_bundles = artifact_bundles.get_all_backups()
for backup in backup_artifact_bundles:
    print(" - {}".format(backup['name']))

# Get Backup Bundle
print("\nGet Backup Bundle")
ab_bkp = artifact_bundles.get_backup(backup_artifact_bundles[0]['uri'])
pprint(ab_bkp.data)

# Extract an Artifact Bundle from backup
print("\nExtract an Artifact Bundle from Backup")
response = ab_bkp.extract_backup(artifact_bundles_deployment_group)
pprint(response)

# Download the backup archive of the Artifact Bundle
print("\nDownload the backup archive of the Artifact Bundle")
response = ab_bkp.download_archive(artifact_bundle_file_path['download_archive'])
print(response)

# Upload an Artifact Bundle from file
print("\nUpload an Artifact Bundle from file")
response = artifact_bundles.upload_bundle_from_file(artifact_bundle_file_path['upload'])
pprint(response)

# Upload a Backup of Artifact Bundle from file
print("\nUpload a Backup of Artifact Bundle from file")
res = artifact_bundles.upload_backup_bundle_from_file(artifact_bundle_file_path['upload_backup'], artifact_bundles_deployment_group['deploymentGroupURI'])
pprint(res)
