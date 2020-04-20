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


from hpOneView.resources.resource import Resource


class ApplianceDeviceSNMPv1TrapDestinations(Resource):
    """
    ApplianceDeviceSNMPv1TrapDestinations API client.

    The appliance has the ability to forward events received from monitored or managed
    server hardware to the specified destinations as SNMPv1 traps.
    """
    URI = '/rest/appliance/trap-destinations'

    def __init__(self, connection, data=None):
        super(ApplianceDeviceSNMPv1TrapDestinations, self).__init__(connection, data)

    def get_by_id(self, id):
        """
        Retrieves the trap destination based on the id specified.

        Args:
            id (int): id of the snmp_v1 trap resource

        Return:
            dict: SNMPv1 trap destination

        """
        uri = "{0}/{1}".format(self.URI, id)
        return self._helper.do_get(uri)


    def create_validation(self, data=None, timeout=-1):
        """
        Validate whether a hostname or ip address is a valid trap destination.
        If validation fails, it returns an error identifying the problem that occurred.

        Args:
            data (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Return:
            None if successful, else returns error message.

        """
        validation_uri = "{}/validation".format(self.URI)
        return super(ApplianceDeviceSNMPv1TrapDestinations, self).create(data, uri=validation_uri, timeout=timeout)

    def create(self, data=None, id=None, timeout=-1):
        """
        Adds the specified trap forwarding destination.
        The trap destination associated with the specified id will be created if trap destination with that id does not exists.
        The id can only be an integer greater than 0.

        Args:
            data (dict): Object to create.
            id: id of the resource to be created
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Return:
            dict: Created resource.

        """
        if not id:
            available_id = self.__get_first_available_id()
            uri = '{}/{}'.format(self.URI, available_id)
        else:
            uri = '{}/{}'.format(self.URI, id)
        return super(ApplianceDeviceSNMPv1TrapDestinations, self).create(data, uri=uri, timeout=timeout)

    def __findFirstMissing(self, array, start, end):
        """
        Find the smallest elements missing in a sorted array.

        Args:
            array - list if ids
            start - starting index
            end - ending index

        Returns:
            int: The smallest element missing.
        """
        if (start > end):
            return end + 1

        if (start != array[start]):
            return start

        mid = int((start + end) / 2)

        if (array[mid] == mid):
            return self.__findFirstMissing(array, mid + 1, end)

        return self.__findFirstMissing(array, start, mid)

    def __get_first_available_id(self):
        """
        Private method to get the first available id.
        The id can only be an integer greater than 0.

        Returns:
            int: The first available id
        """
        traps = super(ApplianceDeviceSNMPv1TrapDestinations, self).get_all()
        if traps:
            used_ids = [0]
            for trap in traps:
                used_uris = trap.get('uri')
                used_ids.append(int(used_uris.split('/')[-1]))
            used_ids.sort()
            return self.__findFirstMissing(used_ids, 0, len(used_ids) - 1)
        else:
            return 1
