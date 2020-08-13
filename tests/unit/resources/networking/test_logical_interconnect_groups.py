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
from hpeOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class LogicalInterconnectGroupsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._lig = LogicalInterconnectGroups(self.connection)
        self.uri = "/rest/logical-interconnect-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._lig.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'TestScope'

        self._lig.get_all(2, 500, filter, sort, scope_uris)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._lig.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', scope_uris='')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_default_settings_called_once(self, mock_get):
        lig_settings_uri = "/rest/logical-interconnect-groups/defaultSettings"
        self._lig.get_default_settings()
        mock_get.assert_called_once_with(lig_settings_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_settings_called_once_when_lig_uri_provided(self, mock_get):
        lig_settings_uri = "{}/settings".format(self.uri)
        self._lig.get_settings()
        mock_get.assert_called_once_with(lig_settings_uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        lig = {
            "type": "logical-interconnect-groupV3",
            "name": "OneView Test Logical Interconnect Group",
            "interconnectMapTemplate": {
                "interconnectMapEntryTemplates": []
            },
            "uplinkSets": [],
            "enclosureType": "C7000",
        }
        self._lig.create(lig, timeout=70)
        mock_create.assert_called_once_with(lig, None, 70, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        lig = {
            "type": "logical-interconnect-groupV3",
            "name": "OneView Test Logical Interconnect Group",
            "interconnectMapTemplate": {
                "interconnectMapEntryTemplates": []
            },
            "uplinkSets": [],
            "enclosureType": "C7000",
        }
        self._lig.update(lig, timeout=70)

        lig["uri"] = self.uri

        mock_update.assert_called_once_with(lig, self.uri, False, 70, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._lig.delete(force=True, timeout=50)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            force=True, timeout=50)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self._lig.delete()

        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            force=False, timeout=-1)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._lig.patch('replace',
                        '/scopeUris',
                        ['rest/fake/scope123'],
                        timeout=-1)

        mock_patch.assert_called_once_with(self.uri,
                                           body=[{'path': '/scopeUris',
                                                  'value': ['rest/fake/scope123'],
                                                  'op': 'replace'}],
                                           custom_headers=None,
                                           timeout=-1)
