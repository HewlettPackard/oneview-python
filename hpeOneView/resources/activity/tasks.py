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
import json

standard_library.install_aliases()


from hpeOneView.resources.resource import Resource, ResourcePatchMixin
from hpeOneView.exceptions import HPEOneViewException


class Tasks(ResourcePatchMixin, Resource):
    """
    Tasks API client.

    """
    URI = '/rest/tasks'

    def __init__(self, connection, data=None):
        super(Tasks, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, fields='', filter='', query='', sort='', view='', topCount=0, childLimit=0):
        """
        Gets all the tasks based upon filters provided.

        Note:
            Filters are optional.

        Args:
            start:
                 The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                 first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items.
            fields:
                 Specifies which fields should be returned in the result set.
            filter (list or str):
                 A general filter/query string to narrow the list of items returned. The default is no filter; all
                 resources are returned.
            query:
                 A general query string to narrow the list of resources returned. The default is no query (all
                 resources are returned).
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time, with the
                oldest entry first.
            view:
                 Returns a specific subset of the attributes of the resource or collection, by specifying the name of a
                 predefined view. The default view is expand (show all attributes of the resource and all elements of
                 collections of resources).
            childLimit:
                 Total number of associated resources in an aggregated manner. Default value is 10.
            topCount:
                 Total number of immediate children the task should send back. Otherwise, the task sends back the
                 aggregated view of the tree. Default value is 3.

        Returns:
            list: A list of tasks.
        """
        return self._helper.get_all(start=start, count=count, filter=filter, query=query, sort=sort, view=view,
                                    fields=fields, childLimit=childLimit, topCount=topCount)

    def patch(self, uri, timeout=-1):
        """
        Sets the state of task to cancelling only if IsCancellable is set to true for the task and its children or
        children are in terminal state.

        Args:
            uri: URI of task resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        resp, body = self._connection.do_http('PATCH', path=uri, body=None)

        if resp.status >= 400:
            raise HPEOneViewException(body)
        elif resp.status == 304:
            if body and not isinstance(body, dict):
                try:
                    body = json.loads(body)
                except Exception:
                    pass
        elif resp.status == 202:
            task = self._connection.__get_task_from_response(resp, body)
            return self._task_monitor.wait_for_task(task, timeout)

        return body
