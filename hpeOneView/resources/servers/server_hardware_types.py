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


from hpeOneView.resources.resource import Resource, ensure_resource_client


class ServerHardwareTypes(Resource):
    """
    The server hardware types resource is a representation/abstraction of a physical server managed by the appliance.
    It defines capabilities and settings that can be used in a server profile.

    """
    URI = '/rest/server-hardware-types'

    def __init__(self, connection, data=None):
        super(ServerHardwareTypes, self).__init__(connection, data)

    @ensure_resource_client
    def update(self, data, timeout=-1, force=False):
        """
        Updates one or more attributes for a server hardware type resource.
        Args:
            data (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            force: Flag to force the operation.
        Returns:
            dict: Updated server hardware type.
        """
        uri = self.data["uri"]
        self.data = self._helper.update(data, uri=uri, timeout=timeout, force=force)

        return self
