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


from hpeOneView.resources.resource import (Resource, ResourcePatchMixin, ensure_resource_client)


class SasLogicalJbods(Resource, ResourcePatchMixin):
    """
    SAS Logical JBODs API client.

    Note:
        This resource is only available on HPE Synergy

    """
    URI = '/rest/sas-logical-jbods'

    def __init__(self, connection, data=None):
        super(SasLogicalJbods, self).__init__(connection, data)

    @ensure_resource_client
    def get_drives(self):
        """
        Gets the list of drives allocated to this SAS logical JBOD.

        Args:
            id_or_uri: Can be either the SAS logical JBOD ID or the SAS logical JBOD URI.

        Returns:
            list: A list of Drives
        """
        uri = "{}/drives".format(self.data['uri'])
        return self._helper.do_get(uri)
