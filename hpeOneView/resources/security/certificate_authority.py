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


class CertificateAuthority(Resource):
    """
    Certificate Authority API client.
    """

    URI = '/rest/certificates/ca'

    def __init__(self, connection, data=None):
        super(CertificateAuthority, self).__init__(connection, data)

    def create(self, data=None, parent_task='', timeout=-1):
        """
        Imports an external CA root certificate or CA certificate chain into the appliance trust store.
        Same CA certificate will not be allowed to be imported into the appliance trust store.

        Args:
            data: Fields passed to create the resource.
            parent_task: The parentTask can be passed only if auth header has either a valid trusted token
                         or a valid combined token consisting of a trusted token.
            timeout: Timeout in seconds. Wait for task completion by default.

        Returns:
            dict: response body of imported CA Certificate.
        """
        if parent_task:
            uri_create = "{}?parentTask={}".format(self.URI, parent_task)
        else:
            uri_create = self.URI

        return super(CertificateAuthority, self).create(data, uri=uri_create, timeout=timeout)

    def get_all(self, filter='', cert_details=True):
        """
        Retrieves all the CA certificates.

        Args:
            filter: Filter based on a specific value. Supported filter is filter=certType:INTERNAL
            cert_details: If this is set to true the api returns all the CA certificates with full certificate details

        Returns:
            list: List of all CA Certificate.
        """
        custom_headers = {'If-Req-CertDetails': cert_details}
        return self._helper.get_all(filter=filter, custom_headers=custom_headers)

    def get_crl(self):
        """
        Retrieves the contents of the CRL file maintained by the internal CA; in Base-64 encoded format, in the form
        of a string.

        Returns:
            str: The Certificate Revocation List
        """
        uri_crl = self.URI + "/crl"
        return super(CertificateAuthority, self).get_by_uri(uri_crl)

    def get_by_aliasname(self, alias_name):
        """
        Returns the collection having CA certificates

        Args:
            alias_name: alias name of CA certificate

        Returns:
            dict: The Certificate details by certificate authority alias name
        """
        uri = "{}/{}".format(self.URI, alias_name)
        return super(CertificateAuthority, self).get_by_uri(uri)

    def get_crl_by_aliasname(self, alias_name):
        """
        Downloads the CRL file associated with the given certificate authority alias name.

        Args:
            alias_name: alias name of CA certificate

        Returns:
            str: The Certificate Revocation List by certificate authority alias name
        """
        uri = "{}/{}/crl".format(self.URI, alias_name)
        return super(CertificateAuthority, self).get_by_uri(uri)
