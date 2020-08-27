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

from unittest import TestCase

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.networking.internal_link_sets import InternalLinkSets
from hpeOneView.resources.resource import ResourceHelper

INTERNAL_LINK_SETS = [
    {'name': 'OneViewSDK Test Internal Link Set'},
    {'name': 'test'},
    {'name': 'OneViewSDK Test Internal Link Set'},
    {'name': 'abc'},
]


class InternalLinkSetsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = InternalLinkSets(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        query = 'teste'
        fields = 'a,b,c'
        view = 'teste'

        self._client.get_all(2, 500, filter, query, sort, view, fields)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort, query=query, fields=fields,
                                             view=view)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_without_parameters(self, mock_get_all):
        self._client.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='', query='', fields='', view='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_all):
        mock_get_all.return_value = INTERNAL_LINK_SETS
        expected_result = [
            {'name': 'OneViewSDK Test Internal Link Set'},
            {'name': 'OneViewSDK Test Internal Link Set'},
        ]

        result = self._client.get_by('name', 'OneViewSDK Test Internal Link Set')

        self.assertEqual(result, expected_result)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_should_return_empty_list_when_not_match(self, mock_get_all):
        mock_get_all.return_value = INTERNAL_LINK_SETS
        expected_result = []

        result = self._client.get_by('name', 'Testing')

        self.assertEqual(result, expected_result)
