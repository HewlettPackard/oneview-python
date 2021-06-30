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


class ApplianceHealthStatus(Resource):
    """
    Retrieves the health information from the appliance.

    """
    URI = '/rest/appliance/health-status'

    def __init__(self, connection, data=None):
        super(ApplianceHealthStatus, self).__init__(connection, data)

    def get_health_status(self):
        """
        Retrieves appliance health status

        Returns:
            dict: appliance health status
        """
        return super(ApplianceHealthStatus, self).get_by_uri(self.URI)
