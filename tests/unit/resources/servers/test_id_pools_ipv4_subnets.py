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
import unittest
from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.servers.id_pools_ipv4_subnets import IdPoolsIpv4Subnets


class TestIdPoolsIpv4Subnets(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.client = IdPoolsIpv4Subnets(self.connection)
        self.example_uri = "/rest/id-pools/ipv4/subnets/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        self.client.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id_pools_subnet_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get(id_pools_subnet_id)
        mock_get.assert_called_once_with(id_pools_subnet_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        self.client.get(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_enable_called_once(self, update):
        self.client.update(self.resource_info.copy())
        update.assert_called_once_with(self.resource_info.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get):
        self.client.get_all(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.client.delete({'uri': '/rest/uri'}, force=True, timeout=50)
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self.client.delete({'uri': '/rest/uri'})
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=False, timeout=-1)
