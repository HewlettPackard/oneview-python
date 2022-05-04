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
from hpeOneView.resources.search.index_resources import IndexResources

category_list = ['connection-templates', 'drive-enclosures', 'ethernet-networks', 'enclosures', 'enclosure-groups',
                 'fc-networks', 'fcoe-networks', 'firmware-bundles', 'hypervisor-cluster-profiles',
                 'hypervisor-host-profiles', 'hypervisor-managers', 'interconnects', 'logical-enclosures',
                 'logical-interconnect-groups', 'logical-interconnects', 'network-sets', 'os-deployment-plans',
                 'sas-interconnects', 'sas-logical-interconnect-groups', 'sas-logical-interconnects',
                 'sas-logical-jbods', 'scopes', 'server-hardware', 'server-profile-templates', 'server-profiles',
                 'storage-pools', 'storage-volume-sets', 'storage-volume-templates', 'storage-volumes']


def get_resources_associated_with_label(connection, label):
    index_resource = IndexResources(connection)
    query_string = "labels='{}'".format(label)
    all_index_resources = index_resource.get_all(category=category_list, query=query_string)
    response = [dict_response['uri'] for dict_response in all_index_resources]
    return response


class Labels(Resource):
    """
    Labels API client.

    """

    URI = '/rest/labels'
    RESOURCES_PATH = '/resources'

    def __init__(self, connection, data=None):
        super(Labels, self).__init__(connection, data)

    def get_assigned_resources(self, name):
        """
        Retrieves the assigned resource of a label by name.

        Args:
            name: name of the label.

        Returns:
          Dict:  Get assigned resources of specified label resource.
        """
        response = super(Labels, self).get_by_name(name)
        if response:
            resources_list = get_resources_associated_with_label(self._connection, name)
            assigned_resource = dict(name=name, assignedResourceUris=resources_list)
        return assigned_resource

    def create(self, resource, timeout=-1):
        """
        Set all the labels for a resource.

        Args:
            resource: The object containing the resource URI and a list of labels

        Returns:
            dict: Resource Labels
        """
        uri = self.URI + self.RESOURCES_PATH
        return super(Labels, self).create(resource, uri=uri, timeout=timeout)

    def get_by_resource(self, resource_uri):
        """
        Gets all the labels for the specified resource

        Args:
            resource_uri: The resource URI

        Returns:
            dict: Resource Labels
        """
        uri = self.URI + self.RESOURCES_PATH + '/' + resource_uri
        return super(Labels, self).get_by_uri(uri)

    def get_all(self, count=-1, sort='', start=0, view='', fields='', filter='', name_prefix='', category=[]):
        """
        Gets all items according with the given arguments.
        Args:
            start: The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count: The number of resources to return. A count of -1 requests all items (default).
            sort: The sort order of the returned data set. By default, the sort order is based on create time with the
                oldest entry first.
            view:
                Returns a specific subset of the attributes of the resource or collection by specifying the name of a
                predefined view. The default view is expand (show all attributes of the resource and all elements of
                the collections or resources).
            fields:
                Name of the fields.
        Returns:
             list: A list of items matching the specified filter.
        """
        return self._helper.get_all(count=count, sort=sort, start=start, view=view, fields=fields, filter=filter, name_prefix=name_prefix, category=category)
