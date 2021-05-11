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


from hpeOneView.resources.resource import Resource, ensure_resource_client


class EnclosureGroups(Resource):
    """
    Enclosure Groups API client.

    """
    URI = '/rest/enclosure-groups'

    def __init__(self, connection, data=None):
        super(EnclosureGroups, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a list of enclosure groups.

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
            list: A list of enclosure groups.
        """
        return self._helper.get_all(start, count, filter=filter,
                                    sort=sort, scope_uris=scope_uris)

    @ensure_resource_client
    def get_script(self):
        """
        Gets the configuration script of the enclosure-group resource with the specified URI.

        Returns:
            dict: Configuration script.
        """

        uri = "{}/script".format(self.data['uri'])

        return self._helper.do_get(uri)

    def update_script(self, script_body):
        """
        Updates the configuration script of the enclosure-group with the specified URI.

        Args:
            id_or_uri: Resource id or resource uri.
            script_body:  Configuration script.

        Returns:
            dict: Updated enclosure group.
        """
        uri = "{}/script".format(self.data['uri'])

        return self._helper.update(script_body, uri=uri)
