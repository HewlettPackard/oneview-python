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
from hpOneView.resources.fc_sans.san_managers import SanManagers

TIMEOUT = -1

PROVIDERS = [
    {
        "uri": "/rest/fc-sans/providers/0aa1f4e1-3b5e-4233-af1a-f849dc64da69",
        "name": "Brocade San Plugin",
        "displayName": "Brocade Network Advisor",
        "sanType": "Fabric"
    },
    {
        "uri": "/rest/fc-sans/providers/848c191d-c995-4cd5-a7ba-e627435dd5f2",
        "name": "Cisco San Plugin",
        "displayName": "Cisco",
        "sanType": "Fabric"
    },
    {
        "uri": "/rest/fc-sans/providers/5c5c67f5-0f8f-4c85-a54f-f26b1f1332c7",
        "name": "Direct Attach SAN Plugin",
        "displayName": "HPE",
        "sanType": "Fabric"
    }
]


class SanManagersTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host, 800)
        self._resource = SanManagers(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, query=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, query=query_filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"

        self._resource.get(id)
        mock_get.assert_called_once_with(id_or_uri=id)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_withId(self, mock_create):
        resource = {
            "connectionInfo": [
                {
                    "name": "Host",
                    "value": "brocade-device-manager.domain.com"
                },
                {
                    "name": "Port",
                    "value": 5989
                },
                {
                    "name": "Username",
                    "value": "Administrator"
                },
                {
                    "name": "Password",
                    "value": "password"
                },
                {
                    "name": "UseSsl",
                    "value": True
                }
            ]
        }

        provider_id = "534-345-345-55"
        rest_uri = "/rest/fc-sans/providers/534-345-345-55/device-managers"

        self._resource.add(resource, provider_uri_or_id=provider_id, timeout=TIMEOUT)
        mock_create.assert_called_once_with(resource=resource, uri=rest_uri, timeout=TIMEOUT)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_withUri(self, mock_create):
        resource = {
            "connectionInfo": [
                {
                    "name": "Host",
                    "value": "brocade-device-manager.domain.com"
                },
                {
                    "name": "Port",
                    "value": 5989
                },
                {
                    "name": "Username",
                    "value": "Administrator"
                },
                {
                    "name": "Password",
                    "value": "password"
                },
                {
                    "name": "UseSsl",
                    "value": True
                }
            ]
        }

        provider_uri = "/rest/fc-sans/providers/534-345-345-55"
        rest_uri = "/rest/fc-sans/providers/534-345-345-55/device-managers"

        self._resource.add(resource, provider_uri_or_id=provider_uri, timeout=TIMEOUT)
        mock_create.assert_called_once_with(resource=resource, uri=rest_uri, timeout=TIMEOUT)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_default_connection_info(self, mock_get_by_name):
        provider_name = "Brocade Network Advisor"
        self._resource.get_default_connection_info(provider_name)
        mock_get_by_name.assert_called_once_with(provider_name)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_default_connection_info_with_empty_provider(self, mock_get_by_name):
        provider_name = "Brocade Network Advisor"
        mock_get_by_name.return_value = None
        provider = self._resource.get_default_connection_info(provider_name)
        self.assertFalse(provider)
        mock_get_by_name.assert_called_once_with(provider_name)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_provider_uri(self, mock_get_all):
        provider_name = "Brocade Network Advisor"
        mock_get_all.return_value = PROVIDERS

        result = self._resource.get_provider_uri(provider_name)
        self.assertEqual(result, PROVIDERS[0]['uri'])

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_provider_uri_should_return_none_when_not_found(self, mock_get_all):
        provider_name = "Brocade Network Advisor"
        mock_get_all.return_value = []

        result = self._resource.get_provider_uri(provider_name)
        self.assertEqual(result, None)

    @mock.patch.object(ResourceClient, 'update')
    def test_update(self, mock_update):
        uri = "/rest/fc-sans/device-managers/4ff2327f-7638-4b66-ad9d-283d4940a4ae"
        manager = dict(name="Device Manager Test", description="Direct Attach SAN Manager")

        self._resource.update(resource=manager, id_or_uri=uri)
        mock_update.assert_called_once_with(resource=manager, uri=uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._resource.remove(id, timeout=-1)

        mock_delete.assert_called_once_with(id, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_san_manager_when_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "172.18.15.1", "uri": "/rest/fc-sans/device-managers/1"},
            {"name": "172.18.15.2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        san_manager = self._resource.get_by_name("172.18.15.2")
        expected_result = {"name": "172.18.15.2", "uri": "/rest/fc-sans/device-managers/2"}

        self.assertEqual(san_manager, expected_result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_null_when_not_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "172.18.15.1", "uri": "/rest/fc-sans/device-managers/1"},
            {"name": "172.18.15.2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        san_manager = self._resource.get_by_name("172.18.15.3")

        self.assertIsNone(san_manager)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_provider_display_name_should_return_san_manager_when_found(self, mock_get_all):
        existent_san_managers = [
            {"providerDisplayName": "Brocade Network Advisor 1", "uri": "/rest/fc-sans/device-managers/1"},
            {"providerDisplayName": "Brocade Network Advisor 2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        mock_get_all.return_value = existent_san_managers
        san_manager = self._resource.get_by_provider_display_name("Brocade Network Advisor 2")

        self.assertEqual(san_manager, existent_san_managers[1])

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_provider_display_name_should_return_null_when_not_found(self, mock_get_all):
        existent_san_managers = [
            {"providerDisplayName": "Brocade Network Advisor 1", "uri": "/rest/fc-sans/device-managers/1"},
            {"providerDisplayName": "Brocade Network Advisor 2", "uri": "/rest/fc-sans/device-managers/2"}
        ]
        mock_get_all.return_value = existent_san_managers
        san_manager = self._resource.get_by_provider_display_name("Brocade Network Advisor 3")

        self.assertIsNone(san_manager)
