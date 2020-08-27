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


class IdPoolsIpv4Ranges(object):
    """
    The ID pools IPv4 ranges resource provides a Client API for managing IPv4 ranges.
    """
    URI = '/rest/id-pools/ipv4/ranges'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Creates an IPv4 range.

        Args:
            resource (dict): Object to create
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created range.
        """
        return self._client.create(resource, timeout=timeout)

    def get(self, id_or_uri):
        """
        Gets an IPv4 range by ID or URI.

        Using the allocator and collector associated with the range, IDs may be allocated from or collected back to the
        range.

        Args:
            id_or_uri: Can be either the range ID or URI.

        Returns:
            dict: Range
        """
        return self._client.get(id_or_uri)

    def enable(self, information, id_or_uri, timeout=-1):
        """
        Enables or disables an IPv4 range.

        Args:
            information (dict): Information to update.
            id_or_uri: ID or URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated IPv4 range.
        """

        uri = self._client.build_uri(id_or_uri)

        return self._client.update(information, uri, timeout=timeout)

    def update(self, information, timeout=-1):
        """
        Edit an IPv4 Range.

        Args:
            information (dict): Information to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated IPv4 range.
        """

        return self._client.update(information, timeout=timeout)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes an IPv4 range.

        Args:
            resource (dict):
                Object to delete
            force (bool):
                If set to true, the operation completes despite any problems with
                network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_allocated_fragments(self, id_or_uri, count=-1, start=0):
        """
        Gets all fragments that have been allocated in range.

        Args:
            id_or_uri:
                ID or URI of range.
            count:
                 The number of resources to return. A count of -1 requests all items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total number
                 of items.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.

        Returns:
            list: A list with the allocated fragements.
        """
        uri = self._client.build_uri(id_or_uri) + "/allocated-fragments?start={0}&count={1}".format(start, count)
        return self._client.get_collection(uri)

    def get_free_fragments(self, id_or_uri, count=-1, start=0):
        """
        Gets all free fragments in an IPv4 range.

        Args:
            id_or_uri:
                ID or URI of range.
            count:
                 The number of resources to return. A count of -1 requests all items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total number
                 of items.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.

        Returns:
            list: A list with the free fragments.
        """
        uri = self._client.build_uri(id_or_uri) + "/free-fragments?start={0}&count={1}".format(start, count)
        return self._client.get_collection(uri)
