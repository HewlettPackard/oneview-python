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


class Labels(object):
    """
    Labels API client.

    """

    URI = '/rest/labels'
    RESOURCES_PATH = '/resources'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of labels based on optional sorting and filtering and is constrained by start
        and count parameters.

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
            list: A list of labels.
        """
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a label by ID or URI.

        Args:
            id_or_uri: Can be either the label ID or the label URI.

        Returns:
            dict: The label.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def get_by_resource(self, resource_uri):
        """
        Gets all the labels for the specified resource

        Args:
            resource_uri: The resource URI

        Returns:
            dict: Resource Labels
        """
        uri = self.URI + self.RESOURCES_PATH + '/' + resource_uri
        return self._client.get(id_or_uri=uri)

    def create(self, resource):
        """
        Set all the labels for a resource.

        Args:
            resource: The object containing the resource URI and a list of labels

        Returns:
            dict: Resource Labels
        """
        uri = self.URI + self.RESOURCES_PATH
        return self._client.create(resource=resource, uri=uri)

    def update(self, resource):
        """
        Set all the labels for a resource.

        Args:
            resource (dict): Object to update.

        Returns:
            dict: Resource Labels
        """
        return self._client.update(resource=resource)

    def delete(self, resource, timeout=-1):
        """
        Delete all the labels for a resource.

        Args:
            resource (dict): Object to delete.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.
        """
        self._client.delete(resource=resource, timeout=timeout)
