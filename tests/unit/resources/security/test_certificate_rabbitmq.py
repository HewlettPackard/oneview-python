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

from hpeOneView.connection import connection
from hpeOneView.resources.resource import ResourceClient
from hpeOneView.resources.security.certificate_rabbitmq import CertificateRabbitMQ


class CertificateRabbitMQTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._certificate_rabbitmq = CertificateRabbitMQ(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_generate_called_once_with_defaults(self, mock_create):
        information = {
            "commonName": "default",
            "type": "RabbitMqClientCertV2"
        }
        self._certificate_rabbitmq.generate(information)
        mock_create.assert_called_once_with(information, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_alias_name_called_once(self, mock_get):
        alias_name = 'default'
        self._certificate_rabbitmq.get(alias_name)
        mock_get.assert_called_once_with(alias_name)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_key_pair_called_once(self, mock_get):
        alias_name = 'default'
        self._certificate_rabbitmq.get_key_pair(alias_name)
        uri = "/rest/certificates/client/rabbitmq/keypair/" + alias_name
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_keys_called_once(self, mock_get):
        alias_name = 'default'
        key_format = 'Base64'
        self._certificate_rabbitmq.get_keys(alias_name, key_format)
        uri = "/rest/certificates/client/rabbitmq/keys/" + alias_name + "?format=" + key_format
        mock_get.assert_called_once_with(uri)
