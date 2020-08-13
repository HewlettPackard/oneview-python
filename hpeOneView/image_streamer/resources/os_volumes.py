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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpeOneView.resources.resource import ResourceClient, extract_id_from_uri


class OsVolumes(object):
    URI = '/rest/os-volumes'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {
            'type': 'OeVolume',
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of the OS Volume based on optional sorting and filtering, and constrained by start and count
        parameters.

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
            list: A list of OS Volume.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Retrieves the overview details of the selected OS Volume as per the selected attributes.

        Args:
            id_or_uri: ID or URI of the OS Volume.

        Returns:
            dict: The OS Volume.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all OS Volume that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of OS Volume.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets an OS Volume by name.

        Args:
            name: Name of the OS Volume.

        Returns:
            dict: The OS Volume.
        """
        return self._client.get_by_name(name)

    def download_archive(self, name, file_path):
        """
        Download archived logs of the OS Volume.

        Args:
            name: Name of the OS Volume.
            file_path (str): Destination file path.

        Returns:
            bool: Indicates if the resource was successfully downloaded.
        """
        uri = self.URI + "/archive/" + name
        return self._client.download(uri, file_path)

    def get_storage(self, id_or_uri):
        """
        Get storage details of an OS Volume.

        Args:
            id_or_uri: ID or URI of the OS Volume.

        Returns:
            dict: Storage details
        """
        uri = self.URI + "/{}/storage".format(extract_id_from_uri(id_or_uri))
        return self._client.get(uri)
