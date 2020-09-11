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


from hpeOneView.resources.resource import Resource, ResourcePatchMixin, ensure_resource_client


class LogicalEnclosures(ResourcePatchMixin, Resource):
    """
    The logical enclosure resource provides methods for managing one or more enclosures that are
    linked or stacked with stacking links.

    """
    URI = '/rest/logical-enclosures'

    def __init__(self, connection, data=None):
        super(LogicalEnclosures, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Returns a list of logical enclosures matching the specified filter. A maximum of 40 logical enclosures are
        returned to the caller. Additional calls can be made to retrieve any other logical enclosures matching the
        filter. Valid filter parameters include attributes of a Logical Enclosure resource.

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
            list: A list of logical enclosures.
        """
        return self._helper.get_all(start, count, filter=filter,
                                    sort=sort, scope_uris=scope_uris)

    @ensure_resource_client
    def update_configuration(self, timeout=-1):
        """
        Reapplies the appliance's configuration on enclosures for the logical enclosure by ID or URI. This includes
        running the same configure steps that were performed as part of the enclosure add.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical enclosure.
        """
        uri = "{}/configuration".format(self.data["uri"])
        updated_configuration = self._helper.update(None, uri, timeout=timeout)
        self.refresh()

        return updated_configuration

    @ensure_resource_client
    def get_script(self):
        """
        Gets the configuration script of the logical enclosure by ID or URI.

        Return:
            str: Configuration script.
        """
        uri = "{}/script".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def update_script(self, information, timeout=-1):
        """
        Updates the configuration script of the logical enclosure and on all enclosures in the logical enclosure with
        the specified ID.

        Args:
            information: Updated script.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Return:
            Configuration script.
        """
        uri = "{}/script".format(self.data["uri"])
        return self._helper.update(information, uri=uri, timeout=timeout)

    @ensure_resource_client
    def generate_support_dump(self, information, timeout=-1):
        """
        Generates a support dump for the logical enclosure with the specified ID. A logical enclosure support dump
        includes content for logical interconnects associated with that logical enclosure. By default, it also contains
        appliance support dump content.

        Args:
            information (dict): Information to generate support dump.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Support dump.
        """
        uri = "{}/support-dumps".format(self.data["uri"])
        return self._helper.create(information, uri=uri, timeout=timeout)

    @ensure_resource_client
    def update_from_group(self, data=None, timeout=-1):
        """
        Use this action to make a logical enclosure consistent with the enclosure group when the logical enclosure is
        in the Inconsistent state.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical enclosure.
        """
        uri = "{}/updateFromGroup".format(self.data["uri"])
        return self._helper.update(data, uri, timeout=timeout)
