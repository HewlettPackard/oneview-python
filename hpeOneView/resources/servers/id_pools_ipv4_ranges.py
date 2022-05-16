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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import Resource, ResourceSchemaMixin


class IdPoolsIpv4Ranges(Resource, ResourceSchemaMixin):
    """
    The ID pools IPv4 ranges resource provides a Client API for managing IPv4 ranges.
    """
    URI = '/rest/id-pools/ipv4/ranges'

    def __init__(self, connection, data=None):
        super(IdPoolsIpv4Ranges, self).__init__(connection, data)
        self.__default_values = {'type': 'Range'}

    def enable(self, information, uri, timeout=-1):
        """
        Enables or disables an IPv4 range.

        Args:
            information (dict): Information to update.
            uri: URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated IPv4 range.
        """
        return self._helper.update(information, uri, timeout=timeout)

    def update_allocator(self, information, uri, timeout=-1):
        """
        Allocates a set of IDs from an IPv4 range.

        Args:
            information (dict): Information to update.
            id_or_uri: URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The allocator returned contains the list of IDs successfully allocated.
        """
        uri = uri + "/allocator"
        return self._helper.update(information, uri, timeout=timeout)

    def update_collector(self, information, uri, timeout=-1):
        """
        Collects a set of IDs back to an IPv4 range.

        Args:
            information (dict): Information to update.
            id_or_uri: URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The collector returned contains the list of IDs successfully collected.
        """
        uri = uri + "/collector"
        return self._helper.update(information, uri, timeout=timeout)

    def get_allocated_fragments(self, uri, count=-1, start=0):
        """
        Gets all fragments that have been allocated in range.

        Args:
            uri:
                URI of range.
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
        uri = uri + "/allocated-fragments?start={0}&count={1}".format(start, count)
        return self._helper.get_collection(uri)

    def get_free_fragments(self, uri, count=-1, start=0):
        """
        Gets all free fragments in an IPv4 range.

        Args:
            uri:
                URI of range.
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
        uri = uri + "/free-fragments?start={0}&count={1}".format(start, count)
        return self._helper.get_collection(uri)
