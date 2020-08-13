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

from hpeOneView.connection import connection
from hpeOneView.resources.networking.interconnects import Interconnects
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class InterconnectsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnects = Interconnects(self.connection)
        self._interconnects.data = {'uri': '/rest/interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'}

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_statistics(self, mock_get):
        self._interconnects.get_statistics()
        uri = '{}/statistics'.format(self._interconnects.data["uri"])

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_statistics_with_port_name(self, mock_get):
        self._interconnects.get_statistics('d1')
        uri = '{}/statistics/d1'.format(self._interconnects.data["uri"])

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_interconnect_name_servers(self, mock_get):
        uri = '{}/nameServers'.format(self._interconnects.data["uri"])
        self._interconnects.get_name_servers()

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_statistics_with_port_name_and_subport(self, mock_get):
        self._interconnects.get_subport_statistics('d1', 1)
        uri = '{}/statistics/d1/subport/1'.format(self._interconnects.data["uri"])

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by')
    def test_get_interconnect_by_key(self, mock_get_by):
        field = 'name'
        value = 'fakeName'

        self._interconnects.get_by(field, value)
        mock_get_by.assert_called_once_with(field, value)

    @mock.patch.object(Resource, 'get_by_name')
    def test_get_interconnect_by_name(self, mock_get_by_name):
        name = 'fakeName'

        self._interconnects.get_by_name(name)
        mock_get_by_name.assert_called_once_with(name)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnects.get_all(2, 5, filter, sort)
        mock_get_all.assert_called_once_with(count=5, filter='name=TestName', sort='name:ascending', start=2)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_interconnect_should_return_the_task(self, mock_patch):
        operation = 'replace'
        path = '/powerState'
        value = 'On'
        timeout = 10

        self._interconnects.patch(operation, path, value, timeout)
        mock_patch.assert_called_once_with(operation, path, value, timeout)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_interconnect_port(self, mock_update):
        url = '{}/ports'.format(self._interconnects.data["uri"])
        information = {
            "type": "port",
            "bayNumber": 1,
        }
        self._interconnects.update_port(information)
        mock_update.assert_called_once_with(information, url, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update_with_zero_body')
    def test_reset_port_protection(self, mock_update):
        url = '{}/resetportprotection'.format(self._interconnects.data["uri"])
        self._interconnects.reset_port_protection()
        mock_update.assert_called_once_with(url, -1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_ports(self, mock_update):
        url = '{}/update-ports'.format(self._interconnects.data["uri"])

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

        self._interconnects.update_ports(ports)
        mock_update.assert_called_once_with(expected_ports, url, timeout=-1)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_ports_called_once(self, mock_get_all):
        uri = '{}/ports'.format(self._interconnects.data["uri"])
        self._interconnects.get_ports(2, 5)

        mock_get_all.assert_called_once_with(2, 5, uri=uri)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_ports_called_once_with_defaults(self, mock_get_all):
        uri = '{}/ports'.format(self._interconnects.data["uri"])
        self._interconnects.get_ports()

        mock_get_all.assert_called_once_with(0, -1, uri=uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_ports_should_return_the_ports(self, mock_get):
        port_id = "88888"
        ports = [{"mock": "value"}, {"mock": "value2"}]
        mock_get.return_value = ports

        result = self._interconnects.get_port(port_id)

        self.assertEqual(result, ports)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_port_called_once(self, mock_get):
        port_id = "88888"
        uri = '{}/ports/88888'.format(self._interconnects.data["uri"])

        self._interconnects.get_port(port_id)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_port_should_return_the_port(self, mock_get):
        port_id = "88888"
        mock_get.return_value = {"mock": "value"}

        result = self._interconnects.get_port(port_id)

        self.assertEqual(result, {"mock": "value"})

    @mock.patch.object(ResourceHelper, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body):
        uri_rest_call = '{}/configuration'.format(self._interconnects.data["uri"])
        self._interconnects.update_configuration()

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_pluggable_module_information(self, mock_get):
        self._interconnects.get_pluggable_module_information()

        uri = '{}/pluggableModuleInformation'.format(self._interconnects.data["uri"])

        mock_get.assert_called_once_with(uri)
