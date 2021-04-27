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

        self._users.create(resource)
        mock_create.assert_called_once_with(resource_rest_call, None, -1, None, False)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_called_with_userName(self, mock_get):
        response = {
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
        }
        mock_get.return_value = response
        result = self._users.get_by_userName('testUser')
        mock_get.assert_called_once_with('/rest/users/testUser')
        self.assertEqual(result, response)

    @mock.patch.object(Resource, 'create')
    def test_validate_full_name_called_once(self, mock_post):

        self._users.validate_full_name('fullname101')

        expected_uri = '/rest/users/validateUserName/fullname101'
        mock_post.assert_called_once_with(uri=expected_uri)

    @mock.patch.object(Resource, 'create')
    def test_validate_user_name_called_once(self, mock_post):

        self._users.validate_user_name('userName')

        expected_uri = '/rest/users/validateLoginName/userName'
        mock_post.assert_called_once_with(uri=expected_uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_user_by_role(self, mock_get):
        response = {
            "category": "roles",
            "count": 1,
            "created": "2014-03-18T06:37:41.652Z",
            "eTag": "992",
            "members": [{
                        "category": "roles",
                        "created": None,
                        "eTag": None,
                        "modified": None,
                        "roleName": "Infrastructure administrator",
                        "type": "RoleNameDtoV2",
                        "uri": "/rest/roles/Infrastructure administrator"
                        }],
            "modified": "2014-03-18T06:37:41.653Z",
            "nextPageUri": None,
            "prevPageUri": None,
            "start": 0,
            "total": 1,
            "type": "RoleNameDtoCollectionV2",
            "uri": "/rest/users/role/administrator?count=50&start=0"
        }
        mock_get.return_value.data = response
        result = self._users.get_user_by_role("Infrastructure administrator")
        mock_get.assert_called_once_with("/rest/users/roles/users/Infrastructure%20administrator")
        self.assertEqual(result, response['members'])

    @mock.patch.object(Resource, 'create')
    def test_create_multiple_user(self, mock_post):
        response = [
            {
                "category": "users",
                "created": "2015-11-19T12:25:50.664Z",
                "eTag": "2139354399",
                "emailAddress": "testUser1@example.com",
                "enabled": "true",
                "fullName": "testUser1",
                "mobilePhone": "555-2121",
                "modified": "2015-11-19T12:25:50.664Z",
                "officePhone": "555-1212",
                "password": "myPass1234",
                "permissions": [
                    {
                        "roleName": "Read only",
                        "scopeUri": "/rest/scopes/00bad8f7-1e21-4819-8632-a4c876fcfdd6"
                    }
                ],
                "type": "UserAndPermissions",
                "uri": "/rest/users/testUser1",
                "userName": "testUser1"
            },
            {
                "category": "users",
                "created": "2015-11-19T12:24:57.664Z",
                "eTag": "1979344099",
                "emailAddress": "testUser2@example.com",
                "enabled": "true",
                "fullName": "testUser2",
                "mobilePhone": "555-2121",
                "modified": "2015-11-19T12:24:57.664Z",
                "officePhone": "555-1212",
                "password": "myPass1234",
                "permissions": [
                    {
                        "roleName": "Read only",
                        "scopeUri": None
                    }
                ],
                "type": "UserAndPermissions",
                "uri": "/rest/users/testUser2",
                "userName": "testUser2"
            }
        ]
        mock_post.return_value.data = response
        result = self._users.create_multiple_user(["testUser1", "testUser2"])
        mock_post.assert_called_once_with(["testUser1", "testUser2"], '/rest/users?multiResource=true')
        self.assertEqual(result.data, response)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update(self, mock_update):
        response = {
            "category": "users",
            "created": "2015-11-19T12:03:01.236Z",
            "eTag": "978442108",
            "emailAddress": "testUser@example.com",
            "enabled": True,
            "fullName": "testUser101",
            "mobilePhone": "303-555-1212",
            "modified": "2015-11-19T12:20:59.809Z",
            "officePhone": "303-555-1212",
            "permissions": [
                {
                    "roleName": "Server Administrator",
                    "scopeUri": "/rest/scopes/00bad8f7-1e21-4819-8632-a4c876fcfdd6"
                },
                {
                    "roleName": "Network Administrator",
                    "scopeUri": "/rest/scopes/ed033aac-c516-438e-9570-1301ee951101"
                }
            ],
            "type": "UserAndPermissions",
            "uri": "/rest/users/testUser",
            "userName": "testUser"
        }
        mock_update.return_value = response
        result = self._users.update(response)
        mock_update.assert_called_once_with(response, "/rest/users", False, -1, None)
        self.assertEqual(result.data, response)

    @mock.patch.object(Resource, 'create')
    def test_add_role_to_userName(self, mock_post):
        response = [
            {
                "category": None,
                "created": None,
                "eTag": None,
                "modified": None,
                "roleName": "Read only",
                "type": "RoleNameDtoV2",
                "uri": "/rest/roles/Read only"
            },
            {
                "category": None,
                "created": None,
                "eTag": None,
                "modified": None,
                "roleName": "<another role that may co-exist>",
                "type": "RoleNameDtoV2",
                "uri": "/rest/roles/<another role that may co-exist>"
            }
        ]
        request = [
            {
                "roleName": "Infrastructure administrator"
            },
            {
                "roleName": "Read only"
            }
        ]
        mock_post.return_value.data = response
        result = self._users.add_role_to_userName("testUser", request)
        mock_post.assert_called_once_with(request, "/rest/users/testUser/roles?multiResource=true")
        self.assertEqual(response, result.data)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_role_to_userName(self, mock_put):
        response = [
            {
                "category": None,
                "created": None,
                "eTag": None,
                "modified": None,
                "roleName": "Backup administrator",
                "type": "RoleNameDtoV2",
                "uri": "/rest/roles/Backup administrator"
            }
        ]
        request = [
            {
                "roleName": "Infrastructure administrator"
            },
            {
                "roleName": "Read only"
            }
        ]
        mock_put.return_value = response
        result = self._users.update_role_to_userName("testUser", request)
        mock_put.assert_called_once_with(request, "/rest/users/testUser/roles?multiResource=true")
        self.assertEqual(response, result)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_role_to_userName(self, mock_delete):
        mock_delete.return_value = True
        self._users.remove_role_from_username("testUser", "Read only")
        uri = "/rest/users/roles?filter=\"userName='testUser'\"&filter=\"roleName='Read%20only'\""
        mock_delete.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_multiple_user(self, mock_delete):
        mock_delete.return_value = True
        self._users.delete_multiple_user(["testUser1", "testUser2"])
        uri = "/rest/users?query=(loginname='testUser1')%20or%20(loginname='testUser2')"
        mock_delete.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_change_password(self, mock_post):
        response = {
            "category": None,
            "created": None,
            "emailAddress": "",
            "enabled": True,
            "eTag": None,
            "fullName": "Default appliance administrator",
            "mobilePhone": "",
            "modified": None,
            "officePhone": "",
            "type": "UserDtoV2",
            "uri": "/rest/users/administrator",
            "userName": "administrator"
        }
        request = {
            "newPassword": "password123",
            "oldPassword": "password1234",
            "userName": "user1"
        }
        mock_post.return_value = response
        result = self._users.change_password(request)
        mock_post.assert_called_once_with(request, "/rest/users/changePassword")
        self.assertEqual(result, response)

    @mock.patch.object(Resource, 'get_all')
    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_role_by_userName(self, mock_get, mock_get_all):
        mock_get_all.return_value = [{"userName": "testUser"}]
        role_list = {
            "category": "roles",
            "count": 1,
            "created": "2014-03-18T06:37:41.652Z",
            "eTag": "992",
            "members": [{
                        "category": "roles",
                        "created": None,
                        "eTag": None,
                        "modified": None,
                        "roleName": "Infrastructure administrator",
                        "type": "RoleNameDtoV2",
                        "uri": "/rest/roles/Infrastructure administrator"
                        }],
            "modified": "2014-03-18T06:37:41.653Z",
            "nextPageUri": None,
            "prevPageUri": None,
            "start": 0,
            "total": 1,
            "type": "RoleNameDtoCollectionV2",
            "uri": "/rest/users/role/administrator?count=50&start=0"
        }
        mock_get.return_value.data = role_list
        result = self._users.get_role_by_userName("testUser")
        mock_get.assert_called_once_with("/rest/users/role/testUser")
        self.assertEqual(result, role_list['members'])

    @mock.patch.object(Resource, 'get_all')
    def test_get_role_by_userName_does_not_exit(self, mock_get_all):
        mock_get_all.return_value = [{"userName": "testUser"}]
        result = self._users.get_role_by_userName("testUser1")
        self.assertEqual(result, None)
