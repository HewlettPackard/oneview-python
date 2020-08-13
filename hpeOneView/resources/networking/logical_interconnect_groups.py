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


from hpeOneView.resources.resource import Resource, ResourcePatchMixin


class LogicalInterconnectGroups(ResourcePatchMixin, Resource):
    """
    Logical Interconnect Groups API client.

    """
    URI = '/rest/logical-interconnect-groups'

    DEFAULT_VALUES = {
        '200': {"type": "logical-interconnect-groupV3"},
        '300': {"type": "logical-interconnect-groupV300"},
        '500': {"type": "logical-interconnect-groupV300"},
        '600': {"type": "logical-interconnect-groupV4"},
        '800': {"type": "logical-interconnect-groupV5"},
        '1000': {"type": "logical-interconnect-groupV6"},
        '1200': {"type": "logical-interconnect-groupV7"},
        '1400': {"type": "logical-interconnect-groupV8"},
        '1600': {"type": "logical-interconnect-groupV8"},
        '1800': {"type": "logical-interconnect-groupV8"}
    }

    def __init__(self, connection, data=None):
        super(LogicalInterconnectGroups, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a list of logical interconnect groups based on optional sorting and filtering and is constrained by start
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
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.

        Returns:
            list: A list of logical interconnect groups.
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort, scope_uris=scope_uris)

    def get_default_settings(self):
        """
        Gets the default interconnect settings for a logical interconnect group.

        Returns:
            dict: Interconnect Settings.
        """
        uri = self.URI + "/defaultSettings"
        return self._helper.do_get(uri)

    def get_settings(self):
        """
        Gets the interconnect settings for a logical interconnect group.

        Returns:
            dict: Interconnect Settings.
        """
        uri = "{}/settings".format(self.data["uri"])
        return self._helper.do_get(uri)
