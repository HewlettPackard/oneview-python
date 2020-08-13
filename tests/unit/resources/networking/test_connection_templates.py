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
from hpeOneView.resources.networking.connection_templates import ConnectionTemplates
from hpeOneView.resources.resource import Resource, ResourceHelper


class ConnectionTemplatesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._connection_templates = ConnectionTemplates(self.connection)

    @mock.patch.object(ResourceHelper, 'do_requests_to_getall')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._connection_templates.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with('/rest/connection-templates?start=2&count=500&filter=name%3DTestName&sort=name%3Aascending', 500)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._connection_templates.get_by(
            'name', 'name1128673347-1465916352647')

        mock_get_by.assert_called_once_with(
            'name', 'name1128673347-1465916352647')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_default_called_once(self, mock_do_get):
        self._connection_templates.get_default()
        uri = '/rest/connection-templates/defaultConnectionTemplate'

        mock_do_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'update')
    def test_update_called_once(self, mock_update):
        con_template = {
            "type": "connection-templates",
            "bandwidth": {
                "maximumBandwidth": 10000,
                "typicalBandwidth": 2000
            },
            "name": "CT-23"
        }
        self._connection_templates.update(con_template, 70)
        mock_update.assert_called_once_with(con_template, 70)
