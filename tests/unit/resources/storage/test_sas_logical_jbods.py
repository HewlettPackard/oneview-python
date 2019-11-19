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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.storage.sas_logical_jbods import SasLogicalJbods


class SasLogicalJbodsTest(unittest.TestCase):

    SAS_LOGICAL_JBOD_ID = 'c8ed5329-f9c1-492c-aa46-b78665ee7734'
    SAS_LOGICAL_JBOD_URI = '/rest/sas-logical-jbods/' + SAS_LOGICAL_JBOD_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._resource = SasLogicalJbods(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        args = dict(
            start=2,
            count=500,
            filter='name=TestName',
            sort='name:ascending'
        )

        self._resource.get_all(**args)
        mock_get_all.assert_called_once_with(**args)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._resource.get(id_or_uri=self.SAS_LOGICAL_JBOD_ID)
        mock_get.assert_called_once_with(id_or_uri=self.SAS_LOGICAL_JBOD_ID)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._resource.get_by('name', 'SAS Logical JBOD Name')

        mock_get_by.assert_called_once_with('name', 'SAS Logical JBOD Name')

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'get')
    def test_get_drives_called_once(self, mock_get, mock_build_uri):
        mock_build_uri.return_value = self.SAS_LOGICAL_JBOD_URI
        self._resource.get_drives(id_or_uri=self.SAS_LOGICAL_JBOD_ID)

        expected_uri = self.SAS_LOGICAL_JBOD_URI + SasLogicalJbods.DRIVES_PATH
        mock_build_uri.assert_called_once_with(id_or_uri=self.SAS_LOGICAL_JBOD_ID)
        mock_get.assert_called_once_with(id_or_uri=expected_uri)
