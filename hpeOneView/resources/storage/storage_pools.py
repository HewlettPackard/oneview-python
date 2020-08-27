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


from hpeOneView.resources.resource import Resource


class StoragePools(Resource):
    """
    Storage Pools API client.

    """
    URI = '/rest/storage-pools'

    def __init__(self, connection, data=None):
        super(StoragePools, self).__init__(connection, data)

    def add(self, resource, timeout=-1):
        """
        Adds storage pool for management by the appliance.

        Args:
            resource (dict):
                Object to create
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created storage pool.

        """
        return self.create(resource, timeout=timeout)

    def remove(self, force=False, timeout=-1):
        """
        Removes an imported storage pool from OneView.

        Args:
            resource (dict):
                Object to remove.
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Details of associated resource.

        """
        return self.delete(force=force, timeout=timeout)

    def get_reachable_storage_pools(self, start=0, count=-1, filter='', query='', sort='',
                                    networks=None, scope_exclusions=None, scope_uris=''):
        """
        Gets the storage pools that are connected on the specified networks
        based on the storage system port's expected network connectivity.

        Args:
            start: The first item to return, using 0-based indexing. If not specified,
                the default is 0 - start with the first available item.
            count: The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter: A general filter/query string to narrow the list of items returned.
                The default is no filter - all resources are returned.
            sort: The sort order of the returned data set. By default, the sort order
                is based on create time with the oldest entry first.
            query: A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            networks: Specifies the comma-separated list of network URIs used by the
                reachable storage pools.
            scope_exclusions: Specifies the comma-separated list of storage-pools URIs
                that will be excluded from the scope validation checks.
            scope_uris: Specifies the comma-separated list of scope URIs used by the
                reachable storage pools.

        Returns:
            list: Reachable Storage Pools List.
        """
        uri = self.URI + "/reachable-storage-pools"

        if networks:
            elements = "\'"
            for n in networks:
                elements += n + ','
            elements = elements[:-1] + "\'"
            uri = uri + "?networks=" + elements

        if scope_exclusions:
            storage_pools_uris = ",".join(scope_exclusions)
            uri = uri + "?" if "?" not in uri else uri + "&"
            uri += "scopeExclusions={}".format(storage_pools_uris)

        return self._helper.do_get(self._helper.build_query_uri(start=start, count=count, filter=filter, query=query,
                                                                sort=sort, uri=uri, scope_uris=scope_uris))
