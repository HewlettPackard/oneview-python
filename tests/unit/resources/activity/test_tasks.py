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

from hpeOneView.exceptions import HPEOneViewException
from unittest import TestCase

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.activity.tasks import Tasks
from hpeOneView.resources.resource import (ResourceHelper, TaskMonitor)


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
                                         query='', sort='name:ascending', start=0, view='day', topCount=0, childLimit=0)

    @mock.patch.object(TaskMonitor, "wait_for_task")
    @mock.patch.object(connection, "do_http")
    def test_patch_request_with_status_202(self, mock_do_http, mock_wait4task):
        fake_associated_resource = mock.Mock()
        mockedResponse = type('mockResponse', (), {'status': 202})()
        mockedTaskBody = {'category': 'tasks'}

        mock_do_http.return_value = (mockedResponse, mockedTaskBody)
        mock_wait4task.return_value = fake_associated_resource
        mock_do_http.assert_once_called_with('PATCH', '/uri')
        mock_wait4task.assert_called_once()
        return_patch_request = self._tasks.patch('/uri')
        self.assertEqual(return_patch_request, fake_associated_resource)

    @mock.patch.object(TaskMonitor, "wait_for_task")
    @mock.patch.object(connection, "do_http")
    def test_patch_request_with_status_400(self, mock_do_http, mock_wait4task):
        fake_associated_resource = mock.Mock()
        mockedResponse = type('mockResponse', (), {'status': 400})()
        mockedTaskBody = {'category': 'tasks'}

        mock_do_http.return_value = (mockedResponse, mockedTaskBody)
        mock_wait4task.return_value = fake_associated_resource
        mock_do_http.assert_once_called_with('PATCH', '/uri')
        mock_wait4task.assert_called_once()
        try:
            self._tasks.patch('/uri')
        except HPEOneViewException as e:
            self.assertEqual(e.msg, mockedTaskBody)
