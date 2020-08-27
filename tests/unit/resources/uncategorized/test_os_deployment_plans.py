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
from hpOneView.resources.resource import ResourceHelper
from hpOneView.resources.uncategorized.os_deployment_plans import OsDeploymentPlans


class OsDeploymentPlansTest(TestCase):
    RESOURCE_ID = "81decf85-0dff-4a5e-8a95-52994eeb6493"
    RESOURCE_URI = "/rest/os-deployment-plans/" + RESOURCE_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._os_deployment_plans = OsDeploymentPlans(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._os_deployment_plans.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._os_deployment_plans.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_by):
        self._os_deployment_plans.get_by("name", "test name")
        mock_get_by.assert_called_once_with(0, -1, filter='"name=\'test name\'"',
                                            query='', sort='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_sould_return_none_when_resource_is_not_found(self, mock_get_by):
        mock_get_by.return_value = []
        response = self._os_deployment_plans.get_by_name("test name")
        self.assertEqual(response, None)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_called_once(self, mock_get_by):
        self._os_deployment_plans.get_by_name("test name")
        mock_get_by.assert_called_once_with(0, -1, filter='"name=\'test name\'"', query='', sort='')
