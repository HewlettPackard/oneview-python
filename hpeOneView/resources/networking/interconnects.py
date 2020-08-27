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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import Resource, ResourcePatchMixin
from hpeOneView.resources.resource import merge_default_values


class Interconnects(ResourcePatchMixin, Resource):
    """
    Interconnects API client.

    """

    URI = '/rest/interconnects'

    def __init__(self, connection, data=None):
        super(Interconnects, self).__init__(connection, data)

    def get_statistics(self, port_name=''):
        """
        Gets the statistics from an interconnect.

        Args:
            port_name (str): A specific port name of an interconnect.

        Returns:
             dict: The statistics for the interconnect that matches id.
        """
        uri = "{}/statistics".format(self.data["uri"])

        if port_name:
            uri = uri + "/" + port_name

        return self._helper.do_get(uri)

    def get_subport_statistics(self, port_name, subport_number):
        """
        Gets the subport statistics on an interconnect.

        Args:
            port_name (str): A specific port name of an interconnect.
            subport_number (int): The subport.

        Returns:
             dict: The statistics for the interconnect that matches id, port_name, and subport_number.
        """
        uri = "{}/statistics/{}/subport/{}".format(self.data["uri"], port_name, subport_number)
        return self._helper.do_get(uri)

    def get_name_servers(self):
        """
        Gets the named servers for an interconnect.

        Returns:
             dict: the name servers for an interconnect.
        """

        uri = "{}/nameServers".format(self.data["uri"])
        return self._helper.do_get(uri)

    def update_port(self, port_information, timeout=-1):
        """
        Updates an interconnect port.

        Args:
            port_information (dict): object to update
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        uri = "{}/ports".format(self.data["uri"])
        return self._helper.update(port_information, uri, timeout=timeout)

    def update_ports(self, ports, timeout=-1):
        """
        Updates the interconnect ports.

        Args:
            ports (list): Ports to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        resources = merge_default_values(ports, {'type': 'port'})

        uri = "{}/update-ports".format(self.data["uri"])
        return self._helper.update(resources, uri, timeout=timeout)

    def reset_port_protection(self, timeout=-1):
        """
        Triggers a reset of port protection.

        Cause port protection to be reset on all the interconnects of the logical interconnect that matches ID.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        uri = "{}/resetportprotection".format(self.data["uri"])
        return self._helper.update_with_zero_body(uri, timeout)

    def get_ports(self, start=0, count=-1):
        """
        Gets all interconnect ports.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.

        Returns:
            list: All interconnect ports.
        """
        uri = "{}/ports".format(self.data["uri"])
        return self._helper.get_all(start, count, uri=uri)

    def get_port(self, port_id_or_uri):
        """
        Gets an interconnect port.

        Args:
            port_id_or_uri: The interconnect port id or uri.

        Returns:
            dict: The interconnect port.
        """
        uri = "{}/ports/{}".format(self.data["uri"], port_id_or_uri)
        return self._helper.do_get(uri)

    def get_pluggable_module_information(self):
        """
        Gets all the pluggable module information.

        Returns:
            array: dicts of the pluggable module information.
        """
        uri = "{}/pluggableModuleInformation".format(self.data["uri"])
        return self._helper.do_get(uri)

    def update_configuration(self, timeout=-1):
        """
        Reapplies the appliance's configuration on the interconnect. This includes running the same configure steps
        that were performed as part of the interconnect add by the enclosure.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Interconnect
        """
        uri = "{}/configuration".format(self.data["uri"])
        return self._helper.update_with_zero_body(uri, timeout=timeout)
