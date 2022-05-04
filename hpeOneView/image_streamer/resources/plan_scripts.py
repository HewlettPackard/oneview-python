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


from hpeOneView.resources.resource import ResourceClient, extract_id_from_uri


class PlanScripts(object):
    URI = '/rest/plan-scripts'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {
            'type': 'PlanScript',
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of Plan Scripts based on optional sorting and filtering, and constrained by start and count
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
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of Plan Scripts.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a Plan Script object from the appliance based on its Plan Script UUID.

        Args:
            resource: dict object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get(self, id_or_uri):
        """
        Retrieves the overview details of the selected Plan Script as per the selected attributes.

        Args:
            id_or_uri: ID or URI of the Plan Script.

        Returns:
            dict: The Plan Script.
        """
        return self._client.get(id_or_uri)

    def create(self, resource, timeout=-1):
        """
        Adds a Plan Script using the information provided in the request body. The plan type can be one of the
        following types: General, deploy and capture. Note: The OS type for the Plan Script is always assigned
        as "ESXi".

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Created Plan Script.

        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.create(data, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates the properties of the Plan Script.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Updated resource.

        """
        return self._client.update(resource, timeout=timeout)

    def get_by(self, field, value):
        """
        Gets all Plan Scripts that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Plan Scripts.
        """
        return self._client.get_by(field, value)

    def retrieve_differences(self, id_or_uri, content, timeout=-1):
        """
        Retrieves the modified contents of the selected Plan Script according to the provided content object, as per
        the selected attributes.

        Args:
            id_or_uri: ID or URI of the Plan Script.
            content (str): Plan Script content.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Script differences.
        """
        uri = self.URI + "/differences/" + extract_id_from_uri(id_or_uri)
        return self._client.create(content, uri=uri, timeout=timeout)

    def get_usedby_and_readonly(self, id):
        """
        Gets the build plans details os teh selected plan script as per the selected attributes.

        Args:
            id: ID of the Plan Script.

        Returns:
            array of build plans
        """
        uri = self.URI + "/" + id + "/usedby/readonly"
        return self._client.get(uri)
