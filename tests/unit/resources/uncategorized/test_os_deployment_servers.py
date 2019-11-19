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

from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.uncategorized.os_deployment_servers import OsDeploymentServers


class OsDeploymentServersTest(TestCase):
    RESOURCE_ID = "81decf85-0dff-4a5e-8a95-52994eeb6493"
    RESOURCE_URI = "/rest/os-deployment-servers/" + RESOURCE_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._os_deployment_servers = OsDeploymentServers(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        fields = 'name'
        view = 'expand'
        query = 'query'

        self._os_deployment_servers.get_all(2, 500, filter=filter, sort=sort, fields=fields, view=view, query=query)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, fields=fields, view=view, query=query)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._os_deployment_servers.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', fields='', view='', query='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        self._os_deployment_servers.get(self.RESOURCE_ID)
        mock_get.assert_called_once_with(self.RESOURCE_ID)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        self._os_deployment_servers.get(self.RESOURCE_URI)
        mock_get.assert_called_once_with(self.RESOURCE_URI)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        os_deployment_servers = [{'name': 'name1'}, {'name': 'name2'}]
        mock_get_by.return_value = os_deployment_servers
        result = self._os_deployment_servers.get_by("name", "test name")
        mock_get_by.assert_called_once_with("name", "test name")
        self.assertEqual(result, os_deployment_servers)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_name_sould_return_none_when_resource_is_not_found(self, mock_get_by):
        mock_get_by.return_value = []
        response = self._os_deployment_servers.get_by_name("test name")
        self.assertEqual(response, None)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_name_called_once(self, mock_get_by):
        os_deployment_servers = [{'name': 'test name', 'id': 1}, {'name': 'test name', 'id': 2}]
        mock_get_by.return_value = os_deployment_servers
        result = self._os_deployment_servers.get_by_name("test name")
        mock_get_by.assert_called_once_with("name", "test name")
        self.assertEqual(result, {'name': 'test name', 'id': 1})

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        os_deployment_server = {
            "name": "DeploymentServer"
        }
        self._os_deployment_servers.add(os_deployment_server)
        mock_create.assert_called_once_with(os_deployment_server, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        os_deployment_server = {
            "name": "DeploymentServer"
        }
        self._os_deployment_servers.add(os_deployment_server, 70)
        mock_create.assert_called_once_with(os_deployment_server, timeout=70)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, update):
        os_deployment_server = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "DeploymentServer"
        }
        self._os_deployment_servers.update(os_deployment_server)
        update.assert_called_once_with(os_deployment_server, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        os_deployment_server = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "DeploymentServer"
        }
        self._os_deployment_servers.update(os_deployment_server, True, 70)
        mock_update.assert_called_once_with(os_deployment_server, force=True, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._os_deployment_servers.delete(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._os_deployment_servers.delete(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_networks_called_once(self, mock_get):
        networks = [{"name": "net1"}, {"name": "net2"}]
        mock_get.return_value = networks
        result = self._os_deployment_servers.get_networks()

        mock_get.assert_called_once_with('/rest/deployment-servers/network')

        self.assertEqual(result, networks)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_appliances_called_once_with_defaults(self, mock_get_all):
        appliances = [{"name": "app1"}, {"name": "app2"}]
        mock_get_all.return_value = appliances
        result = self._os_deployment_servers.get_appliances()

        mock_get_all.assert_called_once_with(0, -1, filter='', fields='', query='', sort='',
                                             uri='/rest/deployment-servers/image-streamer-appliances', view='')

        self.assertEqual(result, appliances)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_appliances_called_once(self, mock_get_all):
        appliances = [{"name": "app1"}, {"name": "app2"}]
        mock_get_all.return_value = appliances

        result = self._os_deployment_servers.get_appliances(1, 10, filter='status=Connected', fields='name',
                                                            query='teste <> name', sort='desc=name', view='expand')

        self.assertEqual(result, appliances)
        mock_get_all.assert_called_once_with(1, 10, filter='status=Connected', fields='name', query='teste <> name',
                                             sort='desc=name', uri='/rest/deployment-servers/image-streamer-appliances',
                                             view='expand')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_appliance_called_once(self, mock_get):
        appliance = {"name": "app1"}
        mock_get.return_value = appliance
        appliance_id = "123456"

        result = self._os_deployment_servers.get_appliance(appliance_id)

        mock_get.assert_called_once_with('/rest/deployment-servers/image-streamer-appliances/123456')
        self.assertEqual(result, appliance)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_appliance_called_once_with_fields(self, mock_get):
        appliance = {"name": "app1"}
        mock_get.return_value = appliance
        appliance_id = "123456"

        result = self._os_deployment_servers.get_appliance(appliance_id, fields='field')

        mock_get.assert_called_once_with('/rest/deployment-servers/image-streamer-appliances/123456?fields=field')
        self.assertEqual(result, appliance)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_appliance_by_name_called_once(self, mock_get_all):
        appliances = [{"name": "app1"}, {"name": "app2"}]
        mock_get_all.return_value = appliances

        result = self._os_deployment_servers.get_appliance_by_name("app2")

        self.assertEqual(result, {"name": "app2"})

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_appliance_by_name_should_return_none_when_not_match(self, mock_get_all):
        appliances = []
        mock_get_all.return_value = appliances

        result = self._os_deployment_servers.get_appliance_by_name("app2")

        self.assertEqual(result, None)
