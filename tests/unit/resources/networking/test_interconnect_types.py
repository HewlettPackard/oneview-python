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

from hpeOneView.connection import connection
from hpeOneView.resources.networking.interconnect_types import InterconnectTypes
from hpeOneView.resources.resource import Resource, ResourceHelper


class InterconnectTypesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnect_types = InterconnectTypes(self.connection)

    @mock.patch.object(ResourceHelper, 'do_requests_to_getall')
    def test_get_all_called_once(self, mock_do_get):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnect_types.get_all(2, 500, filter=filter, sort=sort)

        mock_do_get.assert_called_once_with('/rest/interconnect-types?start=2&count=500&filter=name%3DTestName&sort=name%3Aascending', 500)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._interconnect_types.get_by_name('HP VC Flex-10 Enet Module')

        mock_get_by.assert_called_once_with(
            'name', 'HP VC Flex-10 Enet Module')
