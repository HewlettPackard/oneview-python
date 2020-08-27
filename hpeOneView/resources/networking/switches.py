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
from hpeOneView.resources.resource import merge_default_values


class Switches(object):
    """
    Switches API client.

    Note:
        This resource is only available on C7000 enclosures.

    """
    URI = '/rest/switches'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_statistics(self, id_or_uri, port_name=''):
        """
        Gets statistics for a switch.

        Args:
            id_or_uri: Can be either the switch id or the switch uri.
            port_name: switch port number (optional)

        Returns:
            dict
        """
        uri = self._client.build_uri(id_or_uri) + "/statistics"

        if port_name:
            uri += "/" + port_name

        return self._client.get(uri)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of top of rack switches.

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
            list: A list of rack switches.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a switch by ID or by URI.

        Args:
            id_or_uri: Can be either the switch ID or URI.

        Returns:
            dict: Switch
        """
        return self._client.get(id_or_uri)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a migrated switch.

        Args:
            resource (dict): Object to delete.
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

    def get_environmental_configuration(self, id_or_uri):
        """
        Gets the environmental configuration for a switch.

        Args:
            id_or_uri: Can be either the resource ID or URI.

        Returns:
            dict: environmental configuration
        """
        uri = self._client.build_uri(id_or_uri) + "/environmentalConfiguration"
        return self._client.get(uri)

    def get_by(self, field, value):
        """
        Gets all switches that match the filter.

        The search is case-insensitive.

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of rack switches.
        """
        return self._client.get_by(field, value)

    def update_ports(self, ports, id_or_uri):
        """
        Updates the switch ports. Only the ports under the management of OneView and those that are unlinked are
        supported for update.

        Note:
            This method is available for API version 300 or later.

        Args:
            ports: List of Switch Ports.
            id_or_uri: Can be either the switch id or the switch uri.

        Returns:
            dict: Switch
        """
        ports = merge_default_values(ports, {'type': 'port'})

        uri = self._client.build_uri(id_or_uri) + "/update-ports"
        return self._client.update(uri=uri, resource=ports)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update a resource for a given logical switch.

        Only one operation can be performed in each PATCH call.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout)
