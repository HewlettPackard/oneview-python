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
from hpOneView.resources.hypervisors.hypervisor_cluster_profiles import HypervisorClusterProfiles
from hpOneView.resources.resource import Resource, ResourceHelper


class HypervisorClusterProfilesTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._hypervisor_cluster_profiles = HypervisorClusterProfiles(self.connection)
        self.uri = "/rest/hypervisor-cluster-profiles"
        self._hypervisor_cluster_profiles.data = {"uri": self.uri}

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            name="ClusterProfile",
        )

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._hypervisor_cluster_profiles.create(resource, timeout=70)
        mock_create.assert_called_once_with(resource_rest_call, timeout=70)

    @mock.patch.object(Resource, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        resource = dict(
            name="ClusterProfile",
        )

        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._hypervisor_cluster_profiles.create(resource)
        mock_create.assert_called_once_with(resource_rest_call)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_vswitch_layout_called_once(self, mock_create_vswitch):
        resource = dict(
            virtualSwitchType="Standard",
            type="vmware",
        )

        vswitch_uri = "{}/virtualswitch-layout".format(self.uri)
        resource_rest_call = resource.copy()
        mock_create_vswitch.return_value = {}

        self._hypervisor_cluster_profiles.create_virtual_switch_layout(resource, timeout=60)
        mock_create_vswitch.assert_called_once_with(resource_rest_call, vswitch_uri, 60)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_vswitch_layout_called_once_with_defaults(self, mock_create_vswitch):
        resource = dict(
            virtualSwitchType="Standard",
            type="vmware",
        )

        vswitch_uri = "{}/virtualswitch-layout".format(self.uri)
        resource_rest_call = resource.copy()
        mock_create_vswitch.return_value = {}

        self._hypervisor_cluster_profiles.create_virtual_switch_layout(resource)
        mock_create_vswitch.assert_called_once_with(resource_rest_call, vswitch_uri, -1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_compliance_preview(self, mock_get):
        uri_rest_call = '{}/compliance-preview'.format(self.uri)

        self._hypervisor_cluster_profiles.get_compliance_preview()
        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        query = 'query'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'

        self._hypervisor_cluster_profiles.get_all(2, 500, filter=filter, sort=sort, query=query, scope_uris=scope_uris)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query=query, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._hypervisor_cluster_profiles.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='', scope_uris='')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri):
        uri = "/rest/hypervisor-cluster-profiles/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._hypervisor_cluster_profiles.get_by_uri(uri)
        mock_get_by_uri.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        cluster_profiles = [{'name': 'name1', 'path': 'dc1'}, {'name': 'name2', 'path': 'dcs2'}]
        mock_get_by.return_value = cluster_profiles
        result = self._hypervisor_cluster_profiles.get_by("path", 'dc1')
        mock_get_by.assert_called_once_with("path", "dc1")
        self.assertEqual(result, cluster_profiles)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_name_called_once(self, mock_get_by_name):
        cluster_profiles = [{'name': 'name1', 'path': 'dc1'}, {'name': 'name2', 'path': 'dcs2'}]
        mock_get_by_name.return_value = cluster_profiles
        result = self._hypervisor_cluster_profiles.get_by_name("name1")
        mock_get_by_name.assert_called_once_with("name", "name1")
        self.assertEqual(result.data['path'], 'dc1')

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_default(self, mock_update, mock_ensure_client):
        resource = {
            "name": "NewCluster",
            "uri": self.uri
        }
        self._hypervisor_cluster_profiles.update(resource)
        mock_update.assert_called_once_with(resource, self.uri, False, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        resource = {
            "uri": self.uri,
            "name": "NewCluster"
        }
        self._hypervisor_cluster_profiles.update(resource, 70)
        mock_update.assert_called_once_with(resource, self.uri, False, 70, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._hypervisor_cluster_profiles.delete(force=False)
        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        self._hypervisor_cluster_profiles.delete(force=True)
        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=True, timeout=-1)
