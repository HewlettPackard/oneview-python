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
from hpeOneView.exceptions import HPEOneViewException


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
            user_name (str):
                The userName to be verified.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns: True if user name is in use, False if it is not.
        """
        uri = self.URI + '/validateLoginName/' + user_name
        return self.create(uri=uri)

    def validate_full_name(self, full_name, timeout=-1):
        """
        Verifies if a fullName is already in use.

        Args:
            full_name (str):
                The fullName to be verified.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns: True if full name is in use, False if it is not.
        """
        uri = self.URI + '/validateUserName/' + full_name
        return self.create(uri=uri)

    def change_password(self, resource):
        """
        Change one's own password

        Args:
            resource (dict): Object to change password
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        """
        uri = self._helper.build_uri('changePassword')
        return self._helper.create(resource, uri)

    def get_role_associated_with_userName(self, userName):
        """
        Gets a user by userName.

        Args:
            name (str): userName of the user.

        Returns:
            dict object: User
        """

        users = self.get_all()

        result = [x for x in users if x['userName'] == userName]
        resource = result[0] if result else None
        if resource:
            uri = self.URI + '/role/' + userName
            data = self.get_by_uri(uri).data
            result = data['members']
            return result
        else:
            return None

    def get_by_userName(self, name):
        """
        Gets a complete json body for username

        Args:
          name (str): userName of the user

        Returns:
           dict object: User
        """

        uri = self._helper.build_uri(name)
        try:
            resource = self.get_by_uri(uri)
        except HPEOneViewException:
            resource = None

        return resource

    def get_user_by_role(self, rolename):
        """
        Gets all the users associated with this role

        Args:
          rolename (str): rolename of the user

        Returns:
          list: User
        """

        rolename = quote(rolename)
        uri = self.URI + '/roles/users/' + rolename
        data = self.get_by_uri(uri).data
        result = []
        for i in range(0, len(data['members'])):
            result.append(data["members"][i])

        return result

    def create_multiple_user(self, data):
        """
        Create a multiple user

        Agrs:
          data (list): multiple user

        Returns:
          dict object: User
        """

        uri = self.URI + '?multiResource=true'
        return self.create(data, uri)

    def update(self, data=None, timeout=-1, custom_headers=None, force=False):
        """
        Makes a PUT request to update a resource when a request body is required.

        Args:
            data (dict): Data to update the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers: Allows to add custom HTTP headers.
            force: Force the update operation.

        Returns:
            A dict with the updated resource data.
        """

        resource = deepcopy(self.data)
        resource.update(data)

        self.data = self._helper.update(resource, self.URI, force, timeout, custom_headers)

        return self

    def add_role_to_userName(self, username, data):
        """
        Add roles to a given user name

        Args:
          username (str): userName of the user
          data (list): roles to be added

        Returns:
          dict object: User
        """

        uri = self.URI + '/' + username + '/roles?multiResource=true'
        return self.create(data, uri)

    def update_role_to_userName(self, username, data):
        """
        Update roles to a given user name

        Agrs:
          username (str): username of the user
          data (list): roles to be updated

        Return:
          dict: User
        """

        uri = self.URI + '/' + username + '/roles?multiResource=true'
        return self._helper.update(data, uri)

    def remove_role_from_username(self, username, data):
        """
        Removes a specified role from the username

        Args:
          username (str): username of the user
          data (str/list): list role to be removed from user

        Return:
          boolean
        """

        rolelist_query = self.query_filter(data)
        uri = self.URI + '/roles?filter' + '="userName=\'{}\'{}'.format(username, rolelist_query)
        return self._helper.delete(uri)

    def delete_multiple_user(self, data):
        """
        Delete the multiple users

        Args:
          data (list): List of users to be deleted

        Returns:
          None
        """

        uri = self.URI + '?query='

        for i in range(0, len(data)):
            uri = uri + '(loginname=\'{}\')'.format(data[i])
            if i == len(data) - 1:
                break
            uri = uri + quote(' or ')
        self._helper.delete(uri)

    def query_filter(self, filters):

        formated_filter = ''
        base_query = "\"&filter=\"roleName=\'{}\'\""
        if isinstance(filters, list):
            for role in filters:
                formated_filter += base_query.format(quote(role))
            return formated_filter

        if isinstance(filters, str):
            return base_query.format(quote(filters))
