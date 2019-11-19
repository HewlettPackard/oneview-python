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
import mock

from hpOneView.connection import connection
from hpOneView.resources.servers.server_hardware_types import ServerHardwareTypes
from hpOneView.resources.resource import Resource, ResourceHelper
import unittest


class ServerHardwareTypesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._server_hardware_types = ServerHardwareTypes(self.connection)
        self.uri = "/rest/server-hardware-types/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        self._server_hardware_types.data = {'uri': self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._server_hardware_types.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_conce(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._server_hardware_types.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_defaults(self, update):
        server_hardware_type = {
            "name": "New Server Type Name",
            "description": "New Description"
        }
        self._server_hardware_types.update(server_hardware_type)
        update.assert_called_once_with(
            server_hardware_type, force=False, timeout=-1,
            uri=self.uri)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, update):
        server_hardware_type = {
            "name": "New Server Type Name",
            "description": "New Description"
        }
        self._server_hardware_types.update(server_hardware_type, timeout=70)
        update.assert_called_once_with(
            server_hardware_type, force=False, timeout=70,
            uri=self.uri)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._server_hardware_types.delete(force=True, timeout=50)

        mock_delete.assert_called_once_with(self.uri, force=True, timeout=50, custom_headers=None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self._server_hardware_types.delete()

        mock_delete.assert_called_once_with(self.uri, force=False, timeout=-1, custom_headers=None)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._server_hardware_types.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")
