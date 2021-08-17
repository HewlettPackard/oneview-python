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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.resource import ResourceHelper, Resource
from hpeOneView.resources.storage.volumes import VolumeSnapshots, Volumes


class VolumesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._volumes = Volumes(self.connection)
        self.resource_uri = '/rest/storage-volumes/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._volumes.data = {'uri': self.resource_uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._volumes.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, filter='name=TestName',
                                             sort='name:ascending', start=2)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._volumes.get_by('name', 'Test Volume')

        mock_get_by.assert_called_once_with('name', 'Test Volume')

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        resource = {
            'name': 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1'
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._volumes.create(resource)
        mock_create.assert_called_once_with(resource_rest_call, None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'update')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once(self, mock_get, mock_update):
        resource = {
            'uri': '/rest/storage-volumes/3518be0e-17c1-4189-8f81-83f3724f6155',
            'name': 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1'
        }
        resource_rest_call = resource.copy()

        self._volumes.update(resource)

        mock_update.assert_called_once_with(resource_rest_call,
                                            self.resource_uri, False, -1, None)

    @mock.patch.object(ResourceHelper, 'update')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once_with_force(self, mock_get, mock_update):
        resource = {
            'uri': '/rest/storage-volumes/3518be0e-17c1-4189-8f81-83f3724f6155',
            'name': 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1'
        }
        resource_rest_call = resource.copy()

        self._volumes.update(resource, force=True)

        mock_update.assert_called_once_with(resource_rest_call,
                                            self.resource_uri, True, -1, None)

    @mock.patch(VolumeSnapshots, 'delete')
    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_by_id_called_once(self, mock_delete, mock_snapshot_delete):
        mock_snapshot_delete.return_value = None
        self._volumes.delete(force=False, timeout=-1)

        expected_headers = {"If-Match": '*'}
        mock_delete.assert_called_once_with(self.resource_uri, force=False,
                                            timeout=-1, custom_headers=expected_headers)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_by_resource_called_once(self, mock_delete):
        expected_headers = {"If-Match": '*'}
        self._volumes.delete()
        mock_delete.assert_called_once_with(self.resource_uri, force=False,
                                            timeout=-1, custom_headers=expected_headers)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_with_force_called_once(self, mock_delete):
        self._volumes.delete(force=True)

        mock_delete.assert_called_once_with(mock.ANY, force=True, timeout=mock.ANY, custom_headers=mock.ANY)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_only_from_oneview_called_once_api300(self, mock_delete):
        self._volumes.delete(export_only=True)

        expected_headers = {'If-Match': '*', "exportOnly": True}
        mock_delete.assert_called_once_with(self.resource_uri, force=mock.ANY,
                                            timeout=mock.ANY, custom_headers=expected_headers)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_only_from_oneview_called_once_api500(self, mock_delete):
        extended_uri = '{}?suppressDeviceUpdates=true'.format(self.resource_uri)
        self._volumes.delete(suppress_device_updates=True)

        expected_headers = {'If-Match': '*'}
        mock_delete.assert_called_once_with(extended_uri, force=mock.ANY,
                                            timeout=mock.ANY, custom_headers=expected_headers)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_snapshots_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self._volumes.get_snapshots(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(count=500, filter='name=TestName', sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_snapshots_called_once_with_default(self, mock_get_all):
        self._volumes.get_snapshots()
        mock_get_all.assert_called_once_with(count=-1, filter=u'', sort=u'', start=0)

    @mock.patch.object(ResourceHelper, 'create')
    @mock.patch.object(ResourceHelper, 'get_all')
    def test_create_snapshot_should_be_called_once(self, mock_get, mock_create):
        resource = {
            'name': 'OneViewSDK Test Snapshot',
        }

        self._volumes.create_snapshot(resource, 20)
        mock_create.assert_called_once_with(resource, None, 20, None, False)

    @mock.patch.object(Resource, 'get_by')
    def test_get_snapshot_by_called_once(self, mock_get_by):
        self._volumes.get_snapshot_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_snapshot_by_uri_called_once(self, mock_get_by_uri):
        uri = "/rest/storage-volumes/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/snapshots/23"
        self._volumes.get_snapshot_by_uri(uri)

        mock_get_by_uri.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by')
    def test_get_snapshot_by_name_called_once(self, mock_get_by):
        self._volumes.get_snapshot_by_name("test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_extra_managed_storage_volume_paths_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._volumes.get_extra_managed_storage_volume_paths(2, 500, filter, sort)

        expected_uri = '/rest/storage-volumes/repair?alertFixType=ExtraManagedStorageVolumePaths'
        mock_get_all.assert_called_once_with(2, 500, uri=expected_uri, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'create')
    def test_repair_called_once(self, mock_create):
        data = {
            'resourceUri': self.resource_uri,
            'type': 'ExtraManagedStorageVolumePaths'
        }
        self._volumes.repair()

        custom_headers = {u'Accept-Language': u'en_US'}
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/repair', timeout=-1,
                                            custom_headers=custom_headers)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_attachable_volumes_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        query = 'availableNetworks IN [/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]'
        scope_uris = ['/rest/scopes/e4a23533-9a72-4375-8cd3-a523016df852',
                      '/rest/scopes/7799327d-6d79-4eb2-b969-a523016df869']
        connections = [{'networkUri': '/rest/fc-networks/90bd0f63-3aab-49e2-a45f-a52500b46616'},
                       {'networkUri': '/rest/fc-networks/8acd0f62-1aab-49e2-a45a-d22500b4acdb'}]

        self._volumes.get_attachable_volumes(2, 500, filter, query, sort, scope_uris, connections)

        expected_uri = "/rest/storage-volumes/attachable-volumes?connections="\
                       "[{'networkUri':'/rest/fc-networks/90bd0f63-3aab-49e2-a45f-a52500b46616'},"\
                       "{'networkUri':'/rest/fc-networks/8acd0f62-1aab-49e2-a45a-d22500b4acdb'}]"
        mock_get_all.assert_called_once_with(2, 500, uri=expected_uri, filter=filter, query=query, sort=sort,
                                             scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_attachable_volumes_called_with_default_values(self, mock_get_all):
        self._volumes.get_attachable_volumes()

        expected_uri = '/rest/storage-volumes/attachable-volumes'
        mock_get_all.assert_called_once_with(0, -1, uri=expected_uri, filter='', query='', sort='', scope_uris='')

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_from_snapshot_called_once(self, mock_create):
        data = {
            'fake': 'data'
        }
        self._volumes.create_from_snapshot(data)
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/from-snapshot', timeout=-1)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_from_existing_called_once(self, mock_create):
        data = {
            'fake': 'data'
        }
        self._volumes.add_from_existing(data)
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/from-existing', timeout=-1)
