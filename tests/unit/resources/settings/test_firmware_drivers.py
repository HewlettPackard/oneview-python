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

from hpeOneView.connection import connection
from hpeOneView.resources.resource import Resource, ResourceSchemaMixin
from hpeOneView.resources.settings.firmware_drivers import FirmwareDrivers


class FirmwareDriversTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._firmware_drivers = FirmwareDrivers(self.connection)
        self.uri = "/rest/firmware-drivers"
        self._firmware_drivers.data = {"uri": self.uri}

    @mock.patch.object(Resource, 'get_all')
    def test_get_all(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._firmware_drivers.get_all(2, 500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._firmware_drivers.get_all()
        mock_get_all.assert_called_once_with()

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri):
        uri = "/rest/firmware-drivers/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._firmware_drivers.get_by_uri(uri)
        mock_get_by_uri.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        drivers = [{'name': 'name1', 'type': 'SPP'}, {'name': 'name2', 'type': 'HotFix'}]
        mock_get_by.return_value = drivers
        result = self._firmware_drivers.get_by("type", 'SPP')
        mock_get_by.assert_called_once_with("type", 'SPP')
        self.assertEqual(result, drivers)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_name_called_once(self, mock_get_by_name):
        drivers = [{'name': 'name1', 'type': 'SPP'}, {'name': 'name2', 'type': 'HotFix'}]
        mock_get_by_name.return_value = drivers
        result = self._firmware_drivers.get_by_name("name1")
        mock_get_by_name.assert_called_once_with("name", "name1")
        self.assertEqual(result.data['type'], 'SPP')

    @mock.patch.object(ResourceSchemaMixin, 'get_schema')
    def test_get_schema(self, mock_get_schema):
        self._firmware_drivers.get_schema()
        mock_get_schema.assert_called_once()

    @mock.patch.object(Resource, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        resource = dict(
            customBaselineName="FirmwareDriver1_Example",
        )

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._firmware_drivers.create(resource)
        mock_create.assert_called_once_with(resource_rest_call)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        self._firmware_drivers.delete(force=True)
        mock_delete.assert_called_once_with(force=True)
