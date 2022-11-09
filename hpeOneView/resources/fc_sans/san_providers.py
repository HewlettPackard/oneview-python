# -*- coding: utf-8 -*-
###
# (C) Copyright [2022] Hewlett Packard Enterprise Development LP
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


class SanProviders(Resource):
    """
    SAN Managers API client.

    """

    URI = '/rest/fc-sans/providers'

    def __init__(self, connection, data=None):
        super(SanProviders, self).__init__(connection, data)

    def add(self, resource, provider_uri_or_id, timeout=-1):
        """
        Adds a Device Manager under the specified provider.

        Args:
            resource (dict): Object to add.
            provider_uri_or_id: ID or URI of provider.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Added SAN Manager.
        """
        uri = provider_uri_or_id + "/device-managers"

        return self._helper.create(data=resource, uri=uri, timeout=timeout)

    def get_provider_uri(self, provider_display_name):
        """
        Gets uri for a specific provider.

        Args:
            provider_display_name: Display name of the provider.

        Returns:
            uri
        """
        providers = self.get_by_field('displayName', provider_display_name)
        return providers.data['uri'] if providers else None

    def get_default_connection_info(self, provider_name):
        """
        Gets default connection info for a specific provider.

        Args:
            provider_name: Name of the provider.

        Returns:
            dict: Default connection information.
        """
        provider = self.get_by_field('displayName', provider_name)

        if provider:
            return provider.data['defaultConnectionInfo']
        else:
            return {}
