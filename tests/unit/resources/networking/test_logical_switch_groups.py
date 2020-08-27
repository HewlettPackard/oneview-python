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
from hpOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class LogicalSwitchGroupsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._lsg = LogicalSwitchGroups(self.connection)
        self.uri = "/rest/logical-switch-groups/dce3fc90-873e-48f7-8340-cc927d625b16"
        self._lsg.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._lsg.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, filter='name=TestName',
                                             sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._lsg.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter=u'', sort=u'', start=0)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        lsg = {
            "name": "OneView Test Logical Switch Group",
            "switchMapTemplate": {
                "switchMapEntryTemplates": [{
                    "logicalLocation": {
                        "locationEntries": [{
                            "relativeValue": 1,
                            "type": "StackingMemberId"
                        }]
                    },
                    "permittedSwitchTypeUri": "/rest/switch-types/46d7ffad-4424-4e36-acf3-b379c3116206"
                }]
            }
        }
        self._lsg.create(lsg, timeout=70)
        mock_create.assert_called_once_with(lsg, None, 70, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        lsg = {
            "name": "Updated name",
            "switchMapTemplate": {
                "switchMapEntryTemplates": [{
                    "logicalLocation": {
                        "locationEntries": [{
                            "relativeValue": 1,
                            "type": "StackingMemberId"
                        }]
                    },
                    "permittedSwitchTypeUri": "/rest/switch-types/46d7ffad-4424-4e36-acf3-b379c3116206"
                }]
            },
            "uri": self.uri
        }
        self._lsg.update(lsg, timeout=70)
        mock_update.assert_called_once_with(lsg, self.uri, False, 70, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._lsg.delete(force=True, timeout=50)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=True, timeout=50)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self._lsg.delete()

        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=False, timeout=-1)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._lsg.patch('replace',
                        '/scopeUris', ['rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('/rest/logical-switch-groups/dce3fc90-873e-48f7-8340-cc927d625b16',
                                           body=[{'path': '/scopeUris',
                                                  'value': ['rest/fake/scope123'],
                                                  'op': 'replace'}],
                                           custom_headers=1, timeout=-1)
