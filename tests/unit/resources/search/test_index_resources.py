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
from hpOneView.resources.search.index_resources import IndexResources
from hpOneView.resources.resource import ResourceClient


class IndexResourcesTest(unittest.TestCase):

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
        self.connection = connection(self.host)
        self._resource = IndexResources(self.connection)

    @mock.patch.object(ResourceClient, 'get_all', return_value=dict(members='test'))
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        expected_uri = '/rest/index/resources?filter=name=TestName&sort=name:ascending'

        self._resource.get_all(start=2, count=500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, uri=expected_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_without_results(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        expected_uri = '/rest/index/resources?filter=name=TestName&sort=name:ascending'
        self._resource.get_all(start=2, count=500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, uri=expected_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        index_uri = "/rest/server-hardwares/fake"
        expected_call_uri = "/rest/index/resources/rest/server-hardwares/fake"
        self._resource.get(index_uri)
        mock_get.assert_called_once_with(expected_call_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_aggregated_called_once(self, mock_get_aggregated):

        expected_uri = '/rest/index/resources/aggregated?attribute=Model&attribute=State&category=server-hardware&childLimit=6'

        self._resource.get_aggregated(['Model', 'State'], 'server-hardware')
        mock_get_aggregated.assert_called_once_with(expected_uri)


if __name__ == '__main__':
    unittest.main()
