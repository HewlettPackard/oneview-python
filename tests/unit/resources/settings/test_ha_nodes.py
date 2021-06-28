# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
from hpeOneView.resources.settings.ha_nodes import HANodes
from hpeOneView.resources.resource import Resource, ResourcePatchMixin, ResourceHelper


class HANodesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self.uri = "/rest/appliance/ha-nodes"
        self._ha_nodes = HANodes(self.connection)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_ha_nodes_called_once(self, mock_get):
        self._ha_nodes.get_by_uri()
        mock_get.assert_called_once_with('/rest/appliance/ha-nodes')

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._ha_nodes.get_all()
        mock_get_all.assert_called_once_with()

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_default(self, mock_update, mock_ensure_client):
        resource = {
            "name": "enc101 appliance bay 1",
            "oldUri": "/rest/appliance/ha-nodes/1",
            "role": "Standby"
        }
        self._ha_nodes.update(resource)
        mock_update.assert_called_once_with(resource, self.uri, False, -1, None)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_called_once(self, mock_patch):
        uri = '/rest/appliance/ha-nodes/1'

        resource = {
            "operation": "replace", "path": "/role", "value": "Standby"
        }
        self._ha_nodes.patch("replace", "/role", "Standby")
        mock_patch.assert_called_once_with(
            self.uri, body=[resource], custom_headers=None, timeout=-1)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch(self, mock_pacth):
        self._resource.patch("replace", "/templateCompliance", "Compliant")
        mock_pacth.assert_called_once_with(self.uri, body=[{'path': '/templateCompliance',
                                                            'op': 'replace',
                                                            'value': 'Compliant'}],
                                           custom_headers=None, timeout=-1)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._ha_nodes.delete()
        mock_delete.assert_called_once_with()