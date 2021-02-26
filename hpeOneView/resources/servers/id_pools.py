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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import Resource, ResourceSchemaMixin


class IdPools(Resource, ResourceSchemaMixin):
    """
    Class for Id Pools API client.
    """
    URI = '/rest/id-pools'

    def __init__(self, connection, data=None):
        super(IdPools, self).__init__(connection, data)

    def schema(self):
        """
        Gets schema of ID pools and returns it

        Args:
            uri:
                URI of range.
        Returns:
            dict: A dict containing the schema.
        """
        return self._helper.do_get(self.URI + "/schema")

    def get_pool_type(self, uri):
        """
        Gets a pool along with the list of ranges present in it

        Args:
          uri: URI of range

        Returns:
          dict: List of ranges
        """
        uri = self._helper.build_uri(uri)
        return self._helper.do_get(uri)

    def update_pool_type(self, data, uri, timeout=-1):
        """
        Enables or disables the pool

        Args:
            uri: URI of range.

        Returns:
            dict: Updated Resource.
        """
        uri = self._helper.build_uri(uri)
        print(uri)
        return self._helper.update(data, uri, timeout=timeout)

    def validate_id_pool(self, uri, ids_pools):
        """
        Validates an ID pool.

        Args:
            uri:
                URI of range.
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(uri) + "/validate?idList=" + "&idList=".join(ids_pools)
        return self._helper.do_get(uri)

    def validate(self, information, uri, timeout=-1):
        """
        Validates a set of user specified IDs to reserve in the pool.

        This API can be used to check if the specified IDs can be allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            uri:
                URI of vSN range.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(uri) + "/validate"
        return self._helper.update(information, uri, timeout=timeout)

    def allocate(self, information, uri, timeout=-1):
        """
        Allocates a set of IDs from range.

        The allocator returned contains the list of IDs successfully allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            uri:
                URI of vSN range.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(uri) + "/allocator"

        return self._helper.update(information, uri, timeout=timeout)

    def collect(self, information, uri, timeout=-1):
        """
        Collects one or more IDs to be returned to a pool.

        Args:
            information (dict):
                The list of IDs to be collected
            uri:
                URI of range
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """
        uri = self._helper.build_uri(uri) + "/collector"

        return self._helper.update(information, uri, timeout=timeout)

    def get_check_range_availability(self, uri, ids_pools):
        """
        Checks the range availability in the ID pool.

        Args:
            uri:
                URI of range.
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(uri) + "/checkrangeavailability?idList=" + "&idList=".join(ids_pools)
        return self._helper.do_get(uri)

    def generate(self, uri):
        """
        Generates and returns a random range.

        Args:
            uri:
                URI of range.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(uri) + "/generate"
        return self._helper.do_get(uri)
