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

from hpOneView.resources.resource import ResourceClient


class HypervisorManagers(object):
    URI = '/rest/hypervisor-managers'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', fields='', query='', sort='', view='', scope_uris=''):
        """
        Gets a list of Hypervisor Managers based on optional sorting and filtering, and constrained by start and count
        parameters.

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
            fields:
                Specifies which fields should be returned in the result set.
            query:
                 A general query string to narrow the list of resources returned. The default
                 is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            view:
                Return a specific subset of the attributes of the resource or collection, by
                specifying the name of a predefined view. The default view is expand - show all
                attributes of the resource and all elements of collections of resources.
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.

        Returns:
             list: Hypervisor Managers
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, query=query, fields=fields, view=view, scope_uris=scope_uris)

    def get(self, id_or_uri):
        """
        Get the details of the particular Hypervisor Manager based on its URI or ID.

        Args:
            id_or_uri:
                Can be either the Hypervisor Manager ID or the URI

        Returns:
            dict: Hypervisor Manager
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all hypervisor managers that match the filter
        The search is case-insensitive

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            dict: hypervisor managers
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets the Hypervisor Manager by name.

        Args:
            name: Name of the Hypervisor Manager

        Returns:
            dict: Hypervisor Manager
        """
        return self._client.get_by_name(name)

    def add(self, resource, timeout=-1):
        """
        Adds a Hypervisor Manager using the information provided in the request body.

        Args:
            resource (dict):
                Hypervisor Manager resource.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: The added resource.
        """
        return self._client.create(resource, timeout=timeout)

    def update(self, resource, force=False, timeout=-1):
        """
        Updates the Hypervisor Manager resource. The properties that are omitted (not included as part
        of the request body) are ignored.

        Args:
            resource (dict): Object to update.
            force:
                If set to true, the operation completes despite any problems with network connectivity or errors on
                the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            Updated resource.
        """
        return self._client.update(resource, timeout=timeout, force=force)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a Hypervisor Manager object based on its UUID or URI.

        Args:
            resource (dict):
                Object to delete.
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the hypervisor was successfully deleted.
        """

        return self._client.delete(resource, force=force, timeout=timeout)

