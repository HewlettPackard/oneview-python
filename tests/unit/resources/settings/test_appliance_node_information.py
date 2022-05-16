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
from hpeOneView.resources.settings.appliance_node_information import ApplianceNodeInformation
from hpeOneView.resources.resource import Resource


class ApplianceNodeInformationTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._node_information = ApplianceNodeInformation(self.connection)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_status_called_once(self, mock_get):
        self._node_information.get_status()
        mock_get.assert_called_once_with('/rest/appliance/nodeinfo/status')

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_version_called_once(self, mock_get):
        self._node_information.get_version()
        mock_get.assert_called_once_with('/rest/appliance/nodeinfo/version')
