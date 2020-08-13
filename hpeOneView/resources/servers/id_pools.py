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


class IdPools(object):
    """
    Class for Id Pools API client.
    """
    URI = '/rest/id-pools'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get(self, id_or_uri):
        """
        Gets a pool.

        Args:
            id_or_uri: Can be either the range ID or URI.

        Returns:
            dict: Pool resource.
        """
        return self._client.get(id_or_uri)

    def enable(self, information, id_or_uri, timeout=-1):
        """
        Enables or disables a pool.

        Args:
            information (dict): Information to update.
            id_or_uri: ID or URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """

        uri = self._client.build_uri(id_or_uri)
        return self._client.update(information, uri, timeout=timeout)

    def validate_id_pool(self, id_or_uri, ids_pools):
        """
        Validates an ID pool.

        Args:
            id_or_uri:
                ID or URI of range.
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/validate?idList=" + "&idList=".join(ids_pools)
        return self._client.get(uri)

    def validate(self, information, id_or_uri, timeout=-1):
        """
        Validates a set of user specified IDs to reserve in the pool.

        This API can be used to check if the specified IDs can be allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            id_or_uri:
                ID or URI of vSN range.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/validate"
        return self._client.update(information, uri, timeout=timeout)

    def allocate(self, information, id_or_uri, timeout=-1):
        """
        Allocates a set of IDs from range.

        The allocator returned contains the list of IDs successfully allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            id_or_uri:
                ID or URI of vSN range.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/allocator"

        return self._client.update(information, uri, timeout=timeout)

    def collect(self, information, id_or_uri, timeout=-1):
        """
        Collects one or more IDs to be returned to a pool.

        Args:
            information (dict):
                The list of IDs to be collected
            id_or_uri:
                ID or URI of range
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """
        uri = self._client.build_uri(id_or_uri) + "/collector"

        return self._client.update(information, uri, timeout=timeout)

    def get_check_range_availability(self, id_or_uri, ids_pools):
        """
        Checks the range availability in the ID pool.

        Args:
            id_or_uri:
                ID or URI of range.
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = self._client.build_uri(id_or_uri) + "/checkrangeavailability?idList=" + "&idList=".join(ids_pools)
        return self._client.get(uri)

    def generate(self, id_or_uri):
        """
        Generates and returns a random range.

        Args:
            id_or_uri:
                ID or URI of range.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/generate"
        return self._client.get(uri)
