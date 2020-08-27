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


class StorageVolumeAttachments(Resource):
    """
    Storage Volume Attachments API client.

    """

    URI = '/rest/storage-volume-attachments'

    def __init__(self, connection, data=None):
        super(StorageVolumeAttachments, self).__init__(connection, data)

    def get_extra_unmanaged_storage_volumes(self, start=0, count=-1, filter='', sort=''):
        """
        Gets the list of extra unmanaged storage volumes.

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
            list: Extra unmanaged storage volumes.
        """
        uri = self.URI + "/repair?alertFixType=ExtraUnmanagedStorageVolumes"
        return self._helper.get_all(start=start, count=count, filter=filter, sort=sort, uri=uri)

    def remove_extra_presentations(self, resource, timeout=-1):
        """
        Removes extra presentations from a specified server profile.

        Args:
            resource (dict):
                Object to create
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            dict: Associated storage attachment resource.
        """
        uri = self.URI + "/repair"
        custom_headers = {'Accept-Language': 'en_US'}
        return self._helper.create(resource, uri=uri, timeout=timeout, custom_headers=custom_headers)

    def get_paths(self, path_id=''):
        """
        Gets all paths or a specific attachment path for the specified volume attachment.

        Args:
            path_id: path id

        Returns:
            dict: Paths.
        """
        if path_id:
            uri = "{}/paths/{}".format(self.data["uri"], path_id)
        else:
            uri = "{}/paths".format(self.data["uri"])

        return self._helper.do_get(uri)
