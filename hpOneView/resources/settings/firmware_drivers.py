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


class FirmwareDrivers(Resource):
    """
    The firmware drivers resource managers provides REST APIs to retrieve the firmware bundle inventory data.

    Note: As per the API docs, 'type' field is not present in the firmware drivers POST call. 
          So default values are not added.

    """
    URI = '/rest/firmware-drivers'

    def __init__(self, connection, data=None):
        super(FirmwareDrivers, self).__init__(connection, data)

    def get_schema(self):
        """
        Generate the FirmwareBaseline json formatted schema.

        Return:
            JSON schema of firmware bundle
        """
        schema_uri = "{0}/schema".format(self.URI)
        return self._helper.do_get(schema_uri)
