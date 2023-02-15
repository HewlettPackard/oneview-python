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
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin
from hpeOneView.resources.storage.sas_logical_jbods import SasLogicalJbods


class SasLogicalJbodsTest(unittest.TestCase):

    SAS_LOGICAL_JBOD_ID = 'c8ed5329-f9c1-492c-aa46-b78665ee7734'
    SAS_LOGICAL_JBOD_URI = '/rest/sas-logical-jbods/' + SAS_LOGICAL_JBOD_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._resource = SasLogicalJbods(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        args = dict(
            start=2,
            count=500,
            filter='name=TestName',
            sort='name:ascending'
        )

        self._resource.get_all(**args)
        mock_get_all.assert_called_once_with(**args)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_called_once(self, mock_get):
        self._resource.get_by_uri(self.SAS_LOGICAL_JBOD_URI)
        mock_get.assert_called_once_with(self.SAS_LOGICAL_JBOD_URI)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._resource.get_by('name', 'SAS Logical JBOD Name')

        mock_get_by.assert_called_once_with('name', 'SAS Logical JBOD Name')

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_create_called_once(self, mock_do_post):
        options = {
            "numPhysicalDrives": 1,
            "name": "SasLogicalJBOD1",
            "description": "Sas Jbod description",
            "minSizeGB": 200,
            "maxSizeGB": 600,
            "eraseData": "true",
            "driveTechnology":
            {
                "deviceInterface": "SAS",
                "driveMedia": "HDD"
            },
            "driveEnclosureUris": ["drive_enclosure_uri_list"],
        }
        self._resource.create(options)
        mock_do_post.assert_called_once_with(SasLogicalJbods.URI, options, -1, None)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_called_once(self, mock_patch):
        patch_config = dict(
            operation="replace",
            path="/name",
            value="jbod_new_name"
        )
        self._resource.data = {"name": "name",
                               "uri": self.SAS_LOGICAL_JBOD_URI}
        self._resource.patch(**patch_config)
        mock_patch.assert_called_once_with(**patch_config)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._resource.delete(self.SAS_LOGICAL_JBOD_ID, force=False, timeout=-1)

        mock_delete.assert_called_once_with(self.SAS_LOGICAL_JBOD_ID, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_drives_called_once(self, mock_do_get):

        self._resource.data = {"name": "name",
                                       "uri": self.SAS_LOGICAL_JBOD_URI}
        self._resource.get_drives()

        expected_uri = self.SAS_LOGICAL_JBOD_URI + "/drives"
        mock_do_get.assert_called_once_with(expected_uri)
