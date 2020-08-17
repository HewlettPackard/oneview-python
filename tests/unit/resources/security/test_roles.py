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

from unittest import TestCase
from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.security.roles import Roles


class RolesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = Roles(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with(count=500, filter='name=TestName', sort='name:ascending', start=2)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._client.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter=u'', sort=u'', start=0)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id = "Infrastructure administrator"
        self._client.get(id)
        mock_get.assert_called_once_with('Infrastructure%20administrator')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        uri = "/rest/roles/Infrastructure administrator"
        self._client.get(uri)
        mock_get.assert_called_once_with('/rest/roles/Infrastructure%20administrator')
