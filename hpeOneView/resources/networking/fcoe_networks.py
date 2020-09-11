# -*- coding: utf-8 -*-
###
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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


from hpeOneView.resources.resource import Resource, ResourcePatchMixin


class FcoeNetworks(ResourcePatchMixin, Resource):
    """
    FCoE Networks API client.

    """
    URI = '/rest/fcoe-networks'

    DEFAULT_VALUES = {
        '200': {"type": "fcoe-network"},
        '300': {"type": "fcoe-networkV300"},
        '500': {"type": "fcoe-networkV300"},
        '600': {"type": "fcoe-networkV4"},
        '800': {"type": "fcoe-networkV4"},
        '1000': {"type": "fcoe-networkV4"},
        '1200': {"type": "fcoe-networkV4"},
        '1600': {"type": "fcoe-networkV4"},
        '1800': {"type": "fcoe-networkV4"}

    }

    def __init__(self, connection, data=None):
        super(FcoeNetworks, self).__init__(connection, data)

    def delete_bulk(self, resource, timeout=-1):
        """
        Deletes bulk FCoE networks.

        Args:
            resource (dict): Specifications to delete in bulk.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        """
        uri = self.URI + '/bulk-delete'

        return self._helper.create(resource, uri=uri, timeout=timeout)
