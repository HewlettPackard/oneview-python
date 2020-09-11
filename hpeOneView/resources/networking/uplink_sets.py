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


from hpeOneView.resources.resource import Resource, ensure_resource_client
from hpeOneView.resources.networking.ethernet_networks import EthernetNetworks
from hpeOneView.exceptions import HPEOneViewResourceNotFound
from builtins import isinstance


class UplinkSets(Resource):
    """
    Uplink Sets API client.

    """
    URI = '/rest/uplink-sets'

    DEFAULT_VALUES = {
        '200': {"type": "uplink-setV3"},
        '300': {"type": "uplink-setV300"},
        '500': {"type": "uplink-setV300"},
        '600': {"type": "uplink-setV4"},
        '800': {"type": "uplink-setV4"},
        '1000': {"type": "uplink-setV5"},
        '1200': {"type": "uplink-setV6"},
        '1600': {"type": "uplink-setV7"},
        '1800': {"type": "uplink-setV7"}
    }

    def __init__(self, connection, data=None):
        super(UplinkSets, self).__init__(connection, data)
        self._ethernet_networks = EthernetNetworks(connection)

    @ensure_resource_client
    def get_ethernet_networks(self):
        """
        Gets a list of associated ethernet networks of an uplink set.

        Args:
            id_or_uri: Can be either the uplink set id or the uplink set uri.

        Returns:
            list: Associated ethernet networks.
        """
        network_uris = self.data.get('networkUris')
        networks = []
        if network_uris:
            for uri in network_uris:
                networks.append(self._ethernet_networks.get_by_uri(uri))
        return networks

    @ensure_resource_client
    def add_ethernet_networks(self, ethernet_names):
        """
        Adds existing ethernet networks to an uplink set.

        Args:
            id_or_uri:
                Can be either the uplink set id or the uplink set uri.
            ethernet_name:
                Could be either one or more ethernet network names.
        Returns:
            dict: The updated uplink set.
        """
        self.__set_ethernet_uris(ethernet_names, operation="add")
        return self.data

    @ensure_resource_client
    def remove_ethernet_networks(self, ethernet_names):
        """
        Remove existing ethernet networks of an uplink set.

        Args:
            id_or_uri:
                Can be either the uplink set id or the uplink set uri.
            ethernet_id_or_uris:
                Could be either one or more ethernet network id or ethernet network uri.

        Returns:
            dict: The updated uplink set.
        """
        self.__set_ethernet_uris(ethernet_names, operation="remove")
        return self.data

    def __set_ethernet_uris(self, ethernet_names, operation="add"):
        """Updates network uris."""
        if not isinstance(ethernet_names, list):
            ethernet_names = [ethernet_names]

        associated_enets = self.data.get('networkUris', [])
        ethernet_uris = []

        for i, enet in enumerate(ethernet_names):
            enet_exists = self._ethernet_networks.get_by_name(enet)
            if enet_exists:
                ethernet_uris.append(enet_exists.data['uri'])
            else:
                raise HPEOneViewResourceNotFound("Ethernet: {} does not exist".foramt(enet))

        if operation == "remove":
            enets_to_update = sorted(list(set(associated_enets) - set(ethernet_uris)))
        elif operation == "add":
            enets_to_update = sorted(list(set(associated_enets).union(set(ethernet_uris))))
        else:
            raise ValueError("Value {} is not supported as operation. The supported values are: ['add', 'remove']")

        if set(enets_to_update) != set(associated_enets):
            updated_network = {'networkUris': enets_to_update}
            self.update(updated_network)
