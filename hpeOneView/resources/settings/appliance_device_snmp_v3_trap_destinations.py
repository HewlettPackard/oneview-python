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


class ApplianceDeviceSNMPv3TrapDestinations(Resource):
    """
    ApplianceDeviceSNMPv3TrapDestinations API client.
    The appliance has the ability to forward events received from monitored or managed server hardware to the specified destinations as SNMPv3 traps.
    """
    URI = '/rest/appliance/snmpv3-trap-forwarding/destinations'

    def __init__(self, connection, data=None):
        super(ApplianceDeviceSNMPv3TrapDestinations, self).__init__(connection, data)

    def create_validation(self, destination_address, existing_destinations=None, timeout=-1):
        """
        Validate whether a host name or IP address is valid and does not already exist.
        Supplying invalid destination address results in failure.

        Args:
            destination_address (str): destination ip address.
            existing_destinations (list) - An array of IP address or host name of the existing trap destinations.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Return:
            Returns error message if provides invalid destination address.

        """
        data = dict(
            destinationAddress=destination_address
        )

        if existing_destinations:
            data['existingDestinations'] = existing_destinations

        validation_uri = "{}/validation".format(self.URI)
        return self._helper.create(data, uri=validation_uri, timeout=timeout)

    def create(self, data, timeout=-1):
        """
        Creates a new SNMPv3 trap forwarding destination.
        Traps will be forwarded to this destination only if the SNMPv3 user is associated with it.
        Only one user can be assigned to a destination at any time.

        Args:
            data (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Return:
            dict: Created resource.

        """
        existing_destinations = data.pop('existingDestinations', None)
        self.create_validation(data['destinationAddress'], existing_destinations)
        return super(ApplianceDeviceSNMPv3TrapDestinations, self).create(data, uri=self.URI, timeout=timeout)

    def get_by_name(self, destination_address):
        """Retrieves a resource by its DestinationAddress.

        Args:
            destination_address: Resource DestinationAddress.

        Returns:
            Resource object or None if resource does not exist.
        """
        return super(ApplianceDeviceSNMPv3TrapDestinations, self).get_by_field('destinationAddress', destination_address)

    def get_all(self, start=0, count=-1, filter='', sort='', query=''):
        """
        Retrieves all SNMPv3 trap forwarding destinations.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.

                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            query:
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.

        Returns:
            list: A list of SNMPv3 Trap Destionations.
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort, query=query)
