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


class HypervisorClusterProfiles(Resource):
    """
    The cluster profile resource manager REST APIs to create, retrieve, modify and delete hypervisor cluster profiles.
    """
    URI = '/rest/hypervisor-cluster-profiles'
    DEFAULT_VALUES = {
        '2200': {'type': 'HypervisorClusterProfileV4'}
    }

    def __init__(self, connection, data=None):
        super(HypervisorClusterProfiles, self).__init__(connection, data)
        self.__default_values = {
            'type': 'HypervisorClusterProfileV3'
        }

    def get_all(self, start=0, count=-1, filter='', sort='', query='', scope_uris=''):
        """
        Gets a list of hypervisor cluster profiles based on optional sorting and filtering,
        and constrained by start and count parameters.

        The maximum number of profiles is restricted to 100, i.e.,
        if user requests more than 100, this will be internally limited to 100.

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

        Return:
             list: List of Hypervisor cluster profiles
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort, query=query, scope_uris=scope_uris)

    def create_virtual_switch_layout(self, data=None, timeout=-1):
        """Generates vSwitch layout using information specified in the request body.

        Args:
            data: Fields passed to create the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Return:
            Created virtual switch layout.
        """
        if not data:
            data = {}

        vswitch_uri = "{}/virtualswitch-layout".format(self.URI)
        return self._helper.create(data, vswitch_uri, timeout)

    def get_compliance_preview(self):
        """
        Gets the preview of manual and automatic updates required to make the cluster profile consistent with its template.

        Return:
            cluster profile compliance preview
        """
        compliance_uri = "{0}/compliance-preview".format(self.data["uri"])
        return self._helper.do_get(compliance_uri)

    def delete(self, timeout=-1, soft_delete=False, force=False):
        """
        Deletes a hypervisor cluster profile object from the appliance based on Hypervisor Cluster Profile UUID

        Args:
            force:
                If set to true, the operation completes despite any probles with network
                connectivity or errors on the resource itself. Default is false.
            soft_delete:
                If set to true, the hypervisor cluster profile and its hypervisor profiles
                are removed from appliance only. If set to false, the associated cluster and
                hosts are also removed in the hypervisor manager.

        Return:
            Boolean value. True for success and False for failure.
        """
        uri = "{}?softDelete={}".format(self.data['uri'], soft_delete)

        if force:
            uri += '&force=True'

        return self._helper.delete(uri, timeout=timeout)
