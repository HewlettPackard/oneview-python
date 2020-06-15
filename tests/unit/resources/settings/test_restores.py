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

from hpOneView.connection import connection
from hpOneView.resources.resource import Resource, ResourceHelper
from hpOneView.resources.settings.restores import Restores


class RestoresTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.resource = Restores(self.connection)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_failure_should_be_called_once(self, mock_get):
        uri = '/rest/restores/failure'
        self.resource.get_failure()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'create')
    def test_restore_should_be_called_once(self, mock_create):
        restore = {
            "uriOfBackupToRestore": "/rest/backups/example_backup_2014-03-06_023131"
        }
        self.resource.restore(restore)
        mock_create.assert_called_once_with(restore, timeout=-1)

