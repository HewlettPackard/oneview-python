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
from hpOneView.resources.networking.network_sets import NetworkSets
from hpOneView.resources.resource import ResourceClient


class NetworkSetsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._network_sets = NetworkSets(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._network_sets.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test Network Set',
            'type': 'network-sets',
            'connectionTemplateUri': None,
            'nativeNetworkUri': None
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._network_sets.create(resource, 10)
        mock_create.assert_called_once_with(resource_rest_call, timeout=10,
                                            default_values=self._network_sets.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test Network Set',
            'type': 'network-set',
            'uri': 'a_uri',
            'connectionTemplateUri': None
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._network_sets.update(resource, 20)
        mock_update.assert_called_once_with(resource_rest_call, timeout=20,
                                            default_values=self._network_sets.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._network_sets.delete(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._network_sets.get_by('name', 'OneViewSDK Test Network Set')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK Test Network Set')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._network_sets.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/network-sets/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._network_sets.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_without_ethernet_called_once(self, mock_get):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri = '/rest/network-sets/ad28cf21-8b15-4f92-bdcf-51cb2042db32/withoutEthernet'
        self._network_sets.get_without_ethernet(id)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_without_ethernet_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._network_sets.get_all_without_ethernet(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._network_sets.patch('/rest/fake/ns123', 'replace', '/scopeUris', ['/rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('/rest/fake/ns123', 'replace', '/scopeUris',
                                           ['/rest/fake/scope123'], timeout=1)
