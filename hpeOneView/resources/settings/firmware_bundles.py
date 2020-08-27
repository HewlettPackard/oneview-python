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


from hpeOneView.resources.resource import ResourceClient


class FirmwareBundles(object):
    """
    Firmware Bundles API client.

    """
    URI = '/rest/firmware-bundles'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def upload(self, file_path, timeout=-1):
        """
        Upload an SPP ISO image file or a hotfix file to the appliance.
        The API supports upload of one hotfix at a time into the system.
        For the successful upload of a hotfix, ensure its original name and extension are not altered.

        Args:
            file_path: Full path to firmware.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
          dict: Information about the updated firmware bundle.
        """
        return self._client.upload(file_path, timeout=timeout)
