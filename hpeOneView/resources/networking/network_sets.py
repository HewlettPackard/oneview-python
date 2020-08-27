# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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

from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class NetworkSets(Resource, ResourcePatchMixin):
    """
    Network Sets API client.

    """
    URI = '/rest/network-sets'

    DEFAULT_VALUES = {
        '200': {"type": "network-set"},
        '300': {"type": "network-setV300"},
        '500': {"type": "network-setV300"},
        '600': {"type": "network-setV4"},
        '800': {"type": "network-setV4"},
        '1000': {"type": "network-setV4"},
        '1200': {"type": "network-setV5"},
        '1600': {"type": "network-setV5"},
        '1800': {"type": "network-setV5"}
    }

    def __init__(self, connection, data=None):
        super(NetworkSets, self).__init__(connection, data)

    def get_all_without_ethernet(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of network sets without ethernet. The collection is based
        on optional sorting and filtering and is constrained by start and count parameters.

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
            list: List of network sets, excluding Ethernet networks.
        """
        without_ethernet_client = ResourceHelper("/rest/network-sets/withoutEthernet",
                                                 self._connection,
                                                 self._task_monitor)

        return without_ethernet_client.get_all(start, count, filter=filter, sort=sort)

    def get_without_ethernet(self):
        """
        Gets the network set with the specified ID or URI without ethernet.

        Returns:
            dict: Network set excluding Ethernet networks.
         uri = "{}/script".format(self.data['uri'])
        return self._helper.do_get(uri)
        """
        uri = "{}/withoutEthernet".format(self.data['uri'])
        return self._helper.do_get(uri)
