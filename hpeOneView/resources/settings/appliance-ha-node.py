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


class ApplianceInformation(object):
    """
    ApplianceInformation API client.

    """
    URI = '/rest/appliance'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def ha_node_status(self):
        """
        Retrieves the appliance ha node's status information

        Returns:
            dict: Node's status information
        """
        uri = self.URI + '/ha-nodes'
        return self._client.get(uri)
