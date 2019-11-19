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
from hpOneView.resources.networking.interconnect_link_topologies import InterconnectLinkTopologies
from hpOneView.resources.resource import ResourceClient


class InterconnectLinkTopologiesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnect_link_topologies = InterconnectLinkTopologies(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once_by_id(self, mock_get):
        ilt_id = 'c6f4e705-2bb5-430a-b7a1-a35b2f7aa9b9'
        self._interconnect_link_topologies.get(ilt_id)

        mock_get.assert_called_once_with(ilt_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once_by_uri(self, mock_get):
        ilt_uri = '/rest/interconnect-link-topologies/c6f4e705-2bb5-430a-b7a1-a35b2f7aa9b9'
        self._interconnect_link_topologies.get(ilt_uri)

        mock_get.assert_called_once_with(ilt_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnect_link_topologies.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._interconnect_link_topologies.get_by('name', 'sample name')

        mock_get_by.assert_called_once_with(
            'name', 'sample name')
