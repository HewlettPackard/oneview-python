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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.settings.licenses import Licenses


class LicensesTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        oneview_connection = connection(self.DEFAULT_HOST)
        self.resource = Licenses(oneview_connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        data = {
            'key': 'ASD8 JKL7 UYT9',
            'type': 'LicenseListV500'
        }
        self.resource.create(data)
        mock_create.assert_called_once_with(data, timeout=-1, default_values=self.resource.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = '54'
        self.resource.delete(id)
        mock_delete.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get_by_id):
        id = '/rest/licenses/54'
        self.resource.get_by_id(id)
        mock_get_by_id.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self.resource.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)
