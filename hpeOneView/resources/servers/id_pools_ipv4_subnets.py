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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import Resource


class IdPoolsIpv4Subnets(Resource):
    """
    The ID pools IPv4 subnets resource provides a Client API for managing IPv4 subnets.
    """

    URI = '/rest/id-pools/ipv4/subnets'

    def __init__(self, connection, data=None):
        super(IdPoolsIpv4Subnets, self).__init__(connection, data)
        self.__default_values = {'type': 'Subnet'}

    def allocate(self, information, subnet_id, timeout=-1):
        """
        Allocates a set of IDs from range.
        The allocator returned contains the list of IDs successfully allocated.
        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            subnet_id:
                IPv4 subnet id.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._helper.build_uri(subnet_id) + '/allocator'
        return self._helper.update(information, uri, timeout=timeout)

    def collect(self, information, subnet_id, timeout=-1):
        """
        Collects one or more IDs to be returned to a pool.
        Args:
            information (dict):
                The list of IDs to be collected
            subnet_id:
                IPv4 subnet id
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """
        uri = self._helper.build_uri(subnet_id) + '/collector'
        return self._helper.update(information, uri, timeout=timeout)
