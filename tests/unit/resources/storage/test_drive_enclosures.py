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
from hpeOneView.resources.storage.drive_enclosures import DriveEnclosures
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class DriveEnclosuresTest(unittest.TestCase):

    DRIVE_ENCLOSURE_ID = "SN123101"
    DRIVE_ENCLOSURE_URI = "/rest/drive-enclosures/" + DRIVE_ENCLOSURE_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._drive_enclosures = DriveEnclosures(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._drive_enclosures.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._drive_enclosures.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='')

    @mock.patch.object(Resource, 'get_by_id')
    def test_get_by_id_called_once(self, mock_get_by_id):
        self._drive_enclosures.get_by_id(self.DRIVE_ENCLOSURE_ID)
        mock_get_by_id.assert_called_once_with(self.DRIVE_ENCLOSURE_ID)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        field = 'serialNumber'
        value = 'SN123101'

        self._drive_enclosures.get_by(field, value)
        mock_get_by.assert_called_once_with(field, value)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_port_map_called_once(self, mock_do_get):
        self._drive_enclosures.data = {"name": "name",
                                       "uri": self.DRIVE_ENCLOSURE_URI}
        self._drive_enclosures.get_port_map()

        expected_uri = self.DRIVE_ENCLOSURE_URI + "/port-map"
        mock_do_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'update')
    def test_refresh_state_called_once(self, mock_update):
        refresh_config = dict(refreshState="RefreshPending")
        self._drive_enclosures.data = {"name": "name",
                                       "uri": self.DRIVE_ENCLOSURE_URI}

        self._drive_enclosures.refresh_state(refresh_config)

        expected_uri = self.DRIVE_ENCLOSURE_URI + "/refreshState"
        mock_update.assert_called_once_with(uri=expected_uri, resource=refresh_config, timeout=-1)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_called_once(self, mock_patch):
        patch_config = dict(
            operation="replace",
            path="/powerState",
            value="Off"
        )
        self._drive_enclosures.data = {"name": "name",
                                       "uri": self.DRIVE_ENCLOSURE_URI}
        self._drive_enclosures.patch(**patch_config)
        mock_patch.assert_called_once_with(**patch_config)
