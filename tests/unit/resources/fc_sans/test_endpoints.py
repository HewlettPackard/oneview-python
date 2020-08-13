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

from unittest import TestCase

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.resource import ResourceClient
from hpeOneView.resources.fc_sans.endpoints import Endpoints

TIMEOUT = -1


class EndpointsTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = Endpoints(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_with_defaults(self, mock_get_all):
        self._resource.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, query='', sort='')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, query=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, query=query_filter, sort=sort)
