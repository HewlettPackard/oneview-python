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
from hpeOneView.resources.storage.storage_systems import StorageSystems
from hpeOneView.resources.resource import Resource, ResourceHelper


class StorageSystemsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._storage_systems = StorageSystems(self.connection)
        self._storage_systems.data = {'uri': '/rest/storage-systems/ad28cf21-8b15-4f92-bdcf-51cb2042db32'}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_systems.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(count=500, filter='name=TestName', sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_systems.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter='', sort='', start=0)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_host_types_called_once(self, mock_get):
        storage_systems_host_types_uri = "/rest/storage-systems/host-types"
        self._storage_systems.get_host_types()
        mock_get.assert_called_once_with(storage_systems_host_types_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_managed_ports_called_once_with_uri(self, mock_get):
        storage_systems_managed_ports_uri = "{}/managedPorts".format(self._storage_systems.data["uri"])
        self._storage_systems.get_managed_ports()
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_managed_ports_called_once_with_id(self, mock_get):
        storage_systems_managed_ports_uri = "{}/managedPorts".format(self._storage_systems.data["uri"])
        self._storage_systems.get_managed_ports()
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_managed_ports_called_once_with_uri_and_port_id(self, mock_get):
        port_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_systems_managed_ports_uri = \
            "{}/managedPorts/C862833E-907C-4124-8841-BDC75444CF76".format(self._storage_systems.data["uri"])
        self._storage_systems.get_managed_ports(port_id)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_managed_ports_called_once_with_id_and_port_id(self, mock_get):
        port_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_systems_managed_ports_uri = \
            "{}/managedPorts/C862833E-907C-4124-8841-BDC75444CF76".format(self._storage_systems.data["uri"])
        self._storage_systems.get_managed_ports(port_id)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_managed_ports_called_once_with_uri_and_port_uri(self, mock_get):
        port_uri = \
            "{}/managedPorts/C862833E-907C-4124-8841-BDC75444CF76".format(self._storage_systems.data["uri"])

        storage_systems_managed_ports_uri = \
            "{}/managedPorts/C862833E-907C-4124-8841-BDC75444CF76".format(self._storage_systems.data["uri"])

        self._storage_systems.get_managed_ports(port_uri)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_managed_ports_called_once_with_id_and_port_uri(self, mock_get):
        port_uri = \
            "{}/managedPorts/C862833E-907C-4124-8841-BDC75444CF76".format(self._storage_systems.data["uri"])

        storage_systems_managed_ports_uri = \
            "{}/managedPorts/C862833E-907C-4124-8841-BDC75444CF76".format(self._storage_systems.data["uri"])

        self._storage_systems.get_managed_ports(port_uri)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        storage_system = {
            "ip_hostname": "example.com",
            "username": "username",
            "password": "password"
        }
        self._storage_systems.add(storage_system)
        mock_create.assert_called_once_with(storage_system, None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once(self, mock_create):
        storage_system = {
            "ip_hostname": "example.com",
            "username": "username",
            "password": "password"
        }
        self._storage_systems.add(storage_system, 70)
        mock_create.assert_called_once_with(storage_system, None, 70, None, False)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_storage_pools_called_once(self, mock_get):
        storage_systems_managed_ports_uri = "{}/storage-pools".format(self._storage_systems.data["uri"])
        self._storage_systems.get_storage_pools()
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceHelper, 'do_put')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once_with_defaults(self, mock_do_get, mock_do_put):
        storage_system = {
            "type": "StorageSystemV3",
            "credentials": {
                "ip_hostname": "example.com",
                "username": "username"
            },
            "name": "StoreServ1",
        }
        uri = self._storage_systems.data["uri"]
        update_request = storage_system.copy()
        update_request["uri"] = uri

        mock_do_get.return_value = storage_system
        self._storage_systems.update(storage_system)

        mock_do_put.assert_called_once_with(uri, update_request, -1, None)

    @mock.patch.object(ResourceHelper, 'do_put')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once(self, mock_do_get, mock_do_put):
        storage_system = {
            "type": "StorageSystemV3",
            "credentials": {
                "ip_hostname": "example.com",
                "username": "username"
            },
            "name": "StoreServ1",
        }
        uri = self._storage_systems.data["uri"]
        update_request = storage_system.copy()
        update_request["uri"] = uri

        mock_do_get.return_value = storage_system
        self._storage_systems.update(storage_system, 70)

        mock_do_put.assert_called_once_with(uri, update_request, 70, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._storage_systems.remove(force=True, timeout=50)

        mock_delete.assert_called_once_with(self._storage_systems.data["uri"],
                                            custom_headers={'If-Match': '*'}, force=True, timeout=50)

    @mock.patch.object(Resource, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        if_match_header = {'If-Match': '*'}
        self._storage_systems.remove()

        mock_delete.assert_called_once_with(force=False, timeout=-1, custom_headers=if_match_header)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_by):
        self._storage_systems.get_by("name", "test name")
        mock_get_by.assert_called_once_with(count=-1, filter='"name=\'test name\'"', sort='', start=0)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_called_once(self, mock_get_all):
        self._storage_systems.get_by_name("test name")
        mock_get_all.assert_called_once_with(count=-1, filter='"name=\'test name\'"', sort='', start=0)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_ip_hostname_find_value(self, get_all):
        get_all.return_value = [
            {"credentials": {
                "ip_hostname": "10.0.0.0",
                "username": "username"}},
            {"credentials": {
                "ip_hostname": "20.0.0.0",
                "username": "username"}},
        ]

        result = self._storage_systems.get_by_ip_hostname("20.0.0.0")
        get_all.assert_called_once()
        self.assertEqual(
            {"credentials": {
                "ip_hostname": "20.0.0.0",
                "username": "username"}}, result.data)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_ip_hostname_value_not_found(self, get_all):
        get_all.return_value = [
            {"credentials": {
                "ip_hostname": "10.0.0.0",
                "username": "username"}},
            {"credentials": {
                "ip_hostname": "20.0.0.0",
                "username": "username"}},
        ]

        result = self._storage_systems.get_by_ip_hostname("30.0.0.0")
        get_all.assert_called_once()
        self.assertIsNone(result)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_hostname(self, get_all):
        get_all.return_value = [
            {"hostname": "10.0.0.0",
             "username": "username"},
            {"hostname": "20.0.0.0",
             "username": "username"}
        ]

        result = self._storage_systems.get_by_hostname("20.0.0.0")
        get_all.assert_called_once()
        self.assertEqual(
            {"hostname": "20.0.0.0",
             "username": "username"}, result.data)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_hostname_with_None_response(self, get_all):
        get_all.return_value = [
            {"hostname": "10.0.0.0",
             "username": "username"}
        ]

        result = self._storage_systems.get_by_hostname("20.0.0.0")
        get_all.assert_called_once()
        self.assertEqual(None, result)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_reachable_ports_called_once(self, mock_get):
        reachable_ports_uri = "{}/reachable-ports?start=0&count=-1".format(self._storage_systems.data["uri"])
        self._storage_systems.get_reachable_ports()
        mock_get.assert_called_once_with(reachable_ports_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_reachable_ports_called_once_with_networks(self, mock_get):
        networks = ['rest/net1', 'rest/net2']
        reachable_ports_uri = "{}/reachable-ports?networks='rest/net1,rest/net2'&start=0&count=-1".format(self._storage_systems.data["uri"])
        self._storage_systems.get_reachable_ports(networks=networks)
        mock_get.assert_called_once_with(reachable_ports_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_templates_called_once(self, mock_get):
        templates_uri = "{}/templates?start=0&count=-1".format(self._storage_systems.data["uri"])
        self._storage_systems.get_templates()
        mock_get.assert_called_once_with(templates_uri)
