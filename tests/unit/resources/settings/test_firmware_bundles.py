# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
from hpeOneView.resources.settings.firmware_bundles import FirmwareBundles
from hpeOneView.resources.resource import ResourceFileHandlerMixin, Resource


class FirmwareBundlesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self.uri = "/rest/firmware-bundles"
        self._firmware_bundles = FirmwareBundles(self.connection)

    @mock.patch.object(ResourceFileHandlerMixin, 'upload')
    def test_upload_firmware(self, mock_upload):
        firmware_path = "test/SPPgen9snap6.2015_0405.81.iso"
        self._firmware_bundles.upload(firmware_path)
        mock_upload.assert_called_once_with(firmware_path)

    @mock.patch.object(ResourceFileHandlerMixin, 'upload')
    def test_upload_compsig(self, mock_upload):
        sigfile = "test.sig"
        uri = self.uri + "/addCompsig"
        self._firmware_bundles.upload_compsig(sigfile)
        mock_upload.assert_called_once_with(sigfile, uri, -1)
