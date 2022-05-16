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
from hpeOneView.resources.settings.appliance_network_interfaces import ApplianceNetworkInterfaces
from hpeOneView.resources.resource import Resource


class ApplianceNetworkInterfacesTest(unittest.TestCase):
    resource_info = {"applianceNetworks": [{
                     "interfaceName": "Appliance test",
                     "device": "eth0",
                     "macAddress": "00:50:56:98:f1:3e",
                     "ipv4Type": "STATIC",
                     "ipv6Type": "UNCONFIGURE",
                     "hostname": "test.com",
                     "app1Ipv4Addr": "1.1.1.0",
                     "app2Ipv4Addr": "1.1.1.1",
                     "virtIpv4Addr": "1.1.1.2",
                     "ipv4Subnet": "255.255.0.0",
                     "ipv4Gateway": "1.1.1.5",
                     "ipv4NameServers": [
                         "10.10.10.11",
                         "10.10.10.12"
                     ]}],
                     "members": []}

    uri = '/rest/appliance/network-interfaces'

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._network_interface = ApplianceNetworkInterfaces(self.connection)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_all_called_once(self, mock_get):
        self._network_interface.get_all()
        mock_get.assert_called_once_with(self.uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_mac_address_called_with_known_mac_address(self, mock_get_by_uri):
        mock_get_by_uri.return_value.data = self.resource_info
        self._network_interface.get_by_mac_address('00:50:56:98:f1:3e')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_mac_address_called_with_unknown_mac_address(self, mock_get_by_uri):
        mock_get_by_uri.return_value.data = self.resource_info
        new_resource = self._network_interface.get_by_mac_address('00:50:56:98:f1:31')
        self.assertEqual(new_resource, None)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_all_mac_address_called_once(self, mock_get_by_uri):
        mock_get_by_uri.return_value.data = self.resource_info
        uri = self.uri + '/mac-addresses'
        response = self._network_interface.get_all_mac_address()
        mock_get_by_uri.assert_called_once_with(uri)
        self.assertEqual(response, self.resource_info['members'])
