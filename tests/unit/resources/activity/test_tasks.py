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
from hpOneView.resources.activity.tasks import Tasks
from hpOneView.resources.resource import ResourceHelper


class TasksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._tasks = Tasks(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get):
        self._tasks.get_all(fields='parentTaskUri,owner,name',
                            filter="\"taskState='Running'&filter=associatedResource.resourceCatgory='appliance'\"",
                            sort='name:ascending',
                            view='day')

        mock_get.assert_called_once_with(count=-1, fields='parentTaskUri,owner,name',
                                         filter='"taskState=\'Running\'&filter=associatedResource'
                                                '.resourceCatgory=\'appliance\'"',
                                         query='', sort='name:ascending', start=0, view='day')
