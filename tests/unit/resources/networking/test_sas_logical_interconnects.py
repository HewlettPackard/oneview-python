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
from hpeOneView.resources.networking.sas_logical_interconnects import SasLogicalInterconnects
from hpeOneView.resources.resource import ResourceHelper


class SasLogicalInterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = SasLogicalInterconnects(self.connection)
        self.uri = "/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        self._client.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, fields='name=TestName', filter='name:ascending', query='',
                                             sort='', start=2, view='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._client.get_all()
        mock_get_all.assert_called_once_with(count=-1, fields='', filter='', query='', sort='', start=0, view='')

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'create')
    def test_replace_drive_enclosure_called_once(self, mock_create, mock_get):
        drive_replacement = {
            "oldSerialNumber": "SN1100",
            "newSerialNumber": "SN1101"
        }
        self._client.replace_drive_enclosure(drive_replacement)

        mock_create.assert_called_once_with(
            drive_replacement.copy(),
            '{}/replaceDriveEnclosure'.format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_compliance_all_called_once(self, mock_update, mock_get):
        compliance_uris = {
            "uris": [
                "/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
            ]}

        self._client.update_compliance_all(compliance_uris)

        mock_update.assert_called_once_with(compliance_uris.copy(),
                                            '/rest/sas-logical-interconnects/compliance',
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_compliance(self, mock_update, mock_get):
        self._client.update_compliance()

        mock_update.assert_called_once_with({}, '{}/compliance'.format(self.uri), timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_configuration(self, mock_update, mock_get):
        self._client.update_configuration()

        mock_update.assert_called_once_with({}, '{}/configuration'.format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware(self, mock_get):
        expected_uri = self.uri + "/firmware"

        self._client.get_firmware()
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_firmware(self, mock_update, mock_get):
        fake_firmware = dict(
            command="Update",
            sppUri="/rest/firmware-drivers/Service_0Pack_0for_0ProLiant"
        )

        expected_uri = self.uri + "/firmware"

        self._client.update_firmware(fake_firmware)
        mock_update.assert_called_once_with(fake_firmware, expected_uri, force=False)
