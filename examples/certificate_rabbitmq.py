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

from pprint import pprint

from config_loader import try_load_from_file
from hpeOneView.exceptions import HPEOneViewException
from hpeOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

certificate_ca_signed_client = {
    "commonName": "default",
    "type": "RabbitMqClientCertV2"
}

certificate_self_signed_client = {
    "commonName": "any",
    "signedCert": "false",
    "type": "RabbitMqClientCertV2"
}


# Generate a CA Signed Certificate
print('Generate a CA Signed Certificate')
try:
    response = oneview_client.certificate_rabbitmq.generate(certificate_ca_signed_client)
    pprint(response)
except HPEOneViewException as e:
    print(e.msg)
    if e.oneview_response:
        print(e.oneview_response.get('recommendedActions'))


# Generate a Self Signed Certificate
print('\nGenerate a Self Signed Certificate')
try:
    response = oneview_client.certificate_rabbitmq.generate(certificate_self_signed_client)
    pprint(response)
except HPEOneViewException as e:
    print(e.msg)
    if e.oneview_response:
        print(e.oneview_response.get('recommendedActions'))


# Get by Alias Name
print('\nGet by Alias Name')
response = oneview_client.certificate_rabbitmq.get('default')
pprint(response)


# Get a Key Pair
print('\nGet a Key Pair')
response = oneview_client.certificate_rabbitmq.get_key_pair('default')
pprint(response)


# Get Keys in Base64 format
print('\nGet Keys in Base64 format')
response = oneview_client.certificate_rabbitmq.get_keys('default', 'Base64')
pprint(response)


# Get Keys in PKCS12 format
print('\nGet Keys in PKCS12 format')
response = oneview_client.certificate_rabbitmq.get_keys('default', 'PKCS12')
pprint(response)
