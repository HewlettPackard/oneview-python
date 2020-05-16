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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.image_streamer.resources.artifact_bundles import ArtifactBundles
from hpOneView.resources.resource import Resource, ResourceHelper, ResourceFileHandlerMixin


class ArtifactBundlesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._artifact_bundles = ArtifactBundles(self.connection)
        self.uri = "/rest/artifact-bundles/test"
        self._artifact_bundles.data = {"uri": self.uri}

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._artifact_bundles.get_all(2, 500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._artifact_bundles.get_all()
        mock_get_all.assert_called_once_with()

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_all_backups_called_once(self, mock_get_collection):
        uri = '/rest/artifact-bundles/backups'
        self._artifact_bundles.get_all_backups()
        mock_get_collection.assert_called_once_with(uri=uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_backups_by_id_called_once(self, mock_get):
        uri = '/rest/artifact-bundles/backups/test'
        self._artifact_bundles.get_backup(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceFileHandlerMixin, 'download')
    def test_download_archive_artifact_bundle_by_uri_called_once(self, mock_download):
        destination = '~/image.zip'
        expected_uri = '/rest/artifact-bundles/backups/archive/test'

        self._artifact_bundles.download_archive(destination)
        mock_download.assert_called_once_with(expected_uri, destination)

    @mock.patch.object(ResourceFileHandlerMixin, 'download')
    def test_download_called_once_by_uri(self, mock_download):
        uri = '/rest/artifact-bundles/test'
        destination = '~/image.zip'

        self._artifact_bundles.download(destination)
        mock_download.assert_called_once_with('/rest/artifact-bundles/download/test', destination)

    @mock.patch.object(Resource, 'create')
    def test_create_backup_called_once(self, mock_create):
        information = {
            "deploymentGroupURI": "/rest/deployment-groups/00c1344d-e4dd-43c3-a733-1664e159a36f"
        }
        uri = '/rest/artifact-bundles/backups'
        mock_create.return_value = {}

        self._artifact_bundles.create_backup(information)
        mock_create.assert_called_once_with(information.copy(), uri=uri, timeout=-1)

    @mock.patch.object(ResourceFileHandlerMixin, 'upload')
    def test_upload_artifact_bundle_called_once(self, mock_upload):
        filepath = "~/upload.zip"

        self._artifact_bundles.upload_bundle_from_file(filepath)
        mock_upload.assert_called_once_with(filepath)

    @mock.patch.object(ResourceFileHandlerMixin, 'upload')
    def test_upload_backup_artifact_bundle_called_once(self, mock_upload):
        filepath = "~/upload.zip"
        deployment_groups = "/rest/deployment-groups/00c1344d-e4dd-43c3-a733-1664e159a36f"
        expected_uri = '/rest/artifact-bundles/backups/archive?deploymentGrpUri=' + deployment_groups

        self._artifact_bundles.upload_backup_bundle_from_file(filepath, deployment_groups)
        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceHelper, 'update')
    def test_extract_called_once(self, mock_update):
        mock_update.return_value = {}
        resource = {}
        uri = '/rest/artifact-bundles/test?extract=true&forceImport=true'
        custom_headers = {'Content-Type': 'text/plain;charset=UTF-8'}

        self._artifact_bundles.extract(resource)
        mock_update.assert_called_once_with(resource, uri, custom_headers=custom_headers, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_extract_backup_bundle_called_once(self, mock_update):
        mock_update.return_value = {}

        data = {
            'deploymentGroupURI': '/rest/deployment-groups/00c1344d-e4dd-43c3-a733-1664e159a36f'
        }

        uri = '/rest/artifact-bundles/backups/test'

        self._artifact_bundles.extract_backup(data)
        mock_update.assert_called_once_with(data, uri, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_stop_creation_called_once(self, mock_update):
        mock_update.return_value = {}

        task_uri = "/rest/tasks/A15F9270-46FC-48DF-94A9-D11EDB52877E"

        artifact_uri = "/rest/artifact-bundles/test"
        uri = artifact_uri + '/stopArtifactCreate'

        data = {
            'taskUri': task_uri
        }

        self._artifact_bundles.stop_artifact_creation(task_uri)
        mock_update.assert_called_once_with(data, uri=uri)
