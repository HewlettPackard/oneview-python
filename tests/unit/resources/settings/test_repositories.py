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
from hpeOneView.resources.settings.repositories import Repositories
from hpeOneView.resources.resource import Resource, ResourcePatchMixin


class RepositoriesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._repositories = Repositories(self.connection)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._repositories.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter, sort)

    @mock.patch.object(Resource, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            "repositoryName": "Repo_Name",
            "userName": "Admin",
            "password": "*******",
            "repositoryURI": "https://172.20.3.65/repositoryFolder",
            "repositoryType": "FirmwareExternalRepo",
            "base64data": ""
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._repositories.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, 30)

    @mock.patch.object(Resource, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            "repositoryName": "Repo_Name",
            "userName": "Admin",
            "password": "*******",
            "repositoryURI": "https://172.20.3.65/repositoryFolder",
            "base64data": ""
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._repositories.update(resource, 60)
        mock_update.assert_called_once_with(resource_rest_call, 60)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._repositories.delete(force=False, timeout=-1)
        mock_delete.assert_called_once_with(force=False, timeout=-1)

    @mock.patch.object(Resource, 'get_by_name')
    def test_get_by_called_once(self, mock_get_by):
        self._repositories.get_by_name('Repository Name')
        mock_get_by.assert_called_once_with('Repository Name')

    @mock.patch.object(Resource, 'get_by_id')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/repositories/3518be0e-17c1-4189-8f81-83f3724f6155'

        self._repositories.get_by_id(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._repositories.patch('/rest/fake/re123', 'replace', '/repositoryName', ['/rest/fake/repository123'], 1)
        mock_patch.assert_called_once_with('/rest/fake/re123', 'replace', '/repositoryName',
                                           ['/rest/fake/repository123'], 1)
