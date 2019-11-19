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
from hpOneView.resources.settings.appliance_device_snmp_v1_trap_destinations import ApplianceDeviceSNMPv1TrapDestinations
from hpOneView.resources.resource import ResourceClient


class ApplianceDeviceSNMPv1TrapDestinationsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._snmp_v1_trap_dest = ApplianceDeviceSNMPv1TrapDestinations(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get):
        self._snmp_v1_trap_dest.get_all()
        mock_get.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = {
            'destination': '1.1.1.1',
            'communityString': 'public',
            'port': 162
        }
        trap_id = 1
        self._snmp_v1_trap_dest.create(resource, trap_id)
        mock_create.assert_called_once_with(resource, uri="/rest/appliance/trap-destinations/%s" % (trap_id), timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._snmp_v1_trap_dest.get('1')

        mock_get.assert_called_once_with('1')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/appliance/trap-destinations/1'
        self._snmp_v1_trap_dest.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_uri_called_once(self, mock_create):
        uri = '/rest/appliance/trap-destinations/1'
        self._snmp_v1_trap_dest.get_by('uri', uri)
        mock_create.assert_called_once_with('uri', uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_destination_called_once(self, mock_create):
        dest = '1.1.1.1'
        self._snmp_v1_trap_dest.get_by('destination', dest)
        mock_create.assert_called_once_with('destination', dest)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_create):
        resource = {
            'communityString': 'test',
            'port': 162,
            'uri': '/rest/appliance/trap-destinations/1'
        }
        self._snmp_v1_trap_dest.update(resource)
        mock_create.assert_called_once_with(resource, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_create):
        id_or_uri = '/rest/appliance/trap-destinations/1'
        self._snmp_v1_trap_dest.delete(id_or_uri)
        mock_create.assert_called_once_with(id_or_uri, timeout=-1)
