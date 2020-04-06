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
from hpOneView.resources.hypervisors.hypervisor_managers import HypervisorManagers
from hpOneView.resources.resource import ResourceClient


class HypervisorManagersTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._hypervisor_managers = HypervisorManagers(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            type="HypervisorManagerV2",
            name="172.18.13.11",
            displayName="vcenter",
            hypervisorType="Vmware",
            username="dcs",
            password="dcs",
	    initialScopeUris=[]
        )

        mock_create.return_value = {}
        self._hypervisor_managers.add(resource, 70)
        mock_create.assert_called_once_with(resource.copy(), timeout=70)


    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        resource = dict(
            type="HypervisorManagerV2",
            name="172.18.13.11",
            displayName="vcenter",
            hypervisorType="Vmware",
            username="dcs",
            password="dcs",
            initialScopeUris=[],
        )
        self._hypervisor_managers.add(resource)
        mock_create.assert_called_once_with(resource.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        fields = 'name'
        view = 'expand'
        query = 'query'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'

        self._hypervisor_managers.get_all(2, 500, filter=filter, sort=sort, fields=fields, view=view, query=query, scope_uris=scope_uris)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, fields=fields, view=view, query=query, scope_uris=scope_uris)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._hypervisor_managers.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', fields='', view='', query='', scope_uris='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        uri = "/rest/hypervisor-managers/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._hypervisor_managers.get(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._hypervisor_managers.get(id)
        mock_get.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        hypervisor_managers = [{'name': 'name1', 'displayName': 'display1'}, {'name': 'name2', 'displayName': 'display2'}]
        mock_get_by.return_value = hypervisor_managers
        result = self._hypervisor_managers.get_by("displayName", "display1")
        mock_get_by.assert_called_once_with("displayName", "display1")
        self.assertEqual(result, hypervisor_managers)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_name_should_return_none_when_resource_is_not_found(self, mock_get_by):
        mock_get_by.return_value = []
        response = self._hypervisor_managers.get_by_name("test")
        mock_get_by.assert_called_once_with("name", "test")
        self.assertEqual(response, None)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_name_called_once(self, mock_get_by):
        hypervisor_managers = [{'name': 'test name', 'id': 1}, {'name': 'test name', 'id': 2}]
        mock_get_by.return_value = hypervisor_managers
        result = self._hypervisor_managers.get_by_name("test name")
        mock_get_by.assert_called_once_with("name", "test name")
        self.assertEqual(result, {'name': 'test name', 'id': 1})

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_default(self, mock_update):
        hypervisor_manager = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "HypervisorManager"
        }
        self._hypervisor_managers.update(hypervisor_manager)
        mock_update.assert_called_once_with(hypervisor_manager, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        hypervisor_manager = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "HypervisorManager"
        }
        self._hypervisor_managers.update(hypervisor_manager, True, 70)
        mock_update.assert_called_once_with(hypervisor_manager, force=True, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        uri = '/rest/hypervisor-managers/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._hypervisor_managers.delete(uri, force=True, timeout=50)
        mock_delete.assert_called_once_with(uri, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._hypervisor_managers.delete(id)
        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

