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


class IdPoolsIpv4Subnets(object):
    """
    The ID pools IPv4 subnets resource provides a Client API for managing IPv4 subnets.
    """

    URI = '/rest/id-pools/ipv4/subnets'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Creates subnet.

        Args:
            resource (dict): Object to create
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created subnet.
        """
        return self._client.create(resource, timeout=timeout)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of IPV4 Subnet resources. Returns a list of resources based on optional sorting and filtering,
        and constrained by start and count parameters.

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
            list: A list of IPV4 Subnet resources.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets an IPv4 subnet.

        Using the allocator and collector associated with the subnet, IDs may be allocated from or collected back to the
        subnet.

        Args:
            id_or_uri: Can be either the subnet ID or URI.

        Returns:
            dict: IPv4 subnet.
        """
        return self._client.get(id_or_uri)

    def update(self, resource, timeout=-1):
        """
        Update the resource.

        Args:
            resource (dict): Information to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """

        return self._client.update(resource, timeout=timeout)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes the IPv4 subnet.

        Args:
            resource (dict):
                Object to delete
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
