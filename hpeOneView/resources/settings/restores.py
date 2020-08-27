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

from hpeOneView.resources.resource import Resource


class Restores(Resource):
    """
    Restore API client for initiate a restore of an appliance and to get the status of the restore operation.
    """
    URI = '/rest/restores'

    DEFAULT_VALUES = {
        '800': {"type": "RESTORE"},
        '1000': {"type": "RESTOREV1000"},
        '1200': {"type": "RESTOREV1000"},
        '1600': {"type": "RESTOREV1000"}
    }

    def __init__(self, connection, data=None):
        super(Restores, self).__init__(connection, data)

    def get_failure(self):
        """
        Retrieves the result of an appliance restore operation after it has completed.

        The restore result remains valid until a user logs in. After a user logs in, the restore result will be reset.
        This rest request will return only the valid result after restore has completed and before a user logs in.

        Returns:
            dict: Restore Result
        """
        failure_uri = "{0}/failure".format(self.URI)
        return self._helper.do_get(failure_uri)

    def restore(self, resource, timeout=-1):
        """
        Starts a restore operation with the specified backup file. The backup must be uploaded to the appliance
        prior to running this command. Only one restore can run at a time.

        Args:
            resource (dict): Config to restore.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Restore.

        """
        return super(Restores, self).create(resource, timeout=timeout)
