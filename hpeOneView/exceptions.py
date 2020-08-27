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


from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

import logging
import traceback
from past.builtins import basestring

logger = logging.getLogger(__name__)


def handle_exceptions(exception_type, exception_value, exception_traceback, logger=logger):
    message = __get_message(exception_value, exception_type)

    logger.error("Uncaught Exception: %s with message: %s" % (exception_type.__name__, message))
    traceback.print_exception(exception_type, exception_value, exception_traceback)


def __get_message(exception_value, exception_type):
    message = ""

    if issubclass(exception_type, HPEOneViewException):
        if exception_value.msg:
            message = exception_value.msg
        if exception_value.oneview_response:
            message += "\n" + str(exception_value.oneview_response)
    elif len(exception_value.args) > 0:
        message = exception_value.args[0]

    return message


class HPEOneViewException(Exception):
    """
    OneView base Exception.

    Attributes:
       msg (str): Exception message.
       oneview_response (dict): OneView rest response.
   """

    def __init__(self, data, error=None):
        self.msg = None
        self.oneview_response = None

        if isinstance(data, basestring):
            self.msg = data
        else:
            self.oneview_response = data

            if data and isinstance(data, dict):
                self.msg = data.get('message')

        if self.oneview_response:
            Exception.__init__(self, self.msg, self.oneview_response)
        else:
            Exception.__init__(self, self.msg)


class HPEOneViewInvalidResource(HPEOneViewException):
    """
    OneView Invalid Resource Exception.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPEOneViewTaskError(HPEOneViewException):
    """
    OneView Task Error Exception.

    Attributes:
       msg (str): Exception message.
       error_code (str): A code which uniquely identifies the specific error.
    """

    def __init__(self, msg, error_code=None):
        super(HPEOneViewTaskError, self).__init__(msg)
        self.error_code = error_code


class HPEOneViewUnknownType(HPEOneViewException):
    """
    OneView Unknown Type Error.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPEOneViewTimeout(HPEOneViewException):
    """
    OneView Timeout Exception.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPEOneViewValueError(HPEOneViewException):
    """
    OneView Value Error.
    The exception is raised when the data contains an inappropriate value.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPEOneViewResourceNotFound(HPEOneViewException):
    """
    OneView Resource Not Found Exception.
    The exception is raised when an associated resource was not found.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPEOneViewUnavailableMethod(HPEOneViewException):
    """
    OneView Unavailable Method Exception.
    The exception is raised when a method is not available for the resource class.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPEOneViewMissingUniqueIdentifiers(HPEOneViewException):
    """
    OneView Missing Unique Identifiers Exception.
    The exception is raised when unique identifiers are missing for the resource

    Attributes:
       msg (str): Exception message.
    """
    pass
