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

from hpeOneView.connection import connection
from hpeOneView.image_streamer.resources.deployment_plans import DeploymentPlans
from hpeOneView.resources.resource import ResourceHelper, Resource


class DeploymentPlansTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = DeploymentPlans(self.connection)
        self.resource_uri = '/rest/deployment-plans/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.data = {'uri': self.resource_uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, filter='name=TestName',
                                             sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(count=-1, filter=u'', sort=u'', start=0)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'Deployment Plan Name')

        mock_get_by.assert_called_once_with('name', 'Deployment Plan Name')

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once_with_default_type(self, mock_create):
        information = {
            "name": "Deployment Plan Name",
        }
        mock_create.return_value = {}

        self._client.create(information)

        expected_data = {
            "type": "OEDeploymentPlan",
            "name": "Deployment Plan Name",
        }
        mock_create.assert_called_once_with(expected_data, None, -1,
                                            None, False)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once_with_provided_type(self, mock_create):
        information = {
            "type": "OEDeploymentPlan",
            "name": "Deployment Plan Name",
        }
        expected_data = information.copy()
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(expected_data, None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'update')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once(self, mock_get, mock_update):
        information = {
            "type": "OEDeploymentPlan",
            "name": "Deployment Plan Name",
            "description": "Description of the deployment plan",
            "uri": self._client.data["uri"]
        }
        expected_data = information.copy()
        mock_update.return_value = {}

        self._client.update(information)
        mock_update.assert_called_once_with(expected_data,
                                            self.resource_uri, False, -1, None)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_osdp_called_once(self, mock_get_osdp):
        self._client.get_osdp()

        expected_uri = '{}/osdp'.format(self.resource_uri)
        mock_get_osdp.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_usedby_called_once(self, mock_get_usedby):
        self._client.get_usedby()

        expected_uri = '{}/usedby'.format(self.resource_uri)
        mock_get_usedby.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._client.delete(force=False)

        mock_delete.assert_called_once_with(self.resource_uri,
                                            custom_headers=None, force=False,
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        self._client.delete(force=True)

        mock_delete.assert_called_once_with(self.resource_uri,
                                            custom_headers=None, force=True,
                                            timeout=-1)
