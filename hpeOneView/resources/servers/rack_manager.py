# -*- coding: utf-8 -*-
###
# (C) Copyright [2022] Hewlett Packard Enterprise Development LP
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


from hpeOneView.resources.resource import Resource, ResourcePatchMixin, ensure_resource_client


class RackManager(ResourcePatchMixin, Resource):
    """
    The rack manager resource provides methods for managing one or more rack managers and its components.

    """

    URI = '/rest/rack-managers'

    def __init__(self, connection, data=None):
        super(RackManager, self).__init__(connection, data)

    def add(self, information, timeout=-1):
        """
        Adds a rack manager for management by the appliance.

        Args:
            information (dict): Object to create
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created Rack Manager
        """
        return self.create(information, timeout=timeout)

    def get_all_chassis(self):
        """
        Gets the list of chassis from all rack managers.

        Returns: List of Chassis
        """
        uri = self.URI + "/chassis"
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_associated_chassis(self):
        """
        Gets the list of chassis that are part of a rack manager.

        Returns: List of Chassis
        """
        uri = "{}/chassis".format(self.data["uri"])
        return self._helper.do_get(uri)

    def get_a_specific_resource(self, uri):
        """
        Gets a specific resource that is part of a rack manager.

        Returns:
            dict: Resource
        """
        return self._helper.do_get(uri)

    def get_all_managers(self):
        """
        Gets the list of manager resources from all rack managers.

        Returns: list of managers
        """
        uri = self.URI + "/managers"
        return self._helper.do_get(uri)

    def get_all_partitions(self):
        """
        Gets the list of partition resources from all rack managers.

        Returns: List of partitions
        """
        uri = self.URI + "/partitions"
        return self._helper.do_get(uri)

    def remove(self, force=False, timeout=-1):
        """
        Removes the rack manager with the specified URI.
        Note: This operation is only supported on appliances that support rack managers.

        Args:
            force (bool):
                If set to true, the operation completes despite any problems with
                network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates whether the resource was successfully removed.
        """
        return self.delete(force=force, timeout=timeout)

    @ensure_resource_client
    def get_environmental_configuration(self):
        """
        Gets the environmental configuration of a rack manager.

        Returns:
            dict: Environmental confifuration
        """
        uri = "{}/environmentalConfiguration".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_associated_managers(self):
        """
        Gets the list of managers that are part of a rack manager.

        Returns: List of Managers
        """
        uri = "{}/managers".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_associated_partitions(self):
        """
        Gets the list of partitions that are part of a rack manager.

        Returns: List of Partitions
        """
        uri = "{}/partitions".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_remote_support_settings(self):
        """
        Gets the remote support settings of a rack manager.

        Returns:
            dict: Environmental confifuration
        """
        uri = "{}/remoteSupportSettings".format(self.data["uri"])
        return self._helper.do_get(uri)
