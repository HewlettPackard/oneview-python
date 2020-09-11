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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

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
        Change one's own password, email, phone numbers, enable/disable, of self with proper privileges
        by supplying all the values. The 'currentPassword' field must be present with the 'password' field
        while changing one's own password. User can not add any permissions or replace permissions to self.

        Args:
            resource (dict): Object to change password
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        """
        uri = self.URI
        return self._helper.do_put(uri, resource, timeout, None)

    def get_by_userName(self, userName):
        """
        Gets a user by userName.

        Args:
            name: userName of the user.

        Returns:
            dict: User.
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
