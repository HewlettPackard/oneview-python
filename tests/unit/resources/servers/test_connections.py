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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.servers.connections import Connections
from hpOneView.resources.resource import ResourceClient


class ConnectionsTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._connections = Connections(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'interconnectUri=xxxx'
        sort = 'name:ascending'
        fields = 'name'
        view = ''

        self._connections.get_all(2, 500, filter, sort, view, fields)

        mock_get_all.assert_called_once_with(
            2, 500, filter=filter, sort=sort, view=view, fields=fields)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_defaults(self, mock_get_all):
        self._connections.get_all()

        mock_get_all.assert_called_once_with(
            0, -1, filter='', sort='', view='', fields='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._connections.get_by('name', 'OneViewSDK-Test-Connection')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK-Test-Connection')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._connections.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/connections/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._connections.get(uri)

        mock_get.assert_called_once_with(uri)
