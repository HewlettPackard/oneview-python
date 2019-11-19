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
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.resource import ResourceClient


class InterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnects = Interconnects(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_statistics(self, mock_get):
        self._interconnects.get_statistics('3518be0e-17c1-4189-8f81-83f3724f6155')

        uri = '/rest/interconnects/3518be0e-17c1-4189-8f81-83f3724f6155/statistics'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_statistics_with_port_name(self, mock_get):
        self._interconnects.get_statistics('3518be0e-17c1-4189-8f81-83f3724f6155', 'd1')

        uri = '/rest/interconnects/3518be0e-17c1-4189-8f81-83f3724f6155/statistics/d1'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_interconnect_name_servers(self, mock_get):
        uri = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/nameServers'
        interconnect_id = '5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'

        self._interconnects.get_name_servers(interconnect_id)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_statistics_with_port_name_and_subport(self, mock_get):
        self._interconnects.get_subport_statistics('3518be0e-17c1-4189-8f81-83f3724f6155', 'd1', 1)

        uri = '/rest/interconnects/3518be0e-17c1-4189-8f81-83f3724f6155/statistics/d1/subport/1'

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_interconnect(self, mock_get):
        interconnect_id = '5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'

        self._interconnects.get(interconnect_id)
        mock_get.assert_called_once_with(interconnect_id)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_interconnect_by_key(self, mock_get_by):
        field = 'name'
        value = 'fakeName'

        self._interconnects.get_by(field, value)
        mock_get_by.assert_called_once_with(field, value)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_interconnect_by_name(self, mock_get_by_name):
        name = 'fakeName'

        self._interconnects.get_by_name(name)
        mock_get_by_name.assert_called_once_with(name)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnects.get_all(2, 5, filter, sort)
        mock_get_all.assert_called_once_with(2, 5, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_interconnect_should_return_the_task(self, mock_patch):
        interconnect_id = '5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'
        operation = 'replace'
        path = '/powerState'
        value = 'On'
        timeout = 10

        self._interconnects.patch(interconnect_id, operation, path, value, timeout)
        mock_patch.assert_called_once_with(interconnect_id, operation, path, value, timeout)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_interconnect_port(self, mock_update):
        interconnect_id = '5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/ports'
        information = {
            "type": "port",
            "bayNumber": 1,
        }
        self._interconnects.update_port(information, interconnect_id)
        mock_update.assert_called_once_with(information, url, -1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_reset_port_protection(self, mock_update):
        interconnect_id = '5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/resetportprotection'
        self._interconnects.reset_port_protection(interconnect_id)
        mock_update.assert_called_once_with(url, -1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_ports(self, mock_update):
        interconnect_id = '5v8f3ec0-52t4-475a-84g4-c4iod72d2c20'
        url = '/rest/interconnects/5v8f3ec0-52t4-475a-84g4-c4iod72d2c20/update-ports'

        port1 = {
            "type": "port2",
            "portName": "d1",
            "enabled": False,
            "portId": "0f6f4937-6801-4494-a528-5dc01368c043:d1"
        }
        port2 = {
            "portName": "d2",
            "enabled": False,
            "portId": "0f6f4937-6801-4494-a528-5dc01368c043:d2"
        }
        ports = [port1, port2]

        clone = port2.copy()
        clone["type"] = "port"
        expected_ports = [port1, clone]

        self._interconnects.update_ports(ports, interconnect_id)
        mock_update.assert_called_once_with(expected_ports, url, -1)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_ports_called_once(self, mock_get_all):
        interconnect_id = "123456"
        uri = '/rest/interconnects/123456/ports'

        self._interconnects.get_ports(interconnect_id, 2, 5)

        mock_get_all.assert_called_once_with(2, 5, uri=uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_ports_called_once_with_defaults(self, mock_get_all):
        interconnect_id = "123456"
        uri = '/rest/interconnects/123456/ports'

        self._interconnects.get_ports(interconnect_id)

        mock_get_all.assert_called_once_with(0, -1, uri=uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_ports_should_return_the_ports(self, mock_get):
        interconnect_id = "123456"
        port_id = "88888"

        ports = [{"mock": "value"}, {"mock": "value2"}]
        mock_get.return_value = ports

        result = self._interconnects.get_port(interconnect_id, port_id)

        self.assertEqual(result, ports)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_port_called_once(self, mock_get):
        interconnect_id = "123456"
        port_id = "88888"
        uri = '/rest/interconnects/123456/ports/88888'

        self._interconnects.get_port(interconnect_id, port_id)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_port_should_return_the_port(self, mock_get):
        interconnect_id = "123456"
        port_id = "88888"

        mock_get.return_value = {"mock": "value"}

        result = self._interconnects.get_port(interconnect_id, port_id)

        self.assertEqual(result, {"mock": "value"})

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body):
        uri_interconnect = '/rest/interconnects/0123456789test'
        uri_rest_call = '/rest/interconnects/0123456789test/configuration'

        self._interconnects.update_configuration(uri_interconnect)

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_pluggable_module_information(self, mock_get):
        self._interconnects.get_pluggable_module_information('0123456789test')

        uri = '/rest/interconnects/0123456789test/pluggableModuleInformation'

        mock_get.assert_called_once_with(uri)
