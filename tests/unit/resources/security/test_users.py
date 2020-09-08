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
from hpeOneView.resources.security.users import Users
from hpeOneView.resources.resource import Resource, ResourceHelper


class UsersTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._users = Users(self.connection)

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._users.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter, sort)

    @mock.patch.object(ResourceHelper, 'do_post')
    @mock.patch.object(ResourceHelper, 'create')
    def test_create_should_use_given_values(self, mock_create, mock_post):
        resource = {
            'enabled': 'true',
            'fullName': 'testUser101',
            'mobilePhone': '555-2121',
            'officePhone': '555-1212',
            'password': 'myPass1234',
            'roles': ['Read only'],
            'type': 'UserAndRoles',
            'userName': 'testUser'
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._users.create(resource, timeout=70)
        mock_create.assert_called_once_with(resource_rest_call, timeout=70, '/rest/users')

    @mock.patch.object(Resource, 'get_all')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_by_called_with_userName(self, mock_get, mock_get_all):
        mock_get_all.return_value = [{
            'enabled': 'true',
            'fullName': 'testUser101',
            'mobilePhone': '555-2121',
            'officePhone': '555-1212',
            'password': 'myPass1234',
            'permissions': {
                "roleName": "Infrastructure administrator",
                "scopeUri": "/rest/scopes/00bad8f7-1e21-4819-8632-a4c876fcfdd6"
            },
            'type': 'UserAndRoles',
            'userName': 'testUser'
        }]
        self._users.get_by_userName('OneViewSDK Test User')
        mock_get.assert_called_once_with('/rest/users/role/OneViewSDK Test User')

    @mock.patch.object(Resource, 'get_all')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_by_called_with_role(self, mock_get, mock_get_all):
        mock_get_all.return_value = [{
            'enabled': 'true',
            'fullName': 'testUser101',
            'mobilePhone': '555-2121',
            'officePhone': '555-1212',
            'password': 'myPass1234',
            'permissions': {
                "roleName": "Infrastructure administrator",
                "scopeUri": "/rest/scopes/00bad8f7-1e21-4819-8632-a4c876fcfdd6"
            },
            'type': 'UserAndRoles',
            'userName': 'testUser'
        }]
        self._users.get_by_role('fakerole')
        mock_get.assert_called_once_with('/rest/users/roles/users/fakerole')

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_validate_full_name_called_once(self, mock_post):

        self._users.validate_full_name('fullname101')

        expected_uri = '/rest/users/validateUserName/fullname101'
        mock_post.assert_called_once_with(expected_uri, None, -1, None)

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_validate_user_name_called_once(self, mock_post):

        self._users.validate_user_name('userName')

        expected_uri = '/rest/users/validateLoginName/userName'
        mock_post.assert_called_once_with(expected_uri, None, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_put')
    def test_change_password(self, mock_put, mock_ensure_resource_data):
        request = {
            "currentPassword": "admin12345",
            "enabled": "true",
            "password": "admin1234",
            "userName": "admin"
        }
        self._users.change_password(request)

        expected_uri = '/rest/users/'
        mock_put.assert_called_once_with(expected_uri, request, -1, None)
