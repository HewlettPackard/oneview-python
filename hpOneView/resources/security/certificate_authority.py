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

from hpOneView.resources.resource import ResourceClient


class CertificateAuthority(object):
    """
    Certificate Authority API client.
    """

    URI = '/rest/certificates/ca'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get(self):
        """
        Retrieves the certificate of the internal CA in the form of a string.

        Returns:
            str: The Internal CA Certificate.
        """
        return self._client.get(self.URI)

    def get_crl(self):
        """
        Retrieves the contents of the CRL file maintained by the internal CA; in Base-64 encoded format, in the form
        of a string.

        Returns:
            str: The Certificate Revocation List
        """
        crl_url = self.URI + "/crl"
        return self._client.get(crl_url)

    def delete(self, alias_name, timeout=-1):
        """
        Revokes a certificate signed by the internal CA. If client certificate to be revoked is RabbitMQ_readonly,
        then the internal CA root certificate, RabbitMQ client certificate and RabbitMQ server certificate will be
        regenerated. This will invalidate the previous version of RabbitMQ client certificate and the RabbitMQ server
        will be restarted to read the latest certificates.

        Args:
            alias_name (str): Alias name.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.
        """
        uri = self.URI + "/" + alias_name
        return self._client.delete(uri, timeout=timeout)
