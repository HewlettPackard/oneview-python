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
from hpeOneView.resources.networking.network_sets import NetworkSets
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class NetworkSetsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._network_sets = NetworkSets(self.connection)
        self._network_sets.data = {'uri': '/rest/network-sets/ad28cf21-8b15-4f92-bdcf-51cb2042db32'}

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._network_sets.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter, sort)

    @mock.patch.object(ResourceHelper, 'create')
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
        mock_create.assert_called_once_with(resource_rest_call, 10, -1, None, False)

    @mock.patch.object(ResourceHelper, 'do_put')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_should_use_given_values(self, mock_get, mock_put):
        resource = {
            'name': 'OneViewSDK Test Network Set',
            'type': 'network-set',
            'connectionTemplateUri': None
        }
        resource_updated = resource.copy()
        resource_updated['uri'] = self._network_sets.data["uri"]
        mock_put.return_value = resource_updated
        mock_get.return_value = resource

        self._network_sets.update(resource, 20)
        mock_put.assert_called_once_with(self._network_sets.data['uri'],
                                         resource_updated, 20, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._network_sets.delete(force=False)
        mock_delete.assert_called_once_with(self._network_sets.data["uri"],
                                            custom_headers=None,
                                            force=False, timeout=-1)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._network_sets.get_by('name', 'OneViewSDK Test Network Set')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK Test Network Set')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_without_ethernet_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._network_sets.get_all_without_ethernet(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_without_ethernet_called_once(self, mock_get):
        uri = "{}/withoutEthernet".format(self._network_sets.data['uri'])
        self._network_sets.get_without_ethernet()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._network_sets.patch('replace', '/scopeUris', ['/rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('replace', '/scopeUris',
                                           ['/rest/fake/scope123'], 1)
