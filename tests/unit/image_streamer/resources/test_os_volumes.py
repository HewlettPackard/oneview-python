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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.image_streamer.resources.os_volumes import OsVolumes
from hpOneView.resources.resource import ResourceClient


class OsVolumesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = OsVolumes(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('57f2d803-9c11-4f9a-bc02-71804a0fcc3e')

        mock_get.assert_called_once_with(
            '57f2d803-9c11-4f9a-bc02-71804a0fcc3e')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'OSVolume-5')

        mock_get_by.assert_called_once_with(
            'name', 'OSVolume-5')

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name_called_once(self, mock_get_by):
        self._client.get_by_name('OSVolume-5')

        mock_get_by.assert_called_once_with('OSVolume-5')

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_id(self, mock_download):
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'

        self._client.download_archive(id, "~/archive.log")

        mock_download.assert_called_once_with('/rest/os-volumes/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              '~/archive.log')

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_uri(self, mock_download):
        name = "fake"
        uri = '/rest/os-volumes/archive/fake'

        self._client.download_archive(name, "~/archive.log")
        mock_download.assert_called_once_with(uri, '~/archive.log')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_storage(self, mock_get):
        volume_id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        self._client.get_storage(volume_id)
        mock_get.assert_called_once_with('/rest/os-volumes/3518be0e-17c1-4189-8f81-83f3724f6155/storage')
