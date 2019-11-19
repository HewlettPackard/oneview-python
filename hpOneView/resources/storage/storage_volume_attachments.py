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


from hpOneView.resources.resource import ResourceClient


class StorageVolumeAttachments(object):
    """
    Storage Volume Attachments API client.

    """

    URI = '/rest/storage-volume-attachments'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of volume attachment resources.

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
            list: Volume attachment resources.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

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
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort, uri=uri)

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
        return self._client.create(resource, uri=uri, timeout=timeout, custom_headers=custom_headers)

    def get_paths(self, id_or_uri, path_id_or_uri=''):
        """
        Gets all paths or a specific attachment path for the specified volume attachment.

        Args:
            id_or_uri: Can be either the volume attachment id or the volume attachment uri.
            path_id_or_uri: Can be either the path id or the path uri.

        Returns:
            dict: Paths.
        """
        if path_id_or_uri:
            uri = self._client.build_uri(path_id_or_uri)
            if "/paths" not in uri:
                uri = self._client.build_uri(
                    id_or_uri) + "/paths" + "/" + path_id_or_uri

        else:
            uri = self._client.build_uri(id_or_uri) + "/paths"

        return self._client.get(uri)

    def get(self, id_or_uri):
        """
        Gets a volume attachment by ID or URI.

        Args:
            id_or_uri: Can be either the volume attachment ID or the volume attachment URI.

        Returns:
            dict: volume attachment
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all storage systems that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: List of volume attachments.
        """
        return self._client.get_by(field, value)
