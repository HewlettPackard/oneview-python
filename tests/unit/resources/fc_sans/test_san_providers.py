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
from hpeOneView.resources.fc_sans.san_providers import SanProviders
from hpeOneView.resources.resource import Resource, ResourceHelper

TIMEOUT = -1


class SanProvidersTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._san_provider = SanProviders(self.connection)
        self.uri = "/rest/fc-sans/providers/1234-5678"
        self._san_provider.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_device_manager_under_a_provider(self, mock_create):
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
        uri_or_id = '/rest/fc-sans/providers/534-345-345-55'
        rest_uri = "/rest/fc-sans/providers/534-345-345-55/device-managers"

        self._san_provider.add(resource=resource, provider_uri_or_id=uri_or_id, timeout=TIMEOUT)
        mock_create.assert_called_once_with(data=resource, uri=rest_uri, timeout=TIMEOUT)

    @mock.patch.object(Resource, 'get_by_field')
    def test_get_provider_uri(self, mock_get_by_field):
        provider_name = "Brocade Network Advisor"

        self._san_provider.get_provider_uri(provider_name)
        mock_get_by_field.assert_called_once_with('displayName', provider_name)

    @mock.patch.object(Resource, 'get_by_field')
    def test_get_provider_uri_with_empty_provider(self, mock_get_by_field):
        provider_name = "Brocade Network Advisor"
        mock_get_by_field.return_value = None

        result = self._san_provider.get_provider_uri(provider_name)
        self.assertFalse(result)
        mock_get_by_field.assert_called_once_with('displayName', provider_name)

    @mock.patch.object(Resource, 'get_by_field')
    def test_get_default_connection_info(self, mock_get_by_field):
        provider_name = "Brocade Network Advisor"
        self._san_provider.get_default_connection_info(provider_name)
        mock_get_by_field.assert_called_once_with('displayName', provider_name)

    @mock.patch.object(Resource, 'get_by_field')
    def test_get_default_connection_info_with_empty_provider(self, mock_get_by_field):
        provider_name = "Brocade Network Advisor"
        mock_get_by_field.return_value = None
        provider = self._san_provider.get_default_connection_info(provider_name)
        self.assertFalse(provider)
        mock_get_by_field.assert_called_once_with('displayName', provider_name)
