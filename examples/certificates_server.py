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

from pprint import pprint

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

REMOTE_SERVER_OPTIONS = {
    "name": "172.18.13.11",
}

OPTIONS = {
    "certificateDetails": [{
        "aliasName": "vcenter",
        "base64Data": "",
        "type": "CertificateDetailV2"
        }],
}


# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
ONEVIEW_CLIENT = OneViewClient(CONFIG)
CERTIFICATE_SERVER = ONEVIEW_CLIENT.certificates_server

# Fetch server certificate of remote server
print("\nGet server certificate of remote server by ip address")
REMOTE_SERVER_CERT = CERTIFICATE_SERVER.get_remote(REMOTE_SERVER_OPTIONS['name'])
if REMOTE_SERVER_CERT:
    CA_CERTIFICATE = REMOTE_SERVER_CERT.data['certificateDetails'][0]['base64Data']
    print(CA_CERTIFICATE)

# Fetch certificate by alias name
print("\nGet server certificate by alias name")
SERVER_CERTIFICATE = CERTIFICATE_SERVER.get_by_alias_name("vcenter")
if SERVER_CERTIFICATE:
    print("\nFound server certificate by aliasName: {}.\n  uri = {}".format(\
        SERVER_CERTIFICATE.data['certificateDetails'][0]['aliasName'], \
        SERVER_CERTIFICATE.data['uri']))
else:
    # Add a server certificate with the OPTIONS provided
    OPTIONS['certificateDetails'][0]['base64Data'] = CA_CERTIFICATE
    OPTIONS['certificateDetails'][0]['type'] = REMOTE_SERVER_CERT.\
            data['certificateDetails'][0]['type']
    SERVER_CERTIFICATE = CERTIFICATE_SERVER.create(data=OPTIONS)
    print("\nAdded a server certificate with aliasName: {}.\n  uri = {}".format(\
        SERVER_CERTIFICATE.data['certificateDetails'][0]['aliasName'],\
	 SERVER_CERTIFICATE.data['uri']))

# Get by uri
print("\nGet a server certificate by uri")
SERVER_CERT_BY_URI = CERTIFICATE_SERVER.get_by_uri(SERVER_CERTIFICATE.data['uri'])
pprint(SERVER_CERT_BY_URI.data)

# Update alias name of recently added certificate
print("\nUpdate recently created server certificate")
DATA_TO_UPDATE = {'name': 'Updated vcenter'}
SERVER_CERTIFICATE.update(data=DATA_TO_UPDATE)
print("\nUpdated server certificate {} successfully.\n".format(\
      SERVER_CERTIFICATE.data['certificateDetails'][0]['aliasName']))

# Delete the added server certificate
SERVER_CERTIFICATE.delete()
print("\nSuccessfully deleted server certificate")

# Create server certificate for automation
OPTIONS['certificateDetails'][0]['base64Data'] = CA_CERTIFICATE
OPTIONS['certificateDetails'][0]['type'] = REMOTE_SERVER_CERT.data['certificateDetails'][0]['type']
SERVER_CERTIFICATE = CERTIFICATE_SERVER.create(data=OPTIONS)
print("\nAdded a server certificate with aliasName: {}.\n  uri = {}".format(\
      SERVER_CERTIFICATE.data['certificateDetails'][0]['aliasName'],\
      SERVER_CERTIFICATE.data['uri']))
