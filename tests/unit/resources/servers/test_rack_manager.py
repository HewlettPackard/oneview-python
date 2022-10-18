# -*- coding: utf-8 -*-
###
# (C) Copyright [2022] Hewlett Packard Enterprise Development LP
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
from hpeOneView.resources.servers.rack_manager import RackManager
from hpeOneView.resources.resource import (Resource, ResourceHelper,
                                           ResourcePatchMixin)


class RackManagerTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._rack_manager = RackManager(self.connection)
        self.uri = '/rest/rack-manager/1224242424'
        self._rack_manager.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._rack_manager.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._rack_manager.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._rack_manager.get_by('name', 'OneViewSDK-Test-RackManager')
        mock_get_by.assert_called_once_with('name', 'OneViewSDK-Test-RackManager')

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once(self, mock_create):
        options = {
            "hostname": "testhost.com",
            "username": "test_user",
            "password": "test_pass",
            "force": False
        }
        mock_create.return_value = {}

        self._rack_manager.add(options)
        mock_create.assert_called_once_with(options.copy(), None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_environmental_configuration(self, mock_get):
        self._rack_manager.get_environmental_configuration()
        mock_get.assert_called_once_with("{}/environmentalConfiguration".format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_remote_support_settings(self, mock_get):
        self._rack_manager.get_remote_support_settings()
        mock_get.assert_called_once_with("{}/remoteSupportSettings".format(self.uri))

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._rack_manager.remove(force=False)

        mock_delete.assert_called_once_with(self.uri, force=False,
                                            custom_headers=None, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        self._rack_manager.remove(force=True)

        mock_delete.assert_called_once_with(self.uri, force=True,
                                            custom_headers=None,
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_all_chassis(self, mock_get):
        self._rack_manager.get_all_chassis()
        mock_get.assert_called_once_with("/rest/rack-managers/chassis")

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_all_managers(self, mock_get):
        self._rack_manager.get_all_managers()
        mock_get.assert_called_once_with("/rest/rack-managers/managers")

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_all_partitions(self, mock_get):
        self._rack_manager.get_all_partitions()
        mock_get.assert_called_once_with("/rest/rack-managers/partitions")

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_associated_chassis(self, mock_get):
        self._rack_manager.get_associated_chassis()
        mock_get.assert_called_once_with("{}/chassis".format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_associated_managers(self, mock_get):
        self._rack_manager.get_associated_managers()
        mock_get.assert_called_once_with("{}/managers".format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_associated_partitions(self, mock_get):
        self._rack_manager.get_associated_partitions()
        mock_get.assert_called_once_with("{}/partitions".format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_a_specific_resource(self, mock_get):
        uri = '/rest/rack-managers/12345678/managers/abcdefgh/'
        self._rack_manager.get_a_specific_resource(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_called_once(self, mock_patch):
        self._rack_manager.patch('RefreshRackManagerOp', '', '')

        mock_patch.assert_called_once_with(self.uri,
                                           body=[{'op': 'RefreshRackManagerOp',
                                                  'path': '',
                                                  'value': ''}],
                                           custom_headers=None,
                                           timeout=-1)
