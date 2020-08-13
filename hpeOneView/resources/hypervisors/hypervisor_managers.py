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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library

standard_library.install_aliases()


from hpeOneView.resources.resource import Resource


class HypervisorManagers(Resource):
    """
    Hypervisor Managers API client.

    """
    URI = '/rest/hypervisor-managers'

    def __init__(self, connection, data=None):
        super(HypervisorManagers, self).__init__(connection, data)
        self.__default_values = {
            'type': 'HypervisorManagerV2'
        }

    def get_all(self, start=0, count=-1, filter='', sort='', query='', scope_uris=''):
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
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            query:
                 A general query string to narrow the list of resources returned. The default
                 is no query - all resources are returned.
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.

        Returns:
             list: List of Hypervisor Managers
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort, query=query, scope_uris=scope_uris)
