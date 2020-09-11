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


class InterconnectLinkTopologies(object):
    """
    Interconnect Link Topologies API client.

    Note:
        This resource is only available on HPE Synergy.

    """

    URI = '/rest/interconnect-link-topologies'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of all the interconnect link topologies based on the specified parameters.

        Filters can be used in the URL to control the number of interconnect link topologies that are returned.
        With no filters specified, the API returns all interconnect link toplogies.

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
            list: A list of interconnect link topologies.

        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets an interconnect link topology by ID or by URI.

        Args:
            id_or_uri: Can be either the interconnect type id or the interconnect type uri.

        Returns:
            dict: The interconnect link topology.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all interconnect link topologies that match the filter.
        The search is case-insensitive

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of interconnect link topologies.
        """
        return self._client.get_by(field, value)
