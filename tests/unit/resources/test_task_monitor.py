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
from mock import mock, call
from errno import ETIMEDOUT, ECONNABORTED

from hpeOneView.connection import connection
from hpeOneView.resources.task_monitor import TaskMonitor, MSG_UNKNOWN_OBJECT_TYPE, MSG_TASK_TYPE_UNRECONIZED, \
    MSG_TIMEOUT, MSG_UNKNOWN_EXCEPTION, MSG_INVALID_TASK
from hpeOneView.exceptions import HPEOneViewUnknownType, HPEOneViewInvalidResource, HPEOneViewTimeout, HPEOneViewTaskError

ERR_MSG = "Message error"


class TaskMonitorTest(unittest.TestCase):
    def setUp(self):
        super(TaskMonitorTest, self).setUp()
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self.task_monitor = TaskMonitor(self.connection)

    @mock.patch.object(connection, 'get')
    def test_get_associated_resource_with_task(self, mock_get):

        task = {
            "category": "tasks",
            "type": "TaskResourceV2",
            "associatedResource": {
                "resourceUri": "/rest/associatedresourceuri"
            }}

        mock_get.return_value = {"resource": "resource1"}

        ret_task, entity = self.task_monitor.get_associated_resource(task.copy())

        self.assertEqual(entity, {"resource": "resource1"})
        self.assertEqual(ret_task, task)
        mock_get.assert_called_once_with("/rest/associatedresourceuri")

    @mock.patch.object(connection, 'get')
    def test_get_associated_resource_with_backup(self, mock_get):
        backup = {
            "category": "backups",
            "type": "BACKUP",
            "taskUri": "/rest/taskuri",
        }

        task = {
            "category": "TaskResourceV2",
            "type": "tasks",
            "uri": "/rest/justuri",
        }

        def inner_get(uri):
            if uri == "/rest/taskuri":
                return task.copy()
            else:
                return {"resource": "resource1"}

        mock_get.side_effect = inner_get
        mock_get.return_value = task.copy()

        ret_task, entity = self.task_monitor.get_associated_resource(backup.copy())

        self.assertEqual(entity, {"resource": "resource1"})
        self.assertEqual(ret_task, task)

    def test_get_associated_resource_support_dump(self):

        task = {
            "category": "tasks",
            "type": "TaskResourceV2",
            "associatedResource": {
                "resourceUri": "/rest/appliance/support-dumps/hennig59.eco-MyDump16-E-2016_07_07-17_53_42.867287.sdmp"
            }}

        ret_task, entity = self.task_monitor.get_associated_resource(task.copy())

        self.assertEqual(
            entity,
            "/rest/appliance/support-dumps/hennig59.eco-MyDump16-E-2016_07_07-17_53_42.867287.sdmp")
        self.assertEqual(ret_task, task)

    def test_get_associated_resource_with_task_empty(self):
        try:
            self.task_monitor.get_associated_resource({})
        except HPEOneViewUnknownType as e:
            self.assertEqual(MSG_INVALID_TASK, e.msg)
        else:
            self.fail()

    def test_get_associated_resource_with_invalid_task(self):
        try:
            self.task_monitor.get_associated_resource({"category": "networking"})
        except HPEOneViewUnknownType as e:
            self.assertEqual(MSG_UNKNOWN_OBJECT_TYPE, e.msg)
        else:
            self.fail()

    def test_get_associated_resource_with_invalid_type(self):
        try:
            self.task_monitor.get_associated_resource({"category": "tasks",
                                                       "type": "TaskResource"})
        except HPEOneViewInvalidResource as e:
            self.assertEqual(MSG_TASK_TYPE_UNRECONIZED % "TaskResource", e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running(self, mock_get):

        mock_get.return_value = {"uri": "uri",
                                 "taskState": "Pending"}

        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}))

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running_false(self, mock_get):
        mock_get.return_value = {"uri": "uri",
                                 "taskState": "Warning"}

        self.assertFalse(self.task_monitor.is_task_running({"uri": "uri"}))

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running_ignore_network_failure(self, mock_get):
        mock_get.side_effect = [{"uri": "uri",
                                 "taskState": "Pending"}, EnvironmentError(ETIMEDOUT, ERR_MSG)]

        connection_failure_control = dict(last_success=self.task_monitor.get_current_seconds())

        # 1. Success get
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, connection_failure_control))
        # 2. Timeout error, expected True anyway
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, connection_failure_control))

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running_network_failure_without_timeout_control(self, mock_get):
        mock_get.side_effect = EnvironmentError(ETIMEDOUT, ERR_MSG)

        self.assertRaises(EnvironmentError, self.task_monitor.is_task_running, {"uri": "uri"})

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running_generic_failure_with_timeout_control(self, mock_get):
        mock_get.side_effect = Exception(ERR_MSG)

        connection_failure_control = dict(last_success=self.task_monitor.get_current_seconds())

        self.assertRaises(Exception, self.task_monitor.is_task_running, {"uri": "uri"}, connection_failure_control)

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running_ignore_network_failure_reset_count(self, mock_get):
        mock_get.side_effect = [{"uri": "uri",
                                 "taskState": "Pending"},
                                EnvironmentError(ECONNABORTED, ERR_MSG),
                                {"uri": "uri",
                                 "taskState": "Pending"},
                                EnvironmentError(ETIMEDOUT, ERR_MSG)
                                ]

        connection_failure_control = dict(last_success=self.task_monitor.get_current_seconds())

        # 1. Success get
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, connection_failure_control))
        # 2. Inside the timeout, must continue
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, connection_failure_control))
        # Force exceed the timeout
        seconds_to_decrement = TaskMonitor.CONNECTION_FAILURE_TIMEOUT + 10
        connection_failure_control['last_success'] -= seconds_to_decrement
        # 3. Success get (reset timeout)
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, connection_failure_control))
        # 4. Inside the timeout again, must continue
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, connection_failure_control))

    @mock.patch.object(TaskMonitor, 'get')
    def test_is_task_running_ignore_network_failure_exceed_timeout(self, mock_get):
        mock_get.side_effect = [{"uri": "uri",
                                 "taskState": "Pending"},
                                EnvironmentError(ECONNABORTED, ERR_MSG)
                                ]

        conn_failure_control = dict(last_success=self.task_monitor.get_current_seconds())

        # 1. Success get
        self.assertTrue(self.task_monitor.is_task_running({"uri": "uri"}, conn_failure_control))
        # Decrement last success to force exceed the timeout
        seconds_to_decrement = TaskMonitor.CONNECTION_FAILURE_TIMEOUT + 10
        conn_failure_control['last_success'] -= seconds_to_decrement
        # 2. Should fail, timeout exceeded
        self.assertRaises(EnvironmentError, self.task_monitor.is_task_running, {"uri": "uri"},
                          conn_failure_control)

    @mock.patch.object(TaskMonitor, 'is_task_running')
    def test_wait_for_task_timeout(self, mock_is_running):

        mock_is_running.return_value = True
        timeout = 2

        try:
            self.task_monitor.wait_for_task({"uri": "uri"}, timeout)
        except HPEOneViewTimeout as e:
            self.assertEqual(MSG_TIMEOUT % timeout, e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch('time.sleep')
    def test_wait_for_task_increasing_sleep(self, mock_sleep, mock_is_running):

        mock_is_running.return_value = True
        timeout = 0.1

        # should call sleep increasing 1 until 10
        calls = [call(1), call(2), call(3), call(4), call(5), call(6), call(7),
                 call(8), call(9), call(10), call(10), call(10)]

        try:
            self.task_monitor.wait_for_task({"uri": "uri"}, timeout)
        except HPEOneViewTimeout as e:
            mock_sleep.assert_has_calls(calls)
            self.assertEqual(MSG_TIMEOUT % timeout, e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_message(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                "taskErrors": [{"message": "Error Message"}]}

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPEOneViewTaskError as e:
            self.assertEqual("Error Message", e.msg)
            self.assertEqual(None, e.error_code)
        else:
            self.fail("Expected exception not raised")

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_message_and_error_code(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                "taskErrors": [{"message": "Error Message", "errorCode": "ProfileAlreadyExistsInServer"}]}

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPEOneViewTaskError as e:
            self.assertEqual("Error Message", e.msg)
            self.assertEqual("ProfileAlreadyExistsInServer", e.error_code)
        else:
            self.fail("Expected exception not raised")

    def test_wait_for_task_empty(self):
        try:
            self.task_monitor.wait_for_task({})
        except HPEOneViewUnknownType as e:
            self.assertEqual(MSG_INVALID_TASK, e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_empty(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                "taskStatus": "Failed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPEOneViewTaskError as e:
            self.assertEqual("Failed", e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_unknown(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPEOneViewTaskError as e:
            self.assertEqual(MSG_UNKNOWN_EXCEPTION, e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "update",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource": "resource1"}

        ret_entity = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(ret_entity, {"resource": "resource1"})

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_unexpected_result(self, mock_get, mock_is_running):
        task = {"uri": "uri",
                "type": "Undefined",
                "name": "Undefined",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task

        ret_entity = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(ret_entity, task.copy())

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_delete(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "Delete",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource": "resource1"}

        ret = self.task_monitor.wait_for_task(task.copy())

        # may return a different type
        self.assertEqual(True, ret)

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_remove(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "Remove",
                "taskState": "Removed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource": "resource1"}

        ret = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(True, ret)

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_remove_san_manager(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "Remove SAN manager",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource": "resource1"}

        ret = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(True, ret)

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_delete_server_hardware_type(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "Delete server hardware type",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource": "resource1"}

        ret = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(True, ret)

    @mock.patch.object(connection, 'get')
    def test_get(self, mock_get):
        self.task_monitor.get({"uri": "an uri"})
        mock_get.assert_called_once_with("an uri")

    @mock.patch.object(TaskMonitor, 'is_task_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_get_completed_task(self, mock_get, mock_is_running):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "Create unexpected zoning report'",
                "taskState": "Completed",
                "taskOutput": []
                }

        mock_is_running.return_value = False
        mock_get.return_value = task

        response = self.task_monitor.get_completed_task(task.copy())

        self.assertEqual(task, response)

    @mock.patch('time.time')
    def test_get_current_seconds(self, mock_time):
        mock_time.return_value = 120
        current_seconds = TaskMonitor.get_current_seconds()
        self.assertEqual(current_seconds, 120)
