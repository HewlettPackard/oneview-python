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
from hpeOneView.resources.search.index_resources import IndexResources


category_list = ['connection-templates', 'ethernet-networks', 'enclosures', 'enclosure-groups',
                 'fc-networks', 'fcoe-networks', 'firmware-bundles', 'hypervisor-cluster-profiles',
                 'hypervisor-managers', 'interconnects', 'logical-enclosures', 'logical-interconnect-groups',
                 'logical-interconnects', 'network-sets', 'os-deployment-plans', 'scopes', 'server-hardware',
                 'server-profile-templates', 'server-profiles', 'storage-pools', 'storage-volume-sets',
                 'storage-volume-templates', 'storage-volumes']


def get_resources_associated_with_scope(connection, scope_uri):
    index_resource = IndexResources(connection)
    query_string = "scopeUris='{}'".format(scope_uri)
    all_index_resources = index_resource.get_all(category=category_list, query=query_string)
    response = [dict_response['uri'] for dict_response in all_index_resources]
    return response


class Scopes(Resource, ResourcePatchMixin):
    """
    Scopes API client.

    Note:
        This resource is available for API version 300 or later.

    """
    URI = '/rest/scopes'

    DEFAULT_VALUES = {
        '300': {"type": "Scope"},
        '500': {"type": "ScopeV2"},
        '800': {"type": "ScopeV3"},
        '1000': {"type": "ScopeV3"},
        '1200': {"type": "ScopeV3"},
        '1600': {"type": "ScopeV3"},
        '1800': {"type": "ScopeV3"}
    }

    def __init__(self, connection, data=None):
        super(Scopes, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', query='', view=''):
        """
         Gets a list of scopes.

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
            view:
                 Returns a specific subset of the attributes of the resource or collection, by
                 specifying the name of a predefined view. The default view is expand (show all
                 attributes of the resource and all elements of collections of resources).

        Returns:
            list: A list of scopes.
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort, query=query, view=view)

    def get_by_uri(self, uri):
        """
        Retrieves the specified scope resource by uri.

        Args:
            uri: Uri of specified scope resource

        Return:
            dict: Get response of specified scope resource.
        """
        response = super(Scopes, self).get_by_uri(uri)
        if response:
            resource_list = get_resources_associated_with_scope(self._connection, response.data['uri'])
            response.data['addedResourceUris'] = resource_list
        return response

    def get_by_name(self, name):
        """
        Retrieves the specified scope resource by name.

        Args:
            name: name of specified scope resource

        Return:
            dict: Get response of specified scope resource.
        """
        response = super(Scopes, self).get_by_name(name)
        if response:
            resource_list = get_resources_associated_with_scope(self._connection, response.data['uri'])
            response.data['addedResourceUris'] = resource_list
        return response

    def update(self, resource, timeout=-1):
        """
        Updates a scope.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated scope.

        """
        headers = {'If-Match': resource.get('eTag', '*')}
        return super(Scopes, self).update(resource, timeout=timeout, custom_headers=headers)

    def delete(self, timeout=-1):
        """
        Deletes a Scope.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        headers = {'If-Match': '*'}
        return super(Scopes, self).delete(timeout=timeout, custom_headers=headers)

    def get_scope_resource(self, resource_uri):
        """
        Gets a resource's scope, containing a list of the scopes to which the resource is assigned.

        Args:
            resource_uri: Uri of the resource

        Return:
            dict: Gets the scope assignments for a specified resource.
        """
        uri = "{0}/resources{1}".format(self.URI, resource_uri)
        return super(Scopes, self).get_by_uri(uri)

    # This function will work till API version 300
    def update_resource_assignments(self, id_or_uri, resource_assignments, timeout=-1):
        """
        Modifies scope membership by adding or removing resource assignments.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            resource_assignments (dict):
                A dict object with a list of resource URIs to be added and a list of resource URIs to be removed.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        uri = self._helper.build_uri(id_or_uri) + "/resource-assignments"
        return super(Scopes, self).patch_request(uri, resource_assignments, timeout=timeout)
