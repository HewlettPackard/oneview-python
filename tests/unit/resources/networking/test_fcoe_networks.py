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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class FcoeNetworksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fcoe_networks = FcoeNetworks(self.connection)
        self.uri = "/rest/fcoe-networks/3518be0e-17c1-4189-8f81-83f3724f6155"
        self._fcoe_networks.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fcoe_networks.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create(self, mock_create):
        resource = {
            'name': 'OneViewSDK Test FCoE Network',
        }

        mock_create.return_value = {}

        self._fcoe_networks.create(resource)

        mock_create.assert_called_once_with(resource, None, -1, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update(self, mock_update, mock_ensure_client):
        resource = {
            'name': 'vsan1',
            'vlanId': '201',
            'connectionTemplateUri': None,
            'type': 'fcoe-networkV2',
        }
        resource_rest_call = resource.copy()
        resource_rest_call.update(self._fcoe_networks.data)
        mock_update.return_value = {}

        self._fcoe_networks.update(resource, timeout=12)
        mock_update.assert_called_once_with(resource_rest_call, self.uri, False, 12, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._fcoe_networks.delete(force=False, timeout=50)

        mock_delete.assert_called_once_with(self.uri, force=False,
                                            custom_headers=None, timeout=50)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fcoe_networks.get_by('name', 'OneViewSDK Test FCoE Network')

        mock_get_by.assert_called_once_with('name', 'OneViewSDK Test FCoE Network')

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch_request):
        mock_patch_request.return_value = {}

        self._fcoe_networks.patch('replace', '/scopeUris', ['/rest/fake/scope123'], timeout=-1)
        mock_patch_request.assert_called_once_with(self.uri,
                                                   body=[{'path': '/scopeUris',
                                                          'value': ['/rest/fake/scope123'],
                                                          'op': 'replace'}],
                                                   custom_headers=None,
                                                   timeout=-1)

    @mock.patch.object(ResourceHelper, 'create')
    @mock.patch.object(Resource, 'get_all')
    def test_delete_bulk(self, mock_get_all, mock_create):
        resource = {
            "networkUris": [
                "/rest/fcoe-networks/e2f0031b-52bd-4223-9ac1-d91cb519d548",
                "/rest/fcoe-networks/f2f0031b-52bd-4223-9ac1-d91cb519d549",
                "/rest/fcoe-networks/02f0031b-52bd-4223-9ac1-d91cb519d54a"
            ]
        }
        resource_rest_call = resource.copy()

        mock_create.return_value = {}
        mock_get_all.return_value = []

        self._fcoe_networks.delete_bulk(resource, 27)

        mock_create.assert_called_once_with(
            resource_rest_call, uri='/rest/fcoe-networks/bulk-delete', timeout=27)
