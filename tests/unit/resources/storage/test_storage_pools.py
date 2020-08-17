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
from hpOneView.resources.resource import ResourceHelper


class StoragePoolsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._storage_pools = StoragePools(self.connection)
        self.uri = '/rest/storage-pools/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_pools.data = {'uri': self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_pools.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(count=500, filter='name=TestName', sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_pools.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter='', sort='', start=0)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        storage_pool = {
            "storageSystemUri": "/rest/storage-systems/111111",
            "poolName": "storagepool1"
        }
        self._storage_pools.add(storage_pool)
        mock_create.assert_called_once_with(storage_pool, None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once(self, mock_create):
        storage_pool = {
            "storageSystemUri": "/rest/storage-systems/111111",
            "poolName": "storagepool1"
        }
        self._storage_pools.add(storage_pool, 70)
        mock_create.assert_called_once_with(storage_pool, None, 70, None, False)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._storage_pools.remove(force=True, timeout=50)

        mock_delete.assert_called_once_with('/rest/storage-pools/ad28cf21-8b15-4f92-bdcf-51cb2042db32',
                                            custom_headers=None, force=True, timeout=50)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        self._storage_pools.remove()

        mock_delete.assert_called_once_with('/rest/storage-pools/ad28cf21-8b15-4f92-bdcf-51cb2042db32',
                                            custom_headers=None, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once(self, mock_get, mock_update):
        storage_pool = {
            "name": "SSD",
            "raidLevel": "RAID5",
            "uri": self.uri
        }
        mock_get.return_value = storage_pool

        self._storage_pools.update(storage_pool, 70)
        mock_update.assert_called_once_with(storage_pool,
                                            self.uri,
                                            False, 70, None)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_reachable_storage_pools_called_once(self, mock_get):
        query_params = "networks='/rest/networks/fake'&scopeExclusions=/rest/scope/fake"
        uri = "/rest/storage-pools/reachable-storage-pools?" + query_params + "&start=0&count=-1"
        self._storage_pools.get_reachable_storage_pools(networks=['/rest/networks/fake'],
                                                        scope_exclusions=['/rest/scope/fake'])
        mock_get.assert_called_once_with(uri)
