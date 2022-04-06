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
from os.path import basename
import re

standard_library.install_aliases()


from hpeOneView.resources.resource import ResourceFileHandlerMixin, Resource
from hpeOneView.resources.settings.firmware_drivers import FirmwareDrivers


class FirmwareBundles(ResourceFileHandlerMixin, Resource):
    """
    The firmware-bundles resource provides REST APIs for uploading
    firmware ServicePack files or hotfixes to the CI appliance.
    """
    URI = '/rest/firmware-bundles'

    def __init__(self, connection, data=None):
        super(FirmwareBundles, self).__init__(connection, data)

    def upload_compsig(self, file_path, timeout=-1):
        """
        Upload a compsig file for Gen10 and above hotfixes to the appliance.
        The uploaded signature file name will be encoded to a URI safe value.
        The API supports upload of one compsig at a time into the system.
        For the successful upload of a compsig, ensure its original name and extension are not altered.

        Args:
            file_path: Full path to compsig file.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
          dict: Information about the added compsig file.
        """
        uri = self.URI + "/addCompsig"
        return super(FirmwareBundles, self).upload(file_path, uri, timeout)

    def get_by_name(self, name):
        """
        Retrieves the specified firmware bundle resource by name.

        Args:
            name: name of specified firmware bundle resource

        Return:
            dict: Get response of specified firmware bundle resource.
        """
        filename = re.sub(r'\.(\d)', r'_\1', basename(name))
        name = filename.split('.')[0]

        firmware = FirmwareDrivers(self._connection)
        return firmware.get_by_field('resourceId', name)
