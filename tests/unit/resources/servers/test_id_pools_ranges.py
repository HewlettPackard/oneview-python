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
import mock

from hpOneView import HPOneViewValueError
from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.servers.id_pools_ranges import IdPoolsRanges
import unittest


class TestIdPoolsRanges(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.id_pool_name = 'vsn'
        self.client = IdPoolsRanges(self.id_pool_name, self.connection)
        self.example_uri = "/rest/id-pools/" + self.id_pool_name + "/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"

    @mock.patch.object(ResourceClient, '__init__')
    def test_id_pools_ranges_constructor_with_type_vsn(self, mock_rclient):
        mock_rclient.return_value = None
        IdPoolsRanges('vsn', self.connection)
        mock_rclient.assert_called_once_with(self.connection, '/rest/id-pools/vsn/ranges')

    @mock.patch.object(ResourceClient, '__init__')
    def test_id_pools_ranges_constructor_with_type_vwwn(self, mock_rclient):
        mock_rclient.return_value = None
        IdPoolsRanges('vwwn', self.connection)
        mock_rclient.assert_called_once_with(self.connection, '/rest/id-pools/vwwn/ranges')

    @mock.patch.object(ResourceClient, '__init__')
    def test_id_pools_ranges_constructor_with_type_vmac(self, mock_rclient):
        mock_rclient.return_value = None
        IdPoolsRanges('vmac', self.connection)
        mock_rclient.assert_called_once_with(self.connection, '/rest/id-pools/vmac/ranges')

    @mock.patch.object(ResourceClient, '__init__')
    def test_id_pools_ranges_constructor_with_invalid_type(self, mock_rclient):
        mock_rclient.return_value = None
        self.assertRaises(HPOneViewValueError, IdPoolsRanges, 'invalid', self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        self.client.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id_pools_range_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get(id_pools_range_id)
        mock_get.assert_called_once_with(id_pools_range_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        self.client.get(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_enable_called_once(self, update):
        self.client.enable(self.resource_info.copy(), self.example_uri)
        update.assert_called_once_with(self.resource_info.copy(), self.example_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get):
        self.client.get_allocated_fragments(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + "/allocated-fragments?start=0&count=-1")

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_allocated_fragments_called_once(self, mock_get):
        self.client.get_allocated_fragments(self.example_uri, 5, 2)
        mock_get.assert_called_once_with(self.example_uri + "/allocated-fragments?start=2&count=5")

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_free_fragments_called_once_with_defaults(self, mock_get):
        self.client.get_free_fragments(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + "/free-fragments?start=0&count=-1")

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_free_fragments_called_once(self, mock_get):
        self.client.get_free_fragments(self.example_uri, 5, 3)
        mock_get.assert_called_once_with(self.example_uri + "/free-fragments?start=3&count=5")

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.client.delete({'uri': '/rest/uri'}, force=True, timeout=50)
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self.client.delete({'uri': '/rest/uri'})
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_allocate_called_once(self, mock_update):
        self.client.allocate(self.resource_info.copy(), self.example_uri)
        mock_update.assert_called_once_with(self.resource_info.copy(), self.example_uri + "/allocator", timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_collect_called_once(self, update):
        self.client.collect(self.resource_info.copy(), self.example_uri)
        update.assert_called_once_with(self.resource_info.copy(), self.example_uri + "/collector", timeout=-1)
