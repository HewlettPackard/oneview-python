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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import Resource


class ApplianceNetworkInterfaces(Resource):
    """
    ApplianceNetworkInterface API Client.

    """
    URI = '/rest/appliance/network-interfaces'

    def __init__(self, connection, data=None):
        super(ApplianceNetworkInterfaces, self).__init__(connection, data)

    def get_all(self):
        return super(ApplianceNetworkInterfaces, self).get_by_uri(self.URI)

    def get_all_mac_address(self):
        """
        Gets unconfigured network interfaces on the appliance.
        Returns:
            dict: Unconfigured network interfaces on the appliance.
        """
        uri = self._helper.build_uri('mac-addresses')
        mac_addresses = super(ApplianceNetworkInterfaces, self).get_by_uri(uri)
        return mac_addresses.data['members']

    def get_by_mac_address(self, mac_address):
        """
        Gets the network interface by the macAddress.
        Returns:
            dict: Network interface with the given macAddress on the appliance.
        """

        resources = self.get_all().data["applianceNetworks"]
        for resource in resources:
            if resource['macAddress'].lower() == mac_address.lower():
                new_resource = self.new(self._connection, resource)
            else:
                new_resource = None
        return new_resource
