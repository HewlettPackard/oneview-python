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
from hpOneView.resources.networking.switches import Switches
from hpOneView.resources.resource import ResourceClient


class SwitchesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._switches = Switches(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_statistics_called_once(self, mock_get):
        self._switches.get_statistics('3518be0e-17c1-4189-8f81-83f3724f6155')
        uri = '/rest/switches/3518be0e-17c1-4189-8f81-83f3724f6155/statistics'
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_statistics_with_portName(self, mock_get):
        self._switches.get_statistics(
            '3518be0e-17c1-4189-8f81-83f3724f6155', 'X1')
        uri = '/rest/switches/3518be0e-17c1-4189-8f81-83f3724f6155/statistics/X1'
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        switch_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._switches.get(switch_id)
        mock_get.assert_called_once_with(switch_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        switch_uri = "/rest/switches/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._switches.get(switch_uri)
        mock_get.assert_called_once_with(switch_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self._switches.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_defaults(self, mock_get_all):
        self._switches.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_environmental_configuration_called_once_when_id_provided(self, mock_get):
        switches_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        switches_environmental_config_uri = \
            "/rest/switches/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/environmentalConfiguration"
        self._switches.get_environmental_configuration(switches_id)
        mock_get.assert_called_once_with(switches_environmental_config_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_environmental_configuration_called_once_when_uri_provided(self, mock_get):
        switches_uri = "/rest/switches/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        switches_environmental_config_uri = \
            "/rest/switches/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/environmentalConfiguration"
        self._switches.get_environmental_configuration(switches_uri)
        mock_get.assert_called_once_with(switches_environmental_config_uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._switches.delete(id, force=True, timeout=50)
        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._switches.delete(id)
        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._switches.get_by("name", "test name")
        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'update')
    def test_update_ports_called_once(self, mock_update):
        switch_uri = '/rest/switches/f0a0a113-ec97-41b4-83ce-d7c92b900e7c'
        resource = [{"enabled": False}]

        self._switches.update_ports(resource, switch_uri)

        expected_uri = switch_uri + "/update-ports"
        expected_resource = [{"enabled": False, 'type': 'port'}]
        mock_update.assert_called_once_with(uri=expected_uri, resource=expected_resource)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._switches.patch('rest/fake/switches/123', 'replace',
                             '/scopeUris', ['rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('rest/fake/switches/123', 'replace',
                                           '/scopeUris', ['rest/fake/scope123'], timeout=1)
