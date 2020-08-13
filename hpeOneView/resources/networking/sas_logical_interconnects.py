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


from hpeOneView.resources.resource import Resource, ensure_resource_client, unavailable_method


class SasLogicalInterconnects(Resource):
    """
    SAS Logical Interconnects API client.

    """
    URI = '/rest/sas-logical-interconnects'

    def __init__(self, connection, data=None):
        super(SasLogicalInterconnects, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, fields='', filter='', query='', sort='', view=''):
        """
        Gets a list of SAS Logical Interconnects based on optional sorting and filtering and constrained by start and
        count parameters.

        Args:
            start:
                 The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                 first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceeds the total number
                of items.
            fields:
                 Specifies which fields should be returned in the result set.
            filter (list or str):
                 A general filter/query string to narrow the list of items returned. The default is no filter; all
                 resources are returned.
            query:
                 A general query string to narrow the list of resources returned. The default is no query (all
                 resources are returned).
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time, with the
                oldest entry first.
            view:
                 Returns a specific subset of the attributes of the resource or collection, by specifying the name of a
                 predefined view. The default view is expand (show all attributes of the resource and all elements of
                 collections of resources).

        Returns:
            list: A list of SAS logical interconnects.
        """
        return self._helper.get_all(start=start, count=count, filter=filter, query=query, sort=sort, view=view,
                                    fields=fields)

    @ensure_resource_client
    def update_firmware(self, firmware_information, force=False):
        """
        Installs firmware to the member interconnects of a SAS Logical Interconnect.

        Args:
            firmware_information: Options to install firmware to a SAS Logical Interconnect.
            force: If sets to true, the operation completes despite any problems with the network connectivy
              or the erros on the resource itself.
        Returns:
            dict: SAS Logical Interconnect Firmware.
        """
        firmware_uri = "{}/firmware".format(self.data["uri"])
        result = self._helper.update(firmware_information, firmware_uri, force=force)
        self.refresh()

        return result

    @ensure_resource_client
    def get_firmware(self):
        """
        Gets baseline firmware information for a SAS Logical Interconnect.

        Returns:
            dict: SAS Logical Interconnect Firmware.
        """
        firmware_uri = "{}/firmware".format(self.data["uri"])
        return self._helper.do_get(firmware_uri)

    def update_compliance_all(self, information, timeout=-1):
        """
        Returns SAS Logical Interconnects to a consistent state. The current SAS Logical Interconnect state is
        compared to the associated SAS Logical Interconnect group.

        Args:
            information: Can be either the resource ID or URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: SAS Logical Interconnect.
        """

        uri = self.URI + "/compliance"
        result = self._helper.update(information, uri, timeout=timeout)

        return result

    @ensure_resource_client
    def update_compliance(self, timeout=-1):
        """
        Returns a SAS Logical Interconnect to a consistent state. The current SAS Logical Interconnect state is
        compared to the associated SAS Logical Interconnect group.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: SAS Logical Interconnect.
        """
        uri = "{}/compliance".format(self.data["uri"])
        result = self._helper.update({}, uri, timeout=timeout)
        self.refresh()

        return result

    @ensure_resource_client
    def replace_drive_enclosure(self, information):
        """
        When a drive enclosure has been physically replaced, initiate the replacement operation that enables the
        new drive enclosure to take over as a replacement for the prior drive enclosure. The request requires
        specification of both the serial numbers of the original drive enclosure and its replacement to be provided.

        Args:
            information: Options to replace the drive enclosure.

        Returns:
            dict: SAS Logical Interconnect.
        """

        uri = "{}/replaceDriveEnclosure".format(self.data["uri"])
        result = self._helper.create(information, uri)
        self.refresh()

        return result

    @ensure_resource_client
    def update_configuration(self):
        """
        Asynchronously applies or re-applies the SAS Logical Interconnect configuration to all managed interconnects
        of a SAS Logical Interconnect.

        Returns:
            dict: SAS Logical Interconnect.
        """
        uri = "{}/configuration".format(self.data["uri"])
        result = self._helper.update({}, uri)
        self.refresh()

        return result

    def create(self):
        """Create method is not available"""
        unavailable_method()

    def delete(self):
        """Delete method is not available"""
        unavailable_method()

    def update(self):
        """update method is not available"""
        unavailable_method()
