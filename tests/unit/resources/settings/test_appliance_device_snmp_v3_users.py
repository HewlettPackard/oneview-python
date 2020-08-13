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
from hpeOneView.resources.settings.appliance_device_snmp_v3_users import ApplianceDeviceSNMPv3Users
from hpeOneView.resources.resource import ResourceClient


class ApplianceDeviceSNMPv3UsersTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._snmp_v3_users = ApplianceDeviceSNMPv3Users(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get):
        self._snmp_v3_users.get_all()
        mock_get.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = {
            'type': 'Users',
            'userName': 'testUser1',
            'securityLevel': 'Authentication and privacy',
            'authenticationProtocol': 'SHA512',
            'authenticationPassphrase': 'authPass',
            'privacyProtocol': 'AES-256',
            'privacyPassphrase': '1234567812345678'
        }
        self._snmp_v3_users.create(resource)
        mock_create.assert_called_once_with(resource, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._snmp_v3_users.get('0ca1b9e9-3c30-405f-b450-abd36730aa38')

        mock_get.assert_called_once_with('0ca1b9e9-3c30-405f-b450-abd36730aa38')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        self._snmp_v3_users.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_uri_called_once(self, mock_create):
        uri = '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        self._snmp_v3_users.get_by('uri', uri)
        mock_create.assert_called_once_with('uri', uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_create):
        resource = {
            'authenticationPassphrase': 'newAuthPass',
            'privacyPassphrase': 8765432187654321,
            'uri': '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        }
        self._snmp_v3_users.update(resource)
        mock_create.assert_called_once_with(resource, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_create):
        id_or_uri = '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        self._snmp_v3_users.delete(id_or_uri)
        mock_create.assert_called_once_with(id_or_uri, timeout=-1)
