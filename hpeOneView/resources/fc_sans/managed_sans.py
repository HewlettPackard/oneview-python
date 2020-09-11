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


from hpeOneView.resources.resource import Resource, ensure_resource_client, unavailable_method


class ManagedSANs(Resource):
    """
    Managed SANs API client.

    """
    URI = '/rest/fc-sans/managed-sans'

    def __init__(self, connection, data=None):
        super(ManagedSANs, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, query='', sort=''):
        """
        Retrieves the list of registered Managed SANs

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items.
            query:
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of Managed SANs
        """
        return self._helper.get_all(start=start, count=count, query=query, sort=sort)

    def get_by_name(self, name):
        """
        Gets a Managed SAN by name.

        Args:
            name: Name of the Managed SAN

        Returns:
            dict: Managed SAN.
        """
        managed_sans = self.get_all()
        result = [x for x in managed_sans if x['name'] == name]

        resource = result[0] if result else None
        if resource:
            resource = self.new(self._connection, resource)

        return resource

    def create(self):
        """Create method is not available"""
        unavailable_method()

    def delete(self):
        """Delete method is not available"""
        unavailable_method()

    @ensure_resource_client
    def get_endpoints(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of endpoints in a SAN.

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
            list: A list of endpoints.
        """
        uri = "{}/endpoints/".format(self.data["uri"])
        return self._helper.get_all(start, count, filter=filter, sort=sort, uri=uri)

    @ensure_resource_client
    def create_endpoints_csv_file(self, timeout=-1):
        """
        Creates an endpoints CSV file for a SAN.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Endpoint CSV File Response.
        """
        uri = "{}/endpoints/".format(self.data["uri"])
        return self._helper.do_post(uri, {}, timeout, None)

    @ensure_resource_client
    def create_issues_report(self, timeout=-1):
        """
        Creates an unexpected zoning report for a SAN.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            list: A list of FCIssueResponse dict.
        """
        uri = "{}/issues/".format(self.data["uri"])
        return self._helper.create_report(uri, timeout)

    def get_wwn(self, wwn):
        """
        Retrieves a list of associations between provided WWNs and the SANs (if any) on which they reside.

        Note:
            This method is available for API version 300 or later.

        Args:
            wwn (str): The WWN that may be associated with the SAN.

        Returns:
            list: Associations between provided WWNs and the SANs
        """
        uri = '/rest/fc-sans/managed-sans?locate=' + wwn
        return self._helper.do_get(uri)
