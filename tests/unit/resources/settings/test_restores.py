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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.settings.restores import Restores


class RestoresTest(TestCase):
    def setUp(self):
        oneview_connection = connection('127.0.0.1')
        self.resource = Restores(oneview_connection)

        self.restores = [
            {"backupIdToRestore": "example_backup_2017-03-06_023131"},
            {"backupIdToRestore": "example_backup_2017-04-06_023131"}
        ]

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        self.resource.get_all()
        mock_get_all.assert_called_once()

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_restores_when_found(self, mock_get_all):
        mock_get_all.return_value = self.restores

        expected_result = [self.restores[0]]

        result = self.resource.get_by("backupIdToRestore", "example_backup_2017-03-06_023131")

        mock_get_all.assert_called_once_with(filter='"backupIdToRestore=\'example_backup_2017-03-06_023131\'"',
                                             uri='/rest/restores')
        self.assertEqual(result, expected_result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_should_return_empty_list_when_not_found(self, mock_get_all):
        mock_get_all.return_value = []

        result = self.resource.get_by("backupIdToRestore", "example_backup_2017-03-06_023131")

        self.assertEqual(result, [])

    @mock.patch.object(ResourceClient, 'get')
    def test_get_should_be_called_once(self, mock_get):
        self.resource.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_should_be_called_once(self, mock_get):
        uri = '/rest/restores/3518be0e-17c1-4189-8f81-83f3724f6155'
        self.resource.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_failure_should_be_called_once(self, mock_get):
        uri = '/rest/restores/failure'
        self.resource.get_failure()

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_restore_should_be_called_once(self, mock_create):
        restore = {
            "uriOfBackupToRestore": "/rest/backups/example_backup_2014-03-06_023131"
        }
        self.resource.restore(restore)

        mock_create.assert_called_once_with(restore, timeout=-1, default_values=self.resource.DEFAULT_VALUES)
