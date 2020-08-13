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

from hpeOneView.connection import connection
from hpeOneView.resources.security.users import Users
from hpeOneView.resources.resource import ResourceClient
from hpeOneView.exceptions import HPEOneViewException


class UsersTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._users = Users(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._users.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
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

        self._users.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30,
                                            default_values=self._users.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
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
        mock_update.return_value = {}

        self._users.update(resource, 60)
        mock_update.assert_called_once_with(resource_rest_call, timeout=60,
                                            default_values=self._users.DEFAULT_VALUES, uri='/rest/users')

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'fake'
        self._users.delete(id, force=False, timeout=-1)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_called_once(self, mock_get):
        self._users.get_by('userName', 'OneViewSDK Test User')
        mock_get.assert_called_once_with('/rest/users/OneViewSDK Test User')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_called_with_role(self, mock_get):
        self._users.get_by('role', 'fakerole')
        mock_get.assert_called_once_with('/rest/users/roles/users/fakerole')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_called_with_something_invalid(self, mock_get):
        try:
            self._users.get_by('test', 'test')
        except HPEOneViewException as exception:
            self.assertEqual('Only userName, name and role can be queried for this resource.', exception.args[0])
        else:
            self.fail("Expected Exception was not raised")

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_validate_full_name_called_once(self, mock_create_with_zero_body):

        self._users.validate_full_name('fullname101')

        expected_uri = '/rest/users/validateUserName/fullname101'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_validate_user_name_called_once(self, mock_create_with_zero_body):

        self._users.validate_user_name('userName')

        expected_uri = '/rest/users/validateLoginName/userName'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)
