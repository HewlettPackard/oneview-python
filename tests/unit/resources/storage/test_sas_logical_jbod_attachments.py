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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.storage.sas_logical_jbod_attachments import SasLogicalJbodAttachments
from hpeOneView.resources.resource import Resource, ResourceHelper


class SasLogicalJbodAttachmentsTest(unittest.TestCase):
    SAS_LOGICAL_JBOD_ATTACHMENT_ID = 'c8ed5329-f9c1-492c-aa46-b78665ee7734'
    SAS_LOGICAL_JBOD_ATTACHMENT_URI = '/rest/sas-logical-jbod-attachments/' + SAS_LOGICAL_JBOD_ATTACHMENT_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._sas_logical_jbod_attachments = SasLogicalJbodAttachments(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        mock_get_all.get_all(2, 500, filter, sort)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._sas_logical_jbod_attachments.get_by('name', 'SAS Logical JBOD Attachment Name')

        mock_get_by.assert_called_once_with('name', 'SAS Logical JBOD Attachment Name')

    @mock.patch.object(Resource, 'get_by_id')
    def test_get_by_id_called_once(self, mock_get):
        self._sas_logical_jbod_attachments.get_by_id(self.SAS_LOGICAL_JBOD_ATTACHMENT_ID)

        mock_get.assert_called_once_with(self.SAS_LOGICAL_JBOD_ATTACHMENT_ID)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get):
        self._sas_logical_jbod_attachments.get_by_uri(self.SAS_LOGICAL_JBOD_ATTACHMENT_URI)

        mock_get.assert_called_once_with(self.SAS_LOGICAL_JBOD_ATTACHMENT_URI)
