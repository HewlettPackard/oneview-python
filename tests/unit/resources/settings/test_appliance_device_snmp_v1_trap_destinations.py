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

from hpOneView.connection import connection
from hpOneView.resources.resource import Resource, ResourceHelper
from hpOneView.resources.settings.appliance_device_snmp_v1_trap_destinations import ApplianceDeviceSNMPv1TrapDestinations


class ApplianceDeviceSNMPv1TrapDestinationsTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.__appliance_device_snmp_v1_trap_destinations = ApplianceDeviceSNMPv1TrapDestinations(self.connection)
        self.uri = "/rest/appliance/trap-destinations"
        self.__appliance_device_snmp_v1_trap_destinations.data = {"uri": self.uri}

    @mock.patch.object(Resource, 'get_all')
    def test_get_all(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self.__appliance_device_snmp_v1_trap_destinations.get_all(2, 500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self.__appliance_device_snmp_v1_trap_destinations.get_all()
        mock_get_all.assert_called_once_with()

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri):
        uri = "/rest/appliance/trap-destinations/1"
        self.__appliance_device_snmp_v1_trap_destinations.get_by_uri(uri)
        mock_get_by_uri.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        traps = [{'communityString': 'test', 'destination': '1.1.1.1'}, {'communityString': 'public', 'destination': '1.2.3.4'}]
        mock_get_by.return_value = traps
        result = self.__appliance_device_snmp_v1_trap_destinations.get_by("destination", '1.1.1.1')
        mock_get_by.assert_called_once_with("destination", '1.1.1.1')
        self.assertEqual(result, traps)

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        create_uri = "{}/1".format(self.uri)
        trap_id = 1

        resource = {
            'destination': '1.1.1.1',
            'communityString': 'public',
            'port': 162
        }

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self.__appliance_device_snmp_v1_trap_destinations.create(resource, trap_id)
        mock_create.assert_called_once_with(resource_rest_call, uri=create_uri, timeout=-1)

    @mock.patch.object(Resource, 'get_all')
    @mock.patch.object(Resource, 'create')
    def test_create_called_once_with_defaults(self, mock_create, get_all):
        create_uri = "{}/1".format(self.uri)
        mock_create.return_value = {}

        self.__appliance_device_snmp_v1_trap_destinations.create()
        mock_create.assert_called_once_with(None, uri=create_uri, timeout=-1)

    @mock.patch.object(Resource, 'create')
    def test_create_validation_called_once(self, mock_create_validation):
        resource = {
            'destination': '1.1.1.1',
            'communityString': 'public',
            'port': 162
        }

        validation_uri = "{}/validation".format(self.uri)
        resource_rest_call = resource.copy()
        mock_create_validation.return_value = {}

        self.__appliance_device_snmp_v1_trap_destinations.create_validation(resource, timeout=60)
        mock_create_validation.assert_called_once_with(resource_rest_call, uri=validation_uri, timeout=60)

    @mock.patch.object(Resource, 'create')
    def test_create_validation_called_once_with_defaults(self, mock_create_validation):
        validation_uri = "{}/validation".format(self.uri)
        mock_create_validation.return_value = {}

        self.__appliance_device_snmp_v1_trap_destinations.create_validation()
        mock_create_validation.assert_called_once_with(None, uri=validation_uri, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_by_id_called_once(self, mock_get_by_id):
        uri_rest_call = "{0}/1".format(self.uri)
        self.__appliance_device_snmp_v1_trap_destinations.get_by_id(1)
        mock_get_by_id.assert_called_once_with(uri_rest_call)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_default(self, mock_update, mock_ensure_client):
        resource = {
            "destination": "1.1.1.2",
            "uri": self.uri
        }
        self.__appliance_device_snmp_v1_trap_destinations.update(resource)
        mock_update.assert_called_once_with(resource, self.uri, False, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        resource = {
            "uri": self.uri,
            "destination": "1.1.1.2",
        }
        self.__appliance_device_snmp_v1_trap_destinations.update(resource, 70)
        mock_update.assert_called_once_with(resource, self.uri, False, 70, None)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.__appliance_device_snmp_v1_trap_destinations.delete()
        mock_delete.assert_called_once_with()
