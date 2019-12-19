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

from hpOneView.resources.resource import Resource, ResourcePatchMixin


class FcNetworks(ResourcePatchMixin, Resource):
    """
    Fibre Channel networks API client.

    """

    URI = '/rest/fc-networks'

    DEFAULT_VALUES = {
        '200': {'type': 'fc-networkV2'},
        '300': {"type": "fc-networkV300"},
        '500': {"type": "fc-networkV300"},
        '600': {"type": "fc-networkV4"},
        '800': {"type": "fc-networkV4"},
        '1000': {"type": "fc-networkV4"},
        '1200': {"type": "fc-networkV4"}
    }

    def __init__(self, connection, data=None):
        super(FcNetworks, self).__init__(connection, data)
