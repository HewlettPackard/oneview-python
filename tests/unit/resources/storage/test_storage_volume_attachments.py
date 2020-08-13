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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpeOneView.resources.resource import ResourceHelper, Resource


class StorageVolumeAttachmentsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._storage_volume_attachments = StorageVolumeAttachments(self.connection)
        self.uri = '/rest/storage-volume-attachments/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_volume_attachments.data = {'uri': self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_volume_attachments.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, filter='name=TestName',
                                             sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_volume_attachments.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter=u'', sort=u'', start=0)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_extra_unmanaged_storage_volumes_called_once(self, mock_get):
        storage_volume_attachments_host_types_uri = \
            "/rest/storage-volume-attachments/repair?alertFixType=ExtraUnmanagedStorageVolumes"
        self._storage_volume_attachments.get_extra_unmanaged_storage_volumes()
        mock_get.assert_called_once_with(count=-1, filter=u'', sort=u'', start=0,
                                         uri=storage_volume_attachments_host_types_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_paths_called_once(self, mock_get):
        storage_volume_attachments_paths_uri = "{}/paths".format(self.uri)
        self._storage_volume_attachments.get_paths()
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_paths_called_once_with_path_id(self, mock_get):
        path_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_volume_attachments_paths_uri = "{}/paths/C862833E-907C-4124-8841-BDC75444CF76".format(self.uri)
        self._storage_volume_attachments.get_paths(path_id)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_remove_extra_presentations_called_once_with_defaults(self, mock_create):
        info = {
            "type": "ExtraUnmanagedStorageVolumes",
            "resourceUri": self.uri
        }
        self._storage_volume_attachments.remove_extra_presentations(info)
        mock_create.assert_called_once_with(
            info, uri='/rest/storage-volume-attachments/repair', timeout=-1,
            custom_headers={'Accept-Language': 'en_US'})

    @mock.patch.object(ResourceHelper, 'create')
    def test_remove_extra_presentations_called_once(self, mock_create):
        info = {
            "type": "ExtraUnmanagedStorageVolumes",
            "resourceUri": self.uri
        }
        self._storage_volume_attachments.remove_extra_presentations(info, 70)
        mock_create.assert_called_once_with(
            info, uri='/rest/storage-volume-attachments/repair', timeout=70,
            custom_headers={'Accept-Language': 'en_US'})

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._storage_volume_attachments.get_by("name", "test name")
        mock_get_by.assert_called_once_with("name", "test name")
