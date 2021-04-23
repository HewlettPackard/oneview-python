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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from urllib.parse import quote
from copy import deepcopy

standard_library.install_aliases()


from hpeOneView.resources.resource import Resource


class Users(Resource):
    """
    Users API client.

    """

    URI = '/rest/users'

    def __init__(self, connection, data=None):
        super(Users, self).__init__(connection, data)
        self.__default_values = {
            'type': 'UserAndRoles'
        }

    def validate_user_name(self, user_name, timeout=-1):
        """
        Verifies if a userName is already in use.

        Args:
            user_name:
                The userName to be verified.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns: True if user name is in use, False if it is not.
        """
        uri = self.URI + '/validateLoginName/' + user_name
        return self._helper.do_post(uri, None, timeout, None)

    def validate_full_name(self, full_name, timeout=-1):
        """
        Verifies if a fullName is already in use.

        Args:
            full_name:
                The fullName to be verified.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns: True if full name is in use, False if it is not.
        """
        uri = self.URI + '/validateUserName/' + full_name
        return self._helper.do_post(uri, None, timeout, None)

    def change_password(self, resource, timeout=-1):
        """
        Change one's own password

        Args:
            resource (dict): Object to change password
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        """
        uri = self.URI + '/changePassword'
        return self._helper.do_put(uri, resource, timeout, None)

    def get_role_by_userName(self, userName):
        """
        Gets a user by userName.

        Args:
            name: userName of the user.

        Returns:
            dict: User
        """

        users = self.get_all()

        result = [x for x in users if x['userName'] == userName]
        resource = result[0] if result else None
        if resource:
            uri = self.URI + '/role/' + userName
            self._helper.validate_resource_uri(uri)
            data = self._helper.do_get(uri)
            new_resource = self.new(self._connection, data)
        else:
            new_resource = None

        return new_resource

    def get_by_userName(self, name):
        """
        Gets a complete json body for username

        Args:
          name: userName of the user

        Returns:
           dict: User
        """

        uri = self.URI + '/' + name
        data = self._helper.do_get(uri)
        new_resource = self.new(self._connection, data)

        return new_resource

    def get_user_by_role(self, rolename):
        """
        Gets all the users associated with this role

        Args:
          rolename: rolename of the user

        Returns:
          dict: User
        """

        uri = self.URI + '/roles/users/' + rolename
        encoded_uri = quote(uri)
        data = self._helper.do_get(encoded_uri)
        result = []
        for i in range(0, len(data['members'])):
            result.append(data["members"][i])

        return result

    def create_multiple_user(self, user, timeout=-1):
        """
        Create a multiple user

        Agrs:
          user: multiple user

        Returns:
          dict: User
        """

        uri = self.URI + '?multiResource=true'
        return self._helper.do_post(uri, user, timeout, None)

    def update(self, data=None, timeout=-1, custom_headers=None, force=False):
        """
        Makes a PUT request to update a resource when a request body is required.

        Args:
            data: Data to update the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers: Allows to add custom HTTP headers.
            force: Force the update operation.

        Returns:
            A dict with the updated resource data.
        """
        uri = self.URI

        resource = deepcopy(self.data)
        resource.update(data)

        self.data = self._helper.update(resource, uri, force, timeout, custom_headers)

        return self

    def add_role_to_userName(self, username, data):
        """
        Add roles to a given user name

        Args:
          username: userName of the user
          data: roles to be added

        Returns:
          dict: User
        """

        uri = self.URI + '/' + username + '/roles?multiResource=true'
        print(uri)
        return self._helper.do_post(uri, data, -1, None)

    def update_role_to_userName(self, username, data):
        """
        Update roles to a given user name

        Agrs:
          username: username of the user
          data: roles to be updated

        Return:
          dict: User

        """

        uri = self.URI + '/' + username + '/roles?multiResource=true'
        return self._helper.do_put(uri, data, -1, None)

    def remove_role_from_username(self, username, rolename):
        """
        Removes a specified role from the username

        Args:
          username: username of the user
          rolename: role to be removed from user

        Return:
          dict: User
        """

        rolename = quote(rolename)
        uri = self.URI + '/roles?filter' + '="userName=\'{}\'"&filter="roleName=\'{}\'"'.format(username, rolename)
        print(uri)
        return self._helper.delete(uri, False, -1, None)

    def delete_multiple_user(self, data):
        """
        Delete the multiple users

        Args:
          data: List of users to be deleted

        Returns:
          None

        """

        uri = self.URI + '?&query='

        for i in range(0, len(data)):
            uri = uri + '(loginname=\'{}\')'.format(data[i])
            if i == len(data) - 1:
                break
            uri = uri + quote(' or ')
        print(uri)
        self._helper.delete(uri, timeout=-1,
                            custom_headers=None, force=False)

    def change_administrator_password(self, new_password):
        """
        Change the password for the administrator

        Args:
          new_password: Password to be changed

        Return:
          dict: User
        """

        uri = self.URI + '/administrator/resetPassword'
        return self._helper.do_put(uri, new_password, -1, None)
