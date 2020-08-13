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
from hpeOneView.resources.security.certificates_server import CertificatesServer
from hpeOneView.resources.resource import Resource, ResourceHelper
from hpeOneView.exceptions import HPEOneViewException


class CertificatesServerTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._certificate_server = CertificatesServer(self.connection)
        self.uri = "/rest/certificates/servers"
        self._certificate_server.data = {"uri": self.uri}

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            type="CertificateInfoV2",
            certificateDetails=["test1", "test2"],
        )

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._certificate_server.create(resource, timeout=20)
        mock_create.assert_called_once_with(resource_rest_call, uri=self.uri, timeout=20)

    @mock.patch.object(Resource, 'create')
    def test_create_called_once_with_defaults(self, mock_create):
        resource = dict(
            type="CertificateInfoV2",
            certificateDetails=["test1", "test2"],
        )

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._certificate_server.create(resource)
        mock_create.assert_called_once_with(resource_rest_call, uri=self.uri, timeout=-1)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_remote_server_called_once(self, mock_get_remote):
        remote_server = "1.2.3.4"
        uri_rest_call = "/rest/certificates/https/remote/{}".format(remote_server)

        self._certificate_server.get_remote(remote_server)
        mock_get_remote.assert_called_once_with(uri=uri_rest_call)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_aliasName_called_once(self, mock_get_by_aliasname):
        uri_rest_call = "{0}/{1}".format(self.uri, "test1")
        self._certificate_server.get_by_alias_name("test1")
        mock_get_by_aliasname.assert_called_once_with(uri=uri_rest_call)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_aliasName_when_not_found(self, mock_get_by):
        mock_get_by.side_effect = HPEOneViewException("not found")
        self.assertEqual(self._certificate_server.get_by_alias_name("test1"), None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_default(self, mock_update, mock_ensure_client):
        resource = {
            "aliasName": "new certificate",
            "uri": self.uri
        }
        self._certificate_server.update(resource)
        mock_update.assert_called_once_with(resource, self.uri, False, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        resource = {
            "aliasName": "new certificate",
            "uri": self.uri
        }
        self._certificate_server.update(resource, 20)
        mock_update.assert_called_once_with(resource, self.uri, False, 20, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._certificate_server.delete()
        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=False, timeout=-1)
