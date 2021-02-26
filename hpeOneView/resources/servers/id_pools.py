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

    def get_pool_type(self, pool_type):
        """
        Gets a pool along with the list of ranges present in it

        Args:
          pool_type: Id pool type

        Returns:
          dict: List of ranges
        """
        uri = self._helper.build_uri(pool_type)
        return super(IdPools, self).get_by_uri(uri)

    def update_pool_type(self, data, pool_type, timeout=-1):
        """
        Enables or disables the pool

        Args:
          data: List of ID ranges
          pool_type: Id pool type

        Returns:
            dict: Updated Resource.
        """
        uri = self._helper.build_uri(pool_type)
        return self._helper.update(data, uri, timeout=timeout)

    def validate_id_pool(self, pool_type, ids_pools):
        """
        Validates an ID pool.

        Args:
            pool_type: Id pool type

            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(pool_type) + "/validate?idList=" + "&idList=".join(ids_pools)
        return super(IdPools, self).get_by_uri(uri)

    def validate(self, information, pool_type, timeout=-1):
        """
        Validates a set of user specified IDs to reserve in the pool.

        This API can be used to check if the specified IDs can be allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.

            pool_type: Id pool type

            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(pool_type) + "/validate"
        return self._helper.update(information, uri, timeout=timeout)

    def allocate(self, information, pool_type, timeout=-1):
        """
        Allocates a set of IDs from range.

        The allocator returned contains the list of IDs successfully allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.

            pool_type: Id pool type

            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(pool_type) + "/allocator"

        return self._helper.update(information, uri, timeout=timeout)

    def collect(self, information, pool_type, timeout=-1):
        """
        Collects one or more IDs to be returned to a pool.

        Args:
            information (dict):
                The list of IDs to be collected

            pool_type: Id pool type

            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """
        uri = self._helper.build_uri(pool_type) + "/collector"

        return self._helper.update(information, uri, timeout=timeout)

    def get_check_range_availability(self, pool_type, ids_pools):
        """
        Checks the range availability in the ID pool.

        Args:
            pool_type: Id pool type

            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(pool_type) + "/checkrangeavailability?idList=" + "&idList=".join(ids_pools)
        return super(IdPools, self).get_by_uri(uri)

    def generate(self, pool_type):
        """
        Generates and returns a random range.

        Args:
            pool_type: Id pool type

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(pool_type) + "/generate"
        return super(IdPools, self).get_by_uri(uri)
