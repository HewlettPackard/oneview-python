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
import traceback
import unittest
import logging
import mock
import os
import tempfile
import pickle

from hpeOneView.exceptions import handle_exceptions
from hpeOneView.exceptions import HPEOneViewException
from hpeOneView.exceptions import HPEOneViewInvalidResource
from hpeOneView.exceptions import HPEOneViewUnknownType
from hpeOneView.exceptions import HPEOneViewTaskError
from hpeOneView.exceptions import HPEOneViewResourceNotFound
from hpeOneView.exceptions import HPEOneViewValueError


class ExceptionsTest(unittest.TestCase):
    def test_exception_constructor_with_string(self):
        exception = HPEOneViewException("A message string")

        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)

    def test_exception_constructor_with_valid_dict(self):
        exception = HPEOneViewException({'message': "A message string"})

        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, {'message': "A message string"})
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(exception.args[1], {'message': 'A message string'})

    def test_exception_constructor_with_invalid_dict(self):
        exception = HPEOneViewException({'msg': "A message string"})

        self.assertEqual(exception.msg, None)
        self.assertEqual(exception.oneview_response, {'msg': "A message string"})
        self.assertEqual(exception.args[0], None)
        self.assertEqual(exception.args[1], {'msg': "A message string"})

    def test_exception_constructor_with_invalid_type(self):
        exception = HPEOneViewException(['List, item 1', "List, item 2: A message string"])

        self.assertEqual(exception.msg, None)
        self.assertEqual(exception.oneview_response, ['List, item 1', "List, item 2: A message string"])
        self.assertEqual(exception.args[0], None)
        self.assertEqual(exception.args[1], ['List, item 1', "List, item 2: A message string"])

    def test_invalid_resource_exception_inheritance(self):
        exception = HPEOneViewInvalidResource({'message': "A message string"})

        self.assertIsInstance(exception, HPEOneViewException)
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, {'message': "A message string"})
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(exception.args[1], {'message': 'A message string'})

    def test_unknown_type_exception_inheritance_with_string(self):
        exception = HPEOneViewUnknownType("A message string")

        self.assertIsInstance(exception, HPEOneViewException)
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)

    def test_exception_constructor_with_unicode(self):
        exception = HPEOneViewException(u"A message string")

        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)

    def test_task_error_constructor_with_string(self):
        exception = HPEOneViewTaskError("A message string", 100)

        self.assertIsInstance(exception, HPEOneViewException)
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "A message string")
        self.assertEqual(len(exception.args), 1)
        self.assertEqual(exception.error_code, 100)

    def test_oneview_resource_not_found_inheritance(self):
        exception = HPEOneViewResourceNotFound("The resource was not found!")

        self.assertIsInstance(exception, HPEOneViewException)
        self.assertEqual(exception.msg, "The resource was not found!")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "The resource was not found!")

    def test_oneview_value_error_inheritance(self):
        exception = HPEOneViewValueError("The given data is empty!")

        self.assertIsInstance(exception, HPEOneViewException)
        self.assertEqual(exception.msg, "The given data is empty!")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "The given data is empty!")

    def test_pickle_HPEOneViewException_dict(self):
        message = {"msg": "test message"}
        exception = HPEOneViewException(message)
        tempf = tempfile.NamedTemporaryFile(delete=False)
        with tempf as f:
            pickle.dump(exception, f)

        with open(tempf.name, 'rb') as f:
            exception = pickle.load(f)

        os.remove(tempf.name)
        self.assertEqual('HPEOneViewException', exception.__class__.__name__)

    def test_pickle_HPEOneViewException_message(self):
        message = "test message"
        exception = HPEOneViewException(message)
        tempf = tempfile.NamedTemporaryFile(delete=False)
        with tempf as f:
            pickle.dump(exception, f)

        with open(tempf.name, 'rb') as f:
            exception = pickle.load(f)

        os.remove(tempf.name)
        self.assertEqual('HPEOneViewException', exception.__class__.__name__)

    @mock.patch.object(traceback, 'print_exception')
    @mock.patch.object(logging, 'error')
    def test_should_log_message(self, mock_logging_error, mock_traceback):
        message = "test message"
        exception = HPEOneViewException(message)
        traceback_ex = None
        handle_exceptions(exception.__class__, exception, traceback_ex, mock_logging_error)

        log_message = "Uncaught Exception: HPEOneViewException with message: test message"
        mock_logging_error.error.assert_called_once_with(log_message)

    @mock.patch.object(traceback, 'print_exception')
    @mock.patch.object(logging, 'error')
    def test_should_print_exception(self, mock_logging_error, mock_traceback):
        message = "test message"
        exception = HPEOneViewException(message)
        traceback_ex = None
        handle_exceptions(exception.__class__, exception, traceback_ex, mock_logging_error)

        mock_traceback.assert_called_once_with(exception.__class__, exception, traceback_ex)

    @mock.patch.object(traceback, 'print_exception')
    @mock.patch.object(logging, 'error')
    def test_should_log_oneview_reponse(self, mock_logging_error, mock_traceback):
        message = {"msg": "test message"}
        exception = HPEOneViewException(message)
        traceback_ex = None
        handle_exceptions(exception.__class__, exception, traceback_ex, mock_logging_error)

        log_message = "Uncaught Exception: HPEOneViewException with message: \n{'msg': 'test message'}"
        mock_logging_error.error.assert_called_once_with(log_message)

    @mock.patch.object(traceback, 'print_exception')
    @mock.patch.object(logging, 'error')
    def test_should_log_python_exception(self, mock_logging_error, mock_traceback):
        message = "test message"
        exception = Exception(message)
        traceback_ex = None
        handle_exceptions(exception.__class__, exception, traceback_ex, mock_logging_error)

        log_message = "Uncaught Exception: Exception with message: test message"
        mock_logging_error.error.assert_called_once_with(log_message)
