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


from hpeOneView.resources.resource import Resource, unavailable_method


class SasInterconnectTypes(Resource):
    """
    SAS Interconnect Types API client.

    Note:
        This resource is only available on HPE Synergy.

    """
    URI = '/rest/sas-interconnect-types'

    def __init__(self, connection, data=None):
        super(SasInterconnectTypes, self).__init__(connection, data)

    def create(self):
        """Create method is not available"""
        unavailable_method()

    def delete(self):
        """Delete method is not avaialble"""
        unavailable_method()

    def update(self):
        """Update method is not avaialble"""
        unavailable_method()
