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

from unittest import TestCase

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.servers.logical_enclosures import LogicalEnclosures
from hpeOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class LogicalEnclosuresTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._logical_enclosures = LogicalEnclosures(self.connection)
        self.uri = "/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        self._logical_enclosures.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            enclosureUris=[
                "/rest/enclosures/0000000000A66101",
                "/rest/enclosures/0000000000A66102",
                "/rest/enclosures/0000000000A66103"
            ],
            enclosureGroupUri="/rest/enclosure-groups/e41118e4-2233-4b6b-9318-c9982dbf01fa",
            forceInstallFirmware=False,
            name="testLogicalEnclosure"
        )
        mock_create.return_value = {}

        self._logical_enclosures.create(resource)
        mock_create.assert_called_once_with(resource.copy(), None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._logical_enclosures.delete(force=False)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        self._logical_enclosures.delete(force=True)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            force=True, timeout=-1)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'

        self._logical_enclosures.get_all(2, 500, filter, sort, scope_uris)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._logical_enclosures.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', scope_uris='')

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_name_called_once(self, mock_get_by):
        self._logical_enclosures.get_by_name('OneViewSDK-Test-Logical-Enclosure')
        mock_get_by.assert_called_once_with('name', 'OneViewSDK-Test-Logical-Enclosure')

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once_with_defaults(self, mock_update, mock_ensure_client):
        logical_enclosure = {
            "name": "one_enclosure_le",
        }
        logical_enclosure["uri"] = self.uri
        self._logical_enclosures.update(logical_enclosure)
        mock_update.assert_called_once_with(logical_enclosure, self.uri, False, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        logical_enclosure = {
            "name": "one_enclosure_le",
        }
        logical_enclosure["uri"] = self.uri
        self._logical_enclosures.update(logical_enclosure, 70)
        mock_update.assert_called_once_with(logical_enclosure, self.uri,
                                            False, 70, None)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}
        custom_headers = {'If-Match': '*'}

        self._logical_enclosures.patch(
            'replace', '/name', 'new_name', custom_headers, 1)
        mock_patch.assert_called_once_with(self.uri,
                                           body=[{'path': '/name',
                                                  'op': 'replace',
                                                  'value': 'new_name'}],
                                           custom_headers={'If-Match': '*'},
                                           timeout=1)

    @mock.patch.object(Resource, 'refresh')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_configuration(self, mock_update, mock_refresh):
        uri_rest_call = '{}/configuration'.format(self.uri)

        self._logical_enclosures.update_configuration()

        mock_update.assert_called_once_with(None, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_script(self, mock_get):
        uri_rest_call = '{}/script'.format(self.uri)

        self._logical_enclosures.get_script()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_script(self, mock_update):
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/script'
        information = {"#TEST COMMAND": ""}
        configuration_rest_call = information.copy()

        self._logical_enclosures.update_script(information)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'create')
    def test_support_dump_called_once(self, mock_create):
        information = {
            "errorCode": "MyDump16",
            "encrypt": True,
            "excludeApplianceDump": False
        }
        uri_rest_call = '{}/support-dumps'.format(self.uri)

        mock_create.return_value = {}

        self._logical_enclosures.generate_support_dump(information)
        mock_create.assert_called_once_with(
            information.copy(), uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_from_group(self, mock_update):
        uri_rest_call = '{}/updateFromGroup'.format(self.uri)

        self._logical_enclosures.update_from_group()

        mock_update.assert_called_once_with(None, uri_rest_call, timeout=-1)
