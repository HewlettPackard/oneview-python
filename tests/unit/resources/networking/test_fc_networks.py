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
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.resource import Resource, ResourcePatchMixin


class FcNetworksTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fc_networks = FcNetworks(self.connection)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fc_networks.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter, sort)

    @mock.patch.object(Resource, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': True,
            'type': 'fc-networkV2',
            'linkStabilityTime': 20,
            'fabricType': None,
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._fc_networks.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, 30)

    @mock.patch.object(Resource, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 20,
            'fabricType': None,
            'uri': 'a_uri',
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._fc_networks.update(resource, 60)
        mock_update.assert_called_once_with(resource_rest_call, 60)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._fc_networks.delete(force=False, timeout=-1)
        mock_delete.assert_called_once_with(force=False, timeout=-1)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fc_networks.get_by('name', 'OneViewSDK "Test FC Network')
        mock_get_by.assert_called_once_with('name', 'OneViewSDK "Test FC Network')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/fc-networks/3518be0e-17c1-4189-8f81-83f3724f6155'

        self._fc_networks.get_by_uri(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._fc_networks.patch('/rest/fake/fc123', 'replace', '/scopeUris', ['/rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('/rest/fake/fc123', 'replace', '/scopeUris',
                                           ['/rest/fake/scope123'], 1)
