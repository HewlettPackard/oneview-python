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


class Restores(object):
    """
    Restore API client for initiate a restore of an appliance and to get the status of the restore operation.
    """
    URI = '/rest/restores'

    DEFAULT_VALUES = {
        '200': {"type": "RESTORE"},
        '300': {"type": "RESTORE"}
    }

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get_all(self):
        """
        Retrieve the status of any current appliance restore.

        Returns:
            list: A collection of restore status, but there will be at most one restore status. The status for
            the last restore will be returned if there has been a restore.
        """
        return self._client.get_all()

    def get(self, id_or_uri):
        """
        Retrieves the status of the specified restore operation.

        Args:
            id_or_uri: ID or URI of the Restore.

        Returns:
            dict: Restore
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all Restores that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Restores.
        """
        return self._client.get_by(field, value)

    def get_failure(self):
        """
        Retrieves the result of an appliance restore operation after it has completed.

        The restore result remains valid until a user logs in. After a user logs in, the restore result will be reset.
        This rest request will return only the valid result after restore has completed and before a user logs in.


        Returns:
            dict: Restore Result
        """
        uri = self.URI + '/failure'
        return self._client.get(uri)

    def restore(self, resource, timeout=-1):
        """
        Starts a restore operation with the specified backup file. The backup must be uploaded to the appliance
        prior to running this command. Only one restore can run at a time.

        Args:
            resource (dict): Config to restore.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Restore.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)
