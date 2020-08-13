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


class CertificateRabbitMQ(object):
    URI = '/rest/certificates/client/rabbitmq'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def generate(self, information, timeout=-1):
        """
        Generates a self signed certificate or an internal CA signed certificate for RabbitMQ clients.

        Args:
            information (dict): Information to generate the certificate for RabbitMQ clients.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: RabbitMQ certificate generated
        """
        return self._client.create(information, timeout=timeout)

    def get(self, alias_name):
        """
        Retrieves the base-64 encoded certificate associated with the RabbitMQ user.

        Args:
            alias_name: Key pair associated with the RabbitMQ

        Returns:
            dict: RabbitMQ certificate
        """
        return self._client.get(alias_name)

    def get_key_pair(self, alias_name):
        """
        Retrieves the public and private key pair associated with the specified alias name.

        Args:
            alias_name: Key pair associated with the RabbitMQ

        Returns:
            dict: RabbitMQ certificate
        """
        uri = self.URI + "/keypair/" + alias_name
        return self._client.get(uri)

    def get_keys(self, alias_name, key_format):
        """
        Retrieves the contents of PKCS12 file in the format specified.
        This PKCS12 formatted file contains both the certificate as well as the key file data.
        Valid key formats are Base64 and PKCS12.

        Args:
            alias_name: Key pair associated with the RabbitMQ
            key_format: Valid key formats are Base64 and PKCS12.
        Returns:
            dict: RabbitMQ certificate
        """
        uri = self.URI + "/keys/" + alias_name + "?format=" + key_format
        return self._client.get(uri)
