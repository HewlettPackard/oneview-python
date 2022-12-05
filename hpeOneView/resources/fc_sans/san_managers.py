# -*- coding: utf-8 -*-
###
# (C) Copyright [2022] Hewlett Packard Enterprise Development LP
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


class SanManagers(Resource):
    """
    SAN Managers API client.

    """
    URI = '/rest/fc-sans/device-managers'

    def __init__(self, connection, data=None):
        super(SanManagers, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', query=''):
        """
        Retrieves the list of registered SAN Managers.
        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            query:
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of SAN managers.

        """
        return self._helper.get_all(start=start, count=count, filter=filter, sort=sort, query=query,)

    def update(self, resource, id_or_uri):
        """
        Updates a registered Device Manager.

        Args:
            resource (dict): Object to update.
            id_or_uri: Can be either the Device manager ID or URI.

        Returns:
            dict: The device manager resource.
        """

        return self._helper.update(resource=resource, uri=id_or_uri)

    def remove(self, force=False, timeout=-1):
        """
        Removes the  SAN Manager from OneView.

        Args:
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Details of associated resource.
        """
        headers = {'If-Match': '*'}
        return self.delete(force=force, timeout=timeout, custom_headers=headers)

    def get_by_name(self, name):
        """
        Gets a SAN Manager by name.

        Args:
            name: Name of the SAN Manager

        Returns:
            SAN Manager.
        """
        san_managers = self.get_all()
        result = [x for x in san_managers if x['name'] == name]

        return self.new(self._connection, result[0])if result else None
