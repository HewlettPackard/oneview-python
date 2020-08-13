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


from hpeOneView.resources.resource import ResourceClient


class LogicalDownlinks(object):
    """
    Logical Downlinks API client.

    """
    URI = '/rest/logical-downlinks'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of logical downlinks. The collection is based on
        optional sorting and filtering and is constrained by start and count parameters.

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
            list: A list of logical downlinks.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a logical downlink by ID or by URI.

        Args:
            id_or_uri: Can be either the logical downlink id or the logical downlink uri.

        Returns:
            dict: The logical downlink.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all logical downlinks that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of logical downlinks.
        """
        return self._client.get_by(field, value)

    def get_all_without_ethernet(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of logical downlinks without ethernet. The collection is
        based on optional sorting and filtering and is constrained by start and count parameters.

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
            dict
        """
        without_ethernet_client = ResourceClient(
            self._connection, "/rest/logical-downlinks/withoutEthernet")
        return without_ethernet_client.get_all(start, count, filter=filter, sort=sort)

    def get_without_ethernet(self, id_or_uri):
        """
        Gets the logical downlink with the specified ID without ethernet.

        Args:
            id_or_uri: Can be either the logical downlink id or the logical downlink uri.

        Returns:
            dict
        """
        uri = self._client.build_uri(id_or_uri) + "/withoutEthernet"
        return self._client.get(uri)
