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

from hpeOneView.resources.resource import ResourceClient


class ApplianceDeviceReadCommunity(object):
    """
    ApplianceDeviceReadCommunity API client.
    The device read community string is used by the appliance to establish SNMP communication with devices managed by the appliance.
    """
    URI = '/rest/appliance/device-read-community-string'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get(self):
        """
        Retrieves the global community string.

        Returns:
            dict: ApplianceDeviceReadCommunity
        """
        return self._client.get(self.URI)

    def update(self, resource, timeout=-1):
        """
        Update the device read community string.
        This results in an update of the community string on all servers being managed/monitored by this OneView instance.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated appliance SNMPv1 read community string.
        """
        return self._client.update(resource, timeout=timeout)
