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


class DriveEnclosures(object):
    """
    Drive Enclosures API client.

    Note:
        This resource is only available on HPE Synergy

    """
    URI = '/rest/drive-enclosures'
    PORT_MAP_PATH = "/port-map"
    REFRESH_STATE_PATH = "/refreshState"

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets information about all drive enclosures. Filtering and sorting are supported with the retrieval of
        managed storage systems. The following storage system attributes can be used with filtering and sorting
        operation: name, model, serialNumber, firmware, status, managedDomain, and state.

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
            list: A list of all drive enclosures.
        """
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets the specified drive enclosure resource by ID or by URI.

        Args:
            id_or_uri: Can be either the drive enclosure ID or the drive enclosure URI.

        Returns:
            dict: The drive enclosure.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def get_by(self, field, value):
        """
        Gets all drive enclosures that match the filter.

        The search is case-insensitive.

        Args:
            Field: field name to filter.
            Value: value to filter.

        Returns:
            list: A list of drive enclosures.
        """
        return self._client.get_by(field=field, value=value)

    def get_port_map(self, id_or_uri):
        """
        Use to get the drive enclosure I/O adapter port to SAS interconnect port connectivity.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Returns:
            dict: Drive Enclosure Port Map
        """
        uri = self._client.build_uri(id_or_uri) + self.PORT_MAP_PATH
        return self._client.get(id_or_uri=uri)

    def refresh_state(self, id_or_uri, configuration, timeout=-1):
        """
        Refreshes a drive enclosure.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            configuration: Configuration
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Drive Enclosure
        """
        uri = self._client.build_uri(id_or_uri) + self.REFRESH_STATE_PATH
        return self._client.update(resource=configuration, uri=uri, timeout=timeout)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Performs a specific patch operation for the given drive enclosure. If the server supports the particular
        operation, the operation is performed and a response is returned to the caller with the results.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Drive Enclosure.
        """
        return self._client.patch(id_or_uri=id_or_uri, operation=operation, path=path, value=value, timeout=timeout)
