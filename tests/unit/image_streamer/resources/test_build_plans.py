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
from hpeOneView.image_streamer.resources.build_plans import BuildPlans
from hpeOneView.resources.resource import ResourceClient


class BuildPlansTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = BuildPlans(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'Build Plan Name')

        mock_get_by.assert_called_once_with(
            'name', 'Build Plan Name')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/build-plans/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once_with_default_type(self, mock_create):
        information = {
            "name": "OS Build Plan Name",
        }
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(information, timeout=-1, default_values=self._client.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once_with_provided_type(self, mock_create):
        information = {
            "name": "OS Build Plan Name",
        }
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(information, timeout=-1, default_values=self._client.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        information = {
            "type": "OeBuildPlan",
            "name": "OS Build Plan Name",
            "description": "Description of the build plan",
        }
        expected_data = information.copy()
        mock_update.return_value = {}

        self._client.update(information)
        mock_update.assert_called_once_with(expected_data, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=True)

        mock_delete.assert_called_once_with(id, force=True, timeout=-1)
