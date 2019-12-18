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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import Resource


class DeploymentPlans(Resource):
    URI = '/rest/deployment-plans'

    def __init__(self, connection, data=None):
        super(DeploymentPlans, self).__init__(connection, data)
        self.__default_values = {
            'type': 'OEDeploymentPlan',
        }

    def create(self, resource, timeout=-1):
        """
        Adds a Deployment Plan based on the attributes specified.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Created Deployment plan.

        """
        data = self.__default_values.copy()
        data.update(resource)

        return super(DeploymentPlans, self).create(data, timeout=timeout)

    def get_osdp(self):
        """
        Retrieves facts about Server Profiles and Server Profile Templates that are using Deployment Plan based on the ID or URI provided.

        Returns:
            dict: Server Profiles and Server Profile Templates
        """
        uri = "{}/osdp".format(self.data["uri"])
        return self._helper.do_get(uri)

    def get_usedby(self):
        """
        Retrieves the OS deployment plan details from OneView for a deployment plan resource based on the ID or URI provided.

        Returns:
            dict: The OS Deployment Plan.
        """
        uri = "{}/usedby".format(self.data["uri"])
        return self._helper.do_get(uri)
