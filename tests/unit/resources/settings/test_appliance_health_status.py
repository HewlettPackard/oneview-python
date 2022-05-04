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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.settings.appliance_health_status import ApplianceHealthStatus
from hpeOneView.resources.resource import Resource


class ApplianceHealthStatusTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._health_status = ApplianceHealthStatus(self.connection)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_health_status_called_once(self, mock_get):
        self._health_status.get_health_status()
        mock_get.assert_called_once_with('/rest/appliance/health-status')
