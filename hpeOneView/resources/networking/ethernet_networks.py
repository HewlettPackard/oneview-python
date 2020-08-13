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


from hpeOneView.resources.resource import (Resource, ResourcePatchMixin,
                                           ensure_resource_client)


class EthernetNetworks(ResourcePatchMixin, Resource):
    """
    Ethernet Networks API client.

    """
    URI = '/rest/ethernet-networks'

    DEFAULT_VALUES = {
        '200': {"type": "ethernet-networkV3"},
        '300': {"type": "ethernet-networkV300"},
        '500': {"type": "ethernet-networkV300"},
        '600': {"type": "ethernet-networkV4"},
        '800': {"type": "ethernet-networkV4"},
        '1000': {"type": "ethernet-networkV4"},
        '1200': {"type": "ethernet-networkV4"},
        '1600': {"type": "ethernet-networkV4"},
        '1800': {"type": "ethernet-networkV4"}

    }
    BULK_DEFAULT_VALUES = {
        '200': {"type": "bulk-ethernet-network"},
        '300': {"type": "bulk-ethernet-network"},
        '500': {"type": "bulk-ethernet-network"},
        '600': {"type": "bulk-ethernet-networkV1"},
        '800': {"type": "bulk-ethernet-networkV1"},
        '1000': {"type": "bulk-ethernet-networkV1"},
        '1200': {"type": "bulk-ethernet-networkV2"},
        '1600': {"type": "bulk-ethernet-networkV2"},
        '1800': {"type": "bulk-ethernet-networkV2"}

    }

    def __init__(self, connection, data=None):
        super(EthernetNetworks, self).__init__(connection, data)

    def create_bulk(self, resource, timeout=-1):
        """
        Creates bulk Ethernet networks.

        Args:
            resource (dict): Specifications to create in bulk.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            list: List of created Ethernet Networks.

        """
        uri = self.URI + '/bulk'
        default_values = self._get_default_values(self.BULK_DEFAULT_VALUES)
        updated_data = self._helper.update_resource_fields(resource, default_values)

        self._helper.create(updated_data, uri=uri, timeout=timeout)

        return self.get_range(resource['namePrefix'], resource['vlanIdRange'])

    def get_range(self, name_prefix, vlan_id_range):
        """
        Gets a list of Ethernet Networks that match the 'given name_prefix' and the 'vlan_id_range'.

        Examples:
            >>> enet.get_range('Enet_name', '1-2,5')
                # The result contains the ethernet network with names:
                ['Enet_name_1', 'Enet_name_2', 'Enet_name_5']

            >>> enet.get_range('Enet_name', '2')
                # The result contains the ethernet network with names:
                ['Enet_name_1', 'Enet_name_2']

        Args:
            name_prefix: The Ethernet Network prefix
            vlan_id_range: A combination of values or ranges to be retrieved. For example, '1-10,50,51,500-700'.

        Returns:
            list: A list of Ethernet Networks.

        """
        filter = '"\'name\' matches \'{}\_%\'"'.format(name_prefix)
        ethernet_networks = self.get_all(filter=filter, sort='vlanId:ascending')

        vlan_ids = self.dissociate_values_or_ranges(vlan_id_range)

        for net in ethernet_networks[:]:
            if int(net['vlanId']) not in vlan_ids:
                ethernet_networks.remove(net)
        return ethernet_networks

    def dissociate_values_or_ranges(self, vlan_id_range):
        """
        Build a list of vlan ids given a combination of ranges and/or values

        Examples:
            >>> enet.dissociate_values_or_ranges('1-2,5')
                [1, 2, 5]

            >>> enet.dissociate_values_or_ranges('5')
                [1, 2, 3, 4, 5]

            >>> enet.dissociate_values_or_ranges('4-5,7-8')
                [4, 5, 7, 8]

        Args:
            vlan_id_range: A combination of values or ranges. For example, '1-10,50,51,500-700'.

        Returns:
            list: vlan ids
        """
        values_or_ranges = vlan_id_range.split(',')
        vlan_ids = []
        # The expected result is different if the vlan_id_range contains only one value
        if len(values_or_ranges) == 1 and '-' not in values_or_ranges[0]:
            vlan_ids = list(range(1, int(values_or_ranges[0]) + 1))
        else:
            for value_or_range in values_or_ranges:
                value_or_range.strip()
                if '-' not in value_or_range:
                    vlan_ids.append(int(value_or_range))
                else:
                    start, end = value_or_range.split('-')
                    range_ids = range(int(start), int(end) + 1)
                    vlan_ids.extend(range_ids)

        return vlan_ids

    @ensure_resource_client
    def get_associated_profiles(self):
        """
        Gets the URIs of profiles which are using an Ethernet network.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            list: URIs of the associated profiles.

        """
        uri = "{}/associatedProfiles".format(self.data['uri'])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_associated_uplink_groups(self):
        """
        Gets the uplink sets which are using an Ethernet network.

        Returns:
            list: URIs of the associated uplink sets.

        """
        uri = "{}/associatedUplinkGroups".format(self.data['uri'])
        return self._helper.do_get(uri)

    def delete_bulk(self, resource, timeout=-1):
        """
        Deletes bulk Ethernet networks.

        Args:
            resource (dict): Specifications to delete in bulk.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        """
        uri = self.URI + '/bulk-delete'

        return self._helper.create(resource, uri=uri, timeout=timeout)
