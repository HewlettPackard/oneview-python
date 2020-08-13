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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import ResourceClient


class ApplianceDeviceSNMPv3Users(object):
    """
    ApplianceDeviceSNMPv3Users API client [Available only since API 600].

    As part of SNMPv3 trap forwarding support, the appliance provides APIs for creating User-based Security Model (USM) and forwarding destinations.
    The following protocols are supported while defining USM.

    Authentication protocols: MD5 / SHA1 / SHA256 / SHA384 / SHA512
    Privacy protocols: AES / DES
    The security levels supported while defining USM are None, Authentication only and both Authentication and Privacy.

    """
    URI = '/rest/appliance/snmpv3-trap-forwarding/users'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Creates a new SNMPv3 user.
        This user will be used for sending the SNMPv3 trap to the associated destinations.
        One user can be assigned to multiple destinations.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.

        """
        return self._client.create(resource, timeout=timeout)

    def get(self, id_or_uri):
        """
        Returns the SNMPv3 user with the specified ID, if it exists.

        Args:
            id_or_uri: ID or URI of SNMPv3 user.

        Returns:
            dict: Appliance SNMPv3 user.
        """
        return self._client.get(id_or_uri)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Lists all SNMPv3 Users.

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
            list: A list of SNMPv3 Users.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get_by(self, field, value):
        """
        Gets all SNMPv3 users that match the filter.
        The search is case-insensitive.

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of SNMPv3 Users.
        """
        return self._client.get_by(field, value)

    def delete_all(self, filter=None, timeout=-1):
        """
        Delete an SNMPv3 User based on User name specified in filter. The user will be deleted only if it has no associated destinations.

        Args:
            username: ID or URI of SNMPv3 user.
            filter: A general filter/query string to narrow the list of items returned.
                    The default is no filter - all resources are returned.

        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        return self._client.delete_all(filter=filter, timeout=timeout)

    def delete(self, id_or_uri, timeout=-1):
        """
        Delete an SNMPv3 User based on User Id specified in {Id}.
        The user will be deleted only if it has no associated destinations.

        Args:
            id_or_uri: dict object to delete
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(id_or_uri, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates SNMPv3 User based on User Id as specified in {Id}

        Args:
            resource: dict object with changes.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated appliance SNMPv3 user.
        """
        return self._client.update(resource, timeout=timeout)
