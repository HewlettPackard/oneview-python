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

from hpOneView.connection import connection
from hpOneView.resources.storage.storage_pools import StoragePools
from hpOneView.resources.resource import ResourceClient


class StoragePoolsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._storage_pools = StoragePools(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_pools.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_pools.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        storage_pools_id = "EE9326ED-4595-4828-B411-FE3BD6BA7E9D"
        self._storage_pools.get(storage_pools_id)
        mock_get.assert_called_once_with(storage_pools_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        storage_pools_uri = "/rest/storage-pools/EE9326ED-4595-4828-B411-FE3BD6BA7E9D"
        self._storage_pools.get(storage_pools_uri)
        mock_get.assert_called_once_with(storage_pools_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        storage_pool = {
            "storageSystemUri": "/rest/storage-systems/111111",
            "poolName": "storagepool1"
        }
        self._storage_pools.add(storage_pool)
        mock_create.assert_called_once_with(storage_pool, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once(self, mock_create):
        storage_pool = {
            "storageSystemUri": "/rest/storage-systems/111111",
            "poolName": "storagepool1"
        }
        self._storage_pools.add(storage_pool, 70)
        mock_create.assert_called_once_with(storage_pool, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_pools.remove(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_pools.remove(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._storage_pools.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        storage_pool = {
            "name": "SSD",
            "uri": "rest/fake/pool",
            "raidLevel": "RAID5"
        }
        self._storage_pools.update(storage_pool, 70)
        mock_update.assert_called_once_with(storage_pool, timeout=70)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_reachable_storage_pools_called_once(self, mock_get):
        query_params = "networks='/rest/networks/fake'&scopeExclusions=/rest/scope/fake"
        uri = "/rest/storage-pools/reachable-storage-pools?" + query_params + "&start=0&count=-1"
        self._storage_pools.get_reachable_storage_pools(networks=['/rest/networks/fake'],
                                                        scope_exclusions=['/rest/scope/fake'])
        mock_get.assert_called_once_with(uri)
