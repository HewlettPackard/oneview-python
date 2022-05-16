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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


import logging
import time

from errno import ECONNABORTED, ETIMEDOUT, ENOEXEC, EINVAL, ENETUNREACH, ECONNRESET, ENETDOWN, ECONNREFUSED
from hpeOneView.exceptions import HPEOneViewInvalidResource, HPEOneViewTimeout, HPEOneViewTaskError, HPEOneViewUnknownType

TASK_PENDING_STATES = ['New', 'Starting', 'Pending', 'Running', 'Suspended', 'Stopping']
TASK_ERROR_STATES = ['Error', 'Warning', 'Terminated', 'Killed']
TASK_COMPLETED_STATES = ['Error', 'Warning', 'Completed', 'Terminated', 'Killed']

MSG_UNKNOWN_OBJECT_TYPE = 'Unknown object type'
MSG_TASK_TYPE_UNRECONIZED = "Task type: '%s' resource is not a recognized version"
MSG_UNKNOWN_EXCEPTION = 'Unknown Exception'
MSG_TIMEOUT = 'Waited %s seconds for task to complete, aborting'
MSG_INVALID_TASK = 'Invalid task was provided'

UNLIMITED_TIMEOUT = -1

logger = logging.getLogger(__name__)


class TaskMonitor(object):
    # Seconds to wait when a network failure occurs
    CONNECTION_FAILURE_TIMEOUT = 90

    # Known error numbers when the connection drops
    CONNECTION_FAILURE_ERROR_NUMBERS = [ENOEXEC, EINVAL, ENETUNREACH, ETIMEDOUT, ECONNRESET,
                                        ECONNABORTED, ENETUNREACH, ENETDOWN, ECONNREFUSED]

    def __init__(self, con):
        self._connection = con

    @staticmethod
    def get_current_seconds():
        return int(time.time())

    def wait_for_task(self, task, timeout=-1):
        """
        Wait for task execution and return associated resource.

        Args:
            task: task dict
            timeout: timeout in seconds

        Returns:
            Associated resource when creating or updating; True when deleting.
        """
        self.__wait_task_completion(task, timeout)

        task = self.get(task)

        logger.debug("Waiting for task. Percentage complete: " + str(task.get('computedPercentComplete')))
        logger.debug("Waiting for task. Task state: " + str(task.get('taskState')))

        task_response = self.__get_task_response(task)
        logger.debug('Task completed')
        return task_response

    def get_completed_task(self, task, timeout=-1):
        """
        Waits until the task is completed and returns the task resource.

        Args:
            task: TaskResource
            timeout: Timeout in seconds

        Returns:
            dict: TaskResource
        """
        self.__wait_task_completion(task, timeout)

        return self.get(task)

    def __wait_task_completion(self, task, timeout):
        if not task:
            raise HPEOneViewUnknownType(MSG_INVALID_TASK)

        logger.debug('Waiting for task completion...')

        # gets current cpu second for timeout
        start_time = self.get_current_seconds()
        connection_failure_control = dict(last_success=self.get_current_seconds())

        i = 0
        while self.is_task_running(task, connection_failure_control):
            # wait 1 to 10 seconds
            # the value increases to avoid flooding server with requests
            i = i + 1 if i < 10 else 10

            logger.debug("Waiting for task. Percentage complete: " + str(task.get('computedPercentComplete')))
            logger.debug("Waiting for task. Task state: " + str(task.get('taskState')))

            time.sleep(i)
            if (timeout != UNLIMITED_TIMEOUT) and (start_time + timeout < self.get_current_seconds()):
                raise HPEOneViewTimeout(MSG_TIMEOUT % str(timeout))

    def __get_task_response(self, task):
        deleted_states = ['Delete',
                          'Remove',
                          'Delete server hardware type',
                          'Remove SAN manager',
                          'Delete hypervisor cluster profile.']

        if task['taskState'] in TASK_ERROR_STATES and task['taskState'] != 'Warning':
            msg = None
            error_code = None
            if 'taskErrors' in task and len(task['taskErrors']) > 0:
                err = task['taskErrors'][0]
                if 'message' in err:
                    msg = err['message']

                error_code = err.get('errorCode')

            if msg:
                raise HPEOneViewTaskError(msg, error_code)
            elif 'taskStatus' in task and task['taskStatus']:
                raise HPEOneViewTaskError(task['taskStatus'], error_code)
            else:
                raise HPEOneViewTaskError(MSG_UNKNOWN_EXCEPTION, error_code)

        if 'name' in task and task['name'] in deleted_states:
            return True

        if 'type' in task and task['type'].startswith('Task'):
            # get associated resource when is not a delete task
            task, entity = self.get_associated_resource(task)
            return entity

        logger.warning('Task completed, unknown response: ' + str(task))
        return task

    def is_task_running(self, task, connection_failure_control=None):
        """
        Check if a task is running according to: TASK_PENDING_STATES ['New', 'Starting',
        'Pending', 'Running', 'Suspended', 'Stopping']

        Args:
            task (dict): OneView Task resource.
            connection_failure_control (dict):
                A dictionary instance that contains last_success for error tolerance control.

        Examples:

            >>> connection_failure_control = dict(last_success=int(time.time()))
            >>> while self.is_task_running(task, connection_failure_control):
            >>>     pass

        Returns:
            True when in TASK_PENDING_STATES; False when not.
        """
        if 'uri' in task:
            try:
                task = self.get(task)
                if connection_failure_control:
                    # Updates last success
                    connection_failure_control['last_success'] = self.get_current_seconds()
                if 'taskState' in task and task['taskState'] in TASK_PENDING_STATES:
                    return True

            except Exception as error:
                logger.error('; '.join(str(e) for e in error.args) + ' when waiting for the task: ' + str(task))

                if not connection_failure_control:
                    raise error

                if hasattr(error, 'errno') and error.errno in self.CONNECTION_FAILURE_ERROR_NUMBERS:
                    last_success = connection_failure_control['last_success']
                    if last_success + self.CONNECTION_FAILURE_TIMEOUT < self.get_current_seconds():
                        # Timeout reached
                        raise error
                    else:
                        # Return task is running when network instability occurs
                        return True
                else:
                    raise error

        return False

    def get(self, task):
        """
        Retrieve a task by its uri.

        Args:
            task: task dict, must have 'uri' key.

        Returns:
            task dict
        """

        task = self._connection.get(task['uri'])
        return task

    def get_associated_resource(self, task):
        """
        Retrieve a resource associated with a task.

        Args:
            task: task dict

        Returns:
            tuple: task (updated), the entity found (dict)
        """

        if not task:
            raise HPEOneViewUnknownType(MSG_INVALID_TASK)

        if task['category'] not in ['tasks', 'backups']:
            # it is an error if type is not in obj, so let the except flow
            raise HPEOneViewUnknownType(MSG_UNKNOWN_OBJECT_TYPE)

        if task['type'] in ['TaskResourceV2', 'TaskResourceV3']:
            resource_uri = task['associatedResource']['resourceUri']

            if resource_uri and resource_uri.startswith("/rest/appliance/support-dumps/"):
                # Specific for support dumps
                return task, resource_uri

        elif task['type'] == 'BACKUP':
            task = self._connection.get(task['taskUri'])
            resource_uri = task['uri']
        else:
            raise HPEOneViewInvalidResource(MSG_TASK_TYPE_UNRECONIZED % task['type'])

        entity = {}

        if resource_uri:
            entity = self._connection.get(resource_uri)

        return task, entity
