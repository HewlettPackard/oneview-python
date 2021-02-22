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
import mock
import unittest

from hpeOneView.connection import connection
from hpeOneView.resources.servers.id_pools_ipv4_ranges import IdPoolsIpv4Ranges
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin



class TestIdPoolsIpv4Ranges(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}
    example_uri = "/rest/id-pools/ipv4/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._ipv4_range = IdPoolsIpv4Ranges(self.connection)
        self.uri = self.example_uri
        self._ipv4_range.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        self._ipv4_range.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info, None, -1, None, False)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_id_called_once(self, mock_get):
        id_pools_range_uri = self.example_uri
        self._ipv4_range.get_by_uri(id_pools_range_uri)
        mock_get.assert_called_once_with(id_pools_range_uri)

    @mock.patch.object(Resource, 'update')
    def test_update_called_once(self, mock_update):
        mock_update.return_value = {}
        self._ipv4_range.update(self.resource_info.copy())
        mock_update.assert_called_once_with(self.resource_info.copy())

    @mock.patch.object(ResourceHelper, 'update')
    def test_enable_called_once(self, mock_update):
        mock_update.return_value = {}
        self._ipv4_range.enable(self.resource_info.copy(), self.example_uri, timeout=-1)
        mock_update.assert_called_once_with(self.resource_info.copy(), self.example_uri, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_enable_called_once(self, mock_update):
        payload = {
            "count" :7,
            "idList": [
                "10.1.20.54", 
                "10.1.20.60",
            ]
        }
        mock_update.return_value = {}
        self._ipv4_range.allocator(payload.copy(), self.example_uri)
        allocator_uri  = self.example_uri + "/allocator"
        mock_update.assert_called_once_with(payload.copy(), allocator_uri ,timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_enable_called_once(self, mock_update):
        payload = {
            "idList": [
                "10.1.20.54", 
                "10.1.20.60",
            ]
        }
        mock_update.return_value = {}
        self._ipv4_range.collector(payload.copy(), self.example_uri)
        collector_uri  = self.example_uri + "/collector"
        mock_update.assert_called_once_with(payload.copy(), collector_uri ,timeout=-1)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get):
        self._ipv4_range.get_allocated_fragments(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + "/allocated-fragments?start=0&count=-1")


    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_allocated_fragments_called_once(self, mock_get):
        self._ipv4_range.get_allocated_fragments(self.example_uri, 5, 2)
        mock_get.assert_called_once_with(self.example_uri + "/allocated-fragments?start=2&count=5")

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_free_fragments_called_once_with_defaults(self, mock_get):
        self._ipv4_range.get_free_fragments(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + "/free-fragments?start=0&count=-1")

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_free_fragments_called_once(self, mock_get):
        self._ipv4_range.get_free_fragments(self.example_uri, 5, 3)
        mock_get.assert_called_once_with(self.example_uri + "/free-fragments?start=3&count=5")

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._ipv4_range.delete({'uri': self.example_uri}, force=True, timeout=50)
        mock_delete.assert_called_once_with({'uri': self.example_uri}, force=True, timeout=50)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self._ipv4_range.delete({'uri': self.example_uri}, force=False, timeout=-1)
        mock_delete.assert_called_once_with({'uri': self.example_uri}, force=False, timeout=-1)
