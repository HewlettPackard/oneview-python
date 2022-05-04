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
from hpeOneView.exceptions import HPEOneViewException


class CertificatesServer(Resource):
    """
    The Certificates Servers resource provides REST APIs for configuration of device or
    server certificates for the appliance to establish SSL communication with other managed network entities.

    Import, Update and Delete APIs are asynchronous and GET API is synchronous.

    """
    URI = '/rest/certificates'

    def __init__(self, connection, data=None):
        super(CertificatesServer, self).__init__(connection, data)
        self.__default_values = {
            'type': 'CertificateInfoV2'
        }

    def create(self, data=None, timeout=-1):
        """
        Makes a POST request to create a server certificate resource.

        Args:
            data: Fields passed to create the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Return:
            Created certificate resource.
        """
        uri_create = "{}/servers".format(self.URI)
        return super(CertificatesServer, self).create(data, uri=uri_create, timeout=timeout)

    def get_remote(self, remote_address):
        """
        Retrieves the device or server certificate and certificate chain of the specified device or server.

        Args:
            remote_address:
                Address of remote server

        Return:
             dict: Certificate chain of remote server
        """
        uri = "{0}/https/remote/{1}".format(self.URI, remote_address)
        return super(CertificatesServer, self).get_by_uri(uri=uri)

    def get_by_alias_name(self, alias_name):
        """
        Retrieves the device or server certificate, already trusted in the appliance,
        with the specified aliasName.

        Args:
            alias_name (str): Alias name.

        Return:
            dict: Certificate of trusted appliance
        """
        uri = "{0}/servers/{1}".format(self.URI, alias_name)
        try:
            response = super(CertificatesServer, self).get_by_uri(uri=uri)
        except HPEOneViewException:
            response = None
        return response
