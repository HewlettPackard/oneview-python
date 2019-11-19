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
from hpOneView.resources.settings.firmware_bundles import FirmwareBundles
from hpOneView.resources.resource import ResourceClient


class FirmwareBundlesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._firmware_bundles = FirmwareBundles(self.connection)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload(self, mock_upload):
        firmware_path = "test/SPPgen9snap6.2015_0405.81.iso"

        self._firmware_bundles.upload(firmware_path)

        mock_upload.assert_called_once_with(firmware_path, timeout=-1)
