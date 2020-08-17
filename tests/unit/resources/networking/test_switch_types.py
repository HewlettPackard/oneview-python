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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.switch_types import SwitchTypes
from hpOneView.resources.resource import ResourceHelper


class SwitchTypesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._switch_types = SwitchTypes(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._switch_types.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500,
                                             filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_all):
        self._switch_types.get_by('name', 'Cisco Nexus 6xxx')

        mock_get_all.assert_called_once_with(count=-1,
                                             filter='"name=\'Cisco Nexus 6xxx\'"',
                                             sort='', start=0)
