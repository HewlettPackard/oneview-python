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
from hpeOneView.resources.search.index_resources import IndexResources
from hpeOneView.resources.resource import Resource, ResourceHelper


class IndexResourcesTest(TestCase):

    INDEX_RESOURCE = dict(
        uri="/rest/index/resources/rest/resource/uri",
        resourceUri="/rest/resource/uri",
        type="IndexResourceV300",
        category="the-resource-category",
        created="2014-03-31T02:08:27.884Z",
        modified="2014-03-31T02:08:27.884Z",
        eTag=None,
        members=[{'name': 'sh1'}, {'name': 'sh2'}]
    )

    def return_index(self):
        return self.INDEX_RESOURCE

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._indexresource = IndexResources(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all', return_value=dict(members='test'))
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        expected_uri = '/rest/index/resources?'

        self._indexresource.get_all(start=2, count=500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, fields='', query='', view='', sort=sort, uri=expected_uri)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_without_results(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        expected_uri = '/rest/index/resources?'
        self._indexresource.get_all(start=2, count=500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, fields='', query='', view='', sort=sort, uri=expected_uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri):

        expected_uri = '/rest/index/resources/rest/server-hardware/1'

        self._indexresource.get_by_uri('/rest/server-hardware/1')
        mock_get_by_uri.assert_called_once_with(expected_uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_aggregated_called_once(self, mock_get_aggregated):

        expected_uri = '/rest/index/resources/aggregated?attribute=Model&attribute=State&category=server-hardware&childLimit=6'

        self._indexresource.get_aggregated(['Model', 'State'], 'server-hardware')
        mock_get_aggregated.assert_called_once_with(expected_uri)
