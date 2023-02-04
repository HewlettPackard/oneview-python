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


from hpeOneView.resources.resource import (Resource, ResourcePatchMixin, ensure_resource_client)


class DriveEnclosures(Resource, ResourcePatchMixin):
    """
    Drive Enclosures API client.

    Note:
        This resource is only available on HPE Synergy

    """
    URI = '/rest/drive-enclosures'

    def __init__(self, connection, data=None):
        super(DriveEnclosures, self).__init__(connection, data)

    @ensure_resource_client
    def get_port_map(self):
        """
        Use to get the drive enclosure I/O adapter port to SAS interconnect port connectivity.

        Returns:
            dict: Drive Enclosure Port Map
        """
        uri = "{}/port-map".format(self.data['uri'])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def refresh_state(self, configuration, timeout=-1):
        """
        Refreshes a drive enclosure.

        Args:
            configuration: Configuration
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Drive Enclosure
        """
        uri = "{}/refreshState".format(self.data['uri'])
        return self._helper.update(resource=configuration, uri=uri, timeout=timeout)
