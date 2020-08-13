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
from hpeOneView.resources.storage.sas_logical_jbod_attachments import SasLogicalJbodAttachments
from hpeOneView.resources.resource import ResourceClient


class SasLogicalJbodAttachmentsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._sas_logical_jbod_attachments = SasLogicalJbodAttachments(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._sas_logical_jbod_attachments.get_all(2, 500, filter, sort)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._sas_logical_jbod_attachments.get_by('name', 'SAS Logical JBOD Attachment Name')

        mock_get_by.assert_called_once_with('name', 'SAS Logical JBOD Attachment Name')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._sas_logical_jbod_attachments.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/sas-logical-jbods-attachments/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._sas_logical_jbod_attachments.get(uri)

        mock_get.assert_called_once_with(uri)
