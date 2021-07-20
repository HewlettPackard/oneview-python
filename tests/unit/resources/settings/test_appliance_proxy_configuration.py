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
from hpeOneView.resources.settings.appliance_proxy_configuration import ApplianceProxyConfiguration
from hpeOneView.resources.resource import Resource


class ApplianceProxyConfigurationTest(unittest.TestCase):
    resource_info = {"server": "1.1.1.1",
                     "port": 443,
                     "username": "aaaa",
                     "password": "test",
                     "communicationProtocol": "HTTP"}
    uri = '/rest/appliance/proxy-config'

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._proxy = ApplianceProxyConfiguration(self.connection)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_proxy_config_called_once(self, mock_get):
        self._proxy.get_by_uri(self.uri)
        mock_get.assert_called_once_with(self.uri)

    @mock.patch.object(Resource, 'get_all')
    def test_get_by_proxy_called_once(self, mock_get_all):
        self._proxy.get_by_proxy('1.1.1.1')
        mock_get_all.assert_called_once_with('server', '1.1.1.1')

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        self._proxy.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._proxy.delete()
        mock_delete.assert_called_once_with()
