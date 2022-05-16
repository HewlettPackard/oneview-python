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


class ApplianceDeviceSNMPv3Users(Resource):
    """
    ApplianceDeviceSNMPv3Users API client [Available only since API 600].

    As part of SNMPv3 trap forwarding support, the appliance provides APIs for creating User-based Security Model (USM) and forwarding destinations.
    The following protocols are supported while defining USM.

    Authentication protocols: MD5 / SHA1 / SHA256 / SHA384 / SHA512
    Privacy protocols: AES / DES
    The security levels supported while defining USM are None, Authentication only and both Authentication and Privacy.

    """
    URI = '/rest/appliance/snmpv3-trap-forwarding/users'

    def __init__(self, connection, data=None):
        super(ApplianceDeviceSNMPv3Users, self).__init__(connection, data)

    def get_by_name(self, user_name):
        """Retrieves a resource by its username.
        Args:
            username: Resource username
        Returns:
            Resource object or None if resource does not exist.
        """
        return super(ApplianceDeviceSNMPv3Users, self).get_by_field('userName', user_name)

    def get_all(self, start=0, count=-1, filter='', sort='', query=''):
        """
        Lists all SNMPv3 Users.
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

        Returns:
            list: A list of SNMPv3 Users.
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort, query=query)
