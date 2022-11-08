# -*- coding: utf-8 -*-
###
# (C) Copyright [2022] Hewlett Packard Enterprise Development LP
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
from hpeOneView.resources.fc_sans.san_managers import SanManagers
from hpeOneView.resources.resource import ResourceHelper

TIMEOUT = -1


class SanManagersTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._san_manager = SanManagers(self.connection)
        self.uri = "/rest/fc-sans/device-managers/1234-5678"
        self._san_manager.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'
        query = 'query'

        self._san_manager.get_all(start=2, count=500, filter=query_filter, query=query, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=query_filter, query=query, sort=sort)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_a_registered_device_manager(self, mock_update):
        uri_rest_call = self.uri
        info = {
            'refreshState': "RefreshPending"
        }

        self._san_manager.update(resource=info, uri=uri_rest_call)

        mock_update.assert_called_once_with(resource=info, uri=uri_rest_call)        

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._san_manager.remove(force=False)

        mock_delete.assert_called_once_with(self.uri, force=False,
                                            custom_headers={'If-Match': '*'}, timeout=TIMEOUT)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_san_manager(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "172.18.15.1", "uri": "/rest/fc-sans/device-managers/1"},
            {"name": "172.18.15.2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        san_manager = self._san_manager.get_by_name("172.18.15.2")

        self.assertEqual(san_manager.data,
                         {"name": "172.18.15.2", "uri": "/rest/fc-sans/device-managers/2"})

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_provider_display_name_san_manager(self, mock_get_all):
        mock_get_all.return_value = [
            {"providerDisplayName": "Brocade Network Advisor 1", "uri": "/rest/fc-sans/device-managers/1"},
            {"providerDisplayName": "Brocade Network Advisor 2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        san_manager = self._san_manager.get_by_provider_display_name("Brocade Network Advisor 1")

        self.assertEqual(san_manager.data,
                         {"providerDisplayName": "Brocade Network Advisor 1", "uri": "/rest/fc-sans/device-managers/1"})

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_provider_display_name_should_return_null_when_not_found(self, mock_get_all):
        existent_san_managers = [
            {"providerDisplayName": "Brocade Network Advisor 1", "uri": "/rest/fc-sans/device-managers/1"},
            {"providerDisplayName": "Brocade Network Advisor 2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        mock_get_all.return_value = existent_san_managers
        san_manager = self._san_manager.get_by_provider_display_name("Brocade Network Advisor 3")

        self.assertIsNone(san_manager)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_should_return_null_when_not_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "172.18.15.1", "uri": "/rest/fc-sans/device-managers/1"},
            {"name": "172.18.15.2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        san_manager = self._san_manager.get_by_name("172.18.15.3")

        self.assertIsNone(san_manager)








