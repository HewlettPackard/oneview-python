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

from hpeOneView.resources.resource import Resource, ResourcePatchMixin, unavailable_method


class HANodes(Resource, ResourcePatchMixin):
    """
    HA Nodes resources represent the individual members used to provide
    high-availability for the management appliance cluster.

    """
    URI = '/rest/appliance/ha-nodes'

    def __init__(self, connection, data=None):
        super(HANodes, self).__init__(connection, data)

    def create(self):
        """Create method is not available"""
        unavailable_method()
