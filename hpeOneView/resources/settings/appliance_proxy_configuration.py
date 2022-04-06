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

from hpeOneView.resources.resource import Resource, ResourceHelper


class ApplianceProxyConfiguration(Resource, ResourceHelper):
    """
    ApplianceProxyConfig API Client.

    """
    URI = '/rest/appliance/proxy-config'

    def __init__(self, connection, data=None):
        super(ApplianceProxyConfiguration, self).__init__(connection, data)

    def get_all(self):
        return super(ApplianceProxyConfiguration, self).get_by_uri(self.URI)

    def get_by_proxy(self, proxy_ip):
        """Retrieves a resource by proxy server ip.

        Args:
            proxy_ip: Ip address of the proxy

        Returns:
            Resource object or None if resource does not exist.
        """
        results = self.get_all().data
        if results:
            if str(results.get("server", "")).lower() == proxy_ip.lower():
                new_resource = self.new(self._connection, results)
            else:
                new_resource = None
        return new_resource

    def delete(self):
        return self._helper.delete(self.URI)
