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
from hpOneView.resources.networking.fabrics import Fabrics
from hpOneView.resources.resource import ResourceClient


class FabricsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._fabrics = Fabrics(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._fabrics.get('7a9f7d09-3c24-4efe-928f-50a1af411120')

        mock_get.assert_called_once_with(
            '7a9f7d09-3c24-4efe-928f-50a1af411120')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fabrics.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fabrics.get_by('name', 'DefaultFabric')

        mock_get_by.assert_called_once_with('name', 'DefaultFabric')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_reserved_vlan_range(self, mock_get):
        uri = '/rest/fabrics/123/reserved-vlan-range'
        self._fabrics.get_reserved_vlan_range('123')

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_reserved_vlan_range(self, mock_update):
        uri = '/rest/fabrics/123/reserved-vlan-range'
        data_to_update = {
            "start": 100,
            "length": 100
        }

        self._fabrics.update_reserved_vlan_range('123', data_to_update)

        mock_update.assert_called_once_with(
            resource=data_to_update,
            uri=uri,
            force=False,
            default_values=Fabrics.DEFAULT_VALUES
        )
