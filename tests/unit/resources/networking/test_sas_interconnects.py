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

from hpeOneView.resources.networking.sas_interconnects import SasInterconnects
from hpeOneView.resources.resource import ResourceHelper, ResourcePatchMixin


class SasInterconnectsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self._sas_interconnects = SasInterconnects(None)
        self.uri = '/rest/sas-interconnects/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._sas_interconnects.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._sas_interconnects.get_all(2, 500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort, query='', view='', fields='')

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_called_once(self, mock_patch_request):
        args = dict(
            operation='replace',
            path='/deviceResetState',
            value='Reset',
        )

        self._sas_interconnects.patch(**args)
        mock_patch_request.assert_called_once_with(self.uri,
                                                   body=[{'path': '/deviceResetState',
                                                          'op': 'replace',
                                                          'value': 'Reset'}],
                                                   custom_headers=None, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_refresh_state_called_once(self, mock_update):
        configuration = dict(refreshState="RefreshPending")
        expected_uri = "{}/refreshState".format(self.uri)

        self._sas_interconnects.refresh_state(configuration=configuration)

        mock_update.assert_called_once_with(resource=configuration, uri=expected_uri)
