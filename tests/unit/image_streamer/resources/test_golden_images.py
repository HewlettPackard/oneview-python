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
from hpOneView.image_streamer.resources.golden_images import GoldenImages
from hpOneView.resources.resource import ResourceClient


class GoldenImagesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = GoldenImages(self.connection)

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

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'GoldenImage')

        mock_get_by.assert_called_once_with(
            'name', 'GoldenImage')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        information = {
            "type": "GoldenImage",
            "description": "Description of this Golden Image",
        }
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(information.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        information = {
            "type": "GoldenImage",
            "description": "Description of this Golden Image",
        }
        mock_update.return_value = {}

        self._client.update(information)
        mock_update.assert_called_once_with(information.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=True)

        mock_delete.assert_called_once_with(id, force=True, timeout=-1)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_post_multipart_called_once(self, mock_upload):
        information = {
            "name": "GoldenImageName",
            "description": "Description of this Golden Image",
        }
        filepath = "test/SPPgen9snap6.2015_0405.81.iso"

        self._client.upload(filepath, information)

        expected_uri = '/rest/golden-images?name=GoldenImageName&description=Description%20of%20this%20Golden%20Image'

        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_without_description(self, mock_upload):
        information = {
            "name": "GoldenImageName",
        }

        filepath = "test/SPPgen9snap6.2015_0405.81.iso"

        self._client.upload(filepath, information)

        expected_uri = '/rest/golden-images?name=GoldenImageName&description='

        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_with_empty_information(self, mock_upload):
        information = {}
        filepath = "test/SPPgen9snap6.2015_0405.81.iso"

        self._client.upload(filepath, information)

        expected_uri = '/rest/golden-images?name=&description='

        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_id(self, mock_download):
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download_archive(id, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_uri(self, mock_download):
        uri = '/rest/golden-images/3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download_archive(uri, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_called_once_with_uri(self, mock_download):
        uri = '/rest/golden-images/3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download(uri, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/download/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_called_once_with_id(self, mock_download):
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download(id, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/download/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)
