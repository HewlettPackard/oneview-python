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


from hpeOneView.resources.resource import Resource, ResourceSchemaMixin


class FirmwareDrivers(ResourceSchemaMixin, Resource):
    """
    The firmware drivers resource managers provides REST APIs to retrieve the firmware bundle inventory data.
    Note: As per the API docs, 'type' field is not present in the firmware drivers POST call. So default values are not added.
    """
    URI = '/rest/firmware-drivers'

    def __init__(self, connection, data=None):
        super(FirmwareDrivers, self).__init__(connection, data)

    def get_by_name(self, name, version=None):
        """
        Retrieves the specified firmware driver resource by name and version.

        Args:
            name: name of specified firmware driver resource
            version: version of specified firmware driver resource (optional)

        Return:
            dict: Get response of specified firmware driver resource.
        """
        results = super(FirmwareDrivers, self).get_all()

        # filter by name and version(optional)
        result = [item for item in results if item.get('name', "").lower() == name.lower()]
        if version:
            result = [item for item in result if str(item.get('version', "")).lower() == version.lower()]

        if result:
            data = result[0]
            new_resource = self.new(self._connection, data)
        else:
            new_resource = None
        return new_resource
