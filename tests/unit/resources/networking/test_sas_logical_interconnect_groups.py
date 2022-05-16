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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.networking.sas_logical_interconnect_groups import SasLogicalInterconnectGroups
from hpeOneView.resources.resource import Resource, ResourceHelper


class SasLogicalInterconnectGroupsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._resource = SasLogicalInterconnectGroups(self.connection)
        self.uri = "/rest/sas-logical-interconnect-groups/3518be0e-17c1-4189-8f81-83f3724f6155"
        self._resource.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'TestScope'
        query = 'test'

        self._resource.get_all(2, 500, filter, sort, scope_uris, query=query)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, scope_uris=scope_uris, query=query)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        resource = {'name': 'Test SAS Logical Interconnect Group'}

        self._resource.create(resource, timeout=30)

        mock_create.assert_called_once_with(resource, None, 30, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        resource = {'name': 'Test SAS Logical Interconnect Group'}

        self._resource.update(resource, timeout=60)
        resource["uri"] = self.uri
        mock_update.assert_called_once_with(resource, self.uri, False, 60, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._resource.delete(force=False, timeout=-1)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        self._resource.delete(force=True, timeout=-1)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=True, timeout=-1)
