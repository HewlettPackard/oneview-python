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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import ResourceClient
from hpOneView.exceptions import HPOneViewException


class Users(object):
    """
    Users API client.

    """

    URI = '/rest/users'

    DEFAULT_VALUES = {
        '200': {'type': 'UserAndRoles'},
        '300': {'type': 'UserAndRoles'},
        '500': {'type': 'UserAndRoles'}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of Users. The collection is based on optional
        sorting and filtering and is constrained by start and count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.

                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of Users.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a User.

        Args:
            resource: dict object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def create(self, resource, timeout=-1):
        """
        Creates a User.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, timeout=-1):
        """
        Updates a User.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated resource.

        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES, uri=self.URI)

    def get_by(self, field, value):
        """
        Gets all Users that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter. Accepted values: 'name', 'userName', 'role'
            value: Value to filter.

        Returns:
            list: A list of Users.
        """
        if field == 'userName' or field == 'name':
            return self._client.get(self.URI + '/' + value)
        elif field == 'role':
            value = value.replace(" ", "%20")
            return self._client.get(self.URI + '/roles/users/' + value)['members']
        else:
            raise HPOneViewException('Only userName, name and role can be queried for this resource.')

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
        return self._client.create_with_zero_body(uri=uri, timeout=timeout)

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
        return self._client.create_with_zero_body(uri=uri, timeout=timeout)
