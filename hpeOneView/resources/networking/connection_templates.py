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


from hpeOneView.resources.resource import Resource


class ConnectionTemplates(Resource):
    """
    Connection Templates API client.

    """
    URI = '/rest/connection-templates'

    def __init__(self, connection, data=None):
        super(ConnectionTemplates, self).__init__(connection, data)
        self.__default_values = {
            'type': 'connection-template'
        }

    def get_default(self):
        """
        Gets the default network connection template. This is the default connection template used
        for construction of networks. Its value is copied when a new connection template is made.

        Returns:
            dict:
        """
        uri = self.URI + "/defaultConnectionTemplate"
        return self._helper.do_get(uri)
