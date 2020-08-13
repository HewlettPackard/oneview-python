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

from hpeOneView.connection import connection
from hpeOneView.resources.settings.backups import Backups
from hpeOneView.resources.resource import ResourceClient


class BackupsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = Backups(self.connection)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_all_called_once(self, mock_get_collection):
        self._client.get_all()

        mock_get_collection.assert_called_once_with('/rest/backups')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('appliance_backup_2017-04-20_180138')

        mock_get.assert_called_once_with('appliance_backup_2017-04-20_180138')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/backups/appliance_backup_2017-04-20_180138'

        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_create_called_once(self, mock_create):
        mock_create.return_value = {}

        self._client.create()

        mock_create.assert_called_once_with(timeout=-1)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_called_once_by_id(self, mock_download):
        download_uri = '/rest/backups/archive/appliance_backup_2017-04-20_182809'
        destination = 'appliance_backup_2017-04-20_180138.bkp'

        self._client.download(download_uri, destination)

        mock_download.assert_called_once_with('/rest/backups/archive/appliance_backup_2017-04-20_182809', destination)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_artifact_bundle_called_once(self, mock_upload):
        filepath = "appliance_backup_2017-04-20_182809.bkp"

        self._client.upload(filepath)

        mock_upload.assert_called_once_with(filepath, '/rest/backups/archive')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_config_called_once(self, mock_get):
        self._client.get_config()

        mock_get.assert_called_once_with('config')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_config_called_once(self, mock_update):
        options = {"enabled": False}

        self._client.update_config(options, timeout=30)

        mock_update.assert_called_once_with(options, uri='/rest/backups/config', timeout=30)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_remote_archive_called_once(self, mock_update):
        save_uri = '/rest/backups/remotearchive/appliance_backup_2017-04-20_182809'

        self._client.update_remote_archive(save_uri, timeout=30)

        mock_update.update_with_zero_body(uri=save_uri, timeout=30)
