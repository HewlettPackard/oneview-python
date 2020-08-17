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
from hpOneView.resources.security.certificate_authority import CertificateAuthority
from hpOneView.resources.resource import ResourceClient


class CertificateAuthorityTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._certificates = CertificateAuthority(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._certificates.get()
        mock_get.assert_called_once_with('/rest/certificates/ca')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_crl_called_once(self, mock_get):
        self._certificates.get_crl()
        mock_get.assert_called_once_with('/rest/certificates/ca/crl')

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._certificates.delete("default")
        mock_delete.assert_called_once_with("/rest/certificates/ca/default", timeout=-1)
