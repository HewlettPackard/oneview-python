# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
from hpeOneView.resources.settings.appliance_device_snmp_v3_trap_destinations import ApplianceDeviceSNMPv3TrapDestinations
from hpeOneView.resources.resource import Resource, ResourceHelper


class ApplianceDeviceSNMPv3TrapDestinationsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._snmp_v3_trap_dest = ApplianceDeviceSNMPv3TrapDestinations(self.connection)
        self.uri = "/rest/appliance/snmpv3-trap-forwarding/destinations"
        self._snmp_v3_trap_dest.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        query = 'query'
        self._snmp_v3_trap_dest.get_all(2, 500, filter=filter, sort=sort, query=query)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query=query)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._snmp_v3_trap_dest.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri):
        uri = "/rest/appliance/snmpv3-trap-forwarding/destinations/1"
        self._snmp_v3_trap_dest.get_by_uri(uri)
        mock_get_by_uri.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by_field')
    def test_get_by_name_called_once(self, mock_get_by_field):
        self._snmp_v3_trap_dest.get_by_name('test')
        mock_get_by_field.assert_called_once_with('destinationAddress', 'test')

    @mock.patch.object(ResourceHelper, 'create')
    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create, mock_create_validation):
        validation_uri = "{}/validation".format(self.uri)
        resource = {
            'type': 'Destination',
            'destinationAddress': '1.1.1.1',
            'port': 162,
            'userId': '6b9c6f7b-7a24-4514-b9c9-0c31e086c170'
        }

        resource_validation = {
            'destinationAddress': '1.1.1.1',
        }

        resource_rest_call = resource.copy()
        mock_create.return_value = {}
        mock_create_validation.return_value = {}

        self._snmp_v3_trap_dest.create(resource)
        mock_create_validation.assert_called_once_with(resource_validation, uri=validation_uri, timeout=-1)
        mock_create.assert_called_once_with(resource_rest_call, uri=self.uri, timeout=-1)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_validation_called_once(self, mock_create_validation):
        resource = {
            'destinationAddress': '1.1.1.1',
            'existingDestinations': ['1.2.3.4']
        }

        validation_uri = "{}/validation".format(self.uri)
        resource_rest_call = resource.copy()
        mock_create_validation.return_value = {}

        self._snmp_v3_trap_dest.create_validation(resource['destinationAddress'], resource['existingDestinations'])
        mock_create_validation.assert_called_once_with(resource_rest_call, uri=validation_uri, timeout=-1)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_default(self, mock_update, mock_ensure_client):
        resource = {
            "destinationAddress": "1.1.1.2",
            "uri": self.uri
        }
        self._snmp_v3_trap_dest.update(resource)
        mock_update.assert_called_once_with(resource, self.uri, False, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        resource = {
            "uri": self.uri,
            "destinationAddress": "1.1.1.2",
        }
        self._snmp_v3_trap_dest.update(resource, 70)
        mock_update.assert_called_once_with(resource, self.uri, False, 70, None)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._snmp_v3_trap_dest.delete()
        mock_delete.assert_called_once_with()
