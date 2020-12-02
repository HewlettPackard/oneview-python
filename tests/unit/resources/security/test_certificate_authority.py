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
from hpeOneView.resources.security.certificate_authority import CertificateAuthority
from hpeOneView.resources.resource import Resource


class CertificateAuthorityTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._certificates = CertificateAuthority(self.connection)
        self.uri = '/rest/certificates/ca'

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            certificateDetails=["test1", "test2"],
        )

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._certificates.create(resource)
        mock_create.assert_called_once_with(resource_rest_call, uri=self.uri, timeout=-1)

    @mock.patch.object(Resource, 'create')
    def test_create_called_with_parent_task(self, mock_create):
        resource = dict(
            certificateDetails=["test1", "test2"],
        )

        uri = "{}?parentTask={}".format(self.uri, 'parent1')
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._certificates.create(resource, 'parent1')
        mock_create.assert_called_once_with(resource_rest_call, uri=uri, timeout=-1)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_with_filter(self, mock_get_all):
        self._certificates.get_all(filter='name=TestName', cert_details=False)
        mock_get_all.assert_called_once_with(custom_headers={'If-Req-CertDetails': False}, filter='name=TestName')

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        self._certificates.get_all()
        mock_get_all.assert_called_once_with(custom_headers={'If-Req-CertDetails': True}, filter='')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_aliasname_called_once(self, mock_get):
        self._certificates.get_by_aliasname('test1')
        mock_get.assert_called_once_with('/rest/certificates/ca/test1')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_crl_called_once(self, mock_get):
        self._certificates.get_crl()
        mock_get.assert_called_once_with('/rest/certificates/ca/crl')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_crl_by_aliasname_called_once(self, mock_get):
        self._certificates.get_crl_by_aliasname('test1')
        mock_get.assert_called_once_with('/rest/certificates/ca/test1/crl')

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._certificates.delete("default")
        mock_delete.assert_called_once_with("default")
