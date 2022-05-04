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

from hpeOneView.resources.resource import Resource


class ApplianceNodeInformation(Resource):
    """
    The nodeinfo resource manager provides REST APIs to
    retrieve information about the nodes of the appliance.

    """
    URI = '/rest/appliance/nodeinfo'

    def __init__(self, connection, data=None):
        super(ApplianceNodeInformation, self).__init__(connection, data)

    def get_status(self):
        """
        Retrieves node's status information

        Returns:
            dict: Node's status information
        """
        uri = self.URI + '/status'
        return super(ApplianceNodeInformation, self).get_by_uri(uri)

    def get_version(self):
        """
        Retrieves node's version information

        Returns:
            dict: Node's version information
        """
        uri = self.URI + '/version'
        return super(ApplianceNodeInformation, self).get_by_uri(uri)
