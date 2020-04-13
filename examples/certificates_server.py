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
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

remote_server_options = {
    "name": "172.18.13.11",
}

options = {
    "certificateDetails":[
      {
         "aliasName":"vcenter",
         "base64Data":"",
         "type":"CertificateDetailV2"
      }
    ],
}


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient.config()
certificate_server = oneview_client.certificates_server

# Fetch server certificate of remote server
print("\nGet server certificate of remote server by ip address")
remote_server_cert = certificate_server.get_remote(remote_server_options['name'])
ca_certificate = remote_server_cert['certificateDetails'][0]['base64Data']
print(ca_certificate)

# Add a server certificate with the options provided
options['certificateDetails'][0]['base64Data'] = ca_certificate
options['certificateDetails'][0]['type'] = remote_server_cert['certificateDetails'][0]['type']
server_certificate = certificate_server.create(data=options)
print("\nAdded a server certificate with aliasName: {}.\n  uri = {}".format(server_certificate.data['certificateDetails'][0]['aliasName'], server_certificate.data['uri']))

# Fetch certificate by alias name
print("\nGet server certificate by alias name")
server_cert_by_alias = certificate_server.get_by_aliasName("vcenter")
print("\nFound server certificate by aliasName: {}.\n  uri = {}".format(server_cert_by_alias['certificateDetails'][0]['aliasName'], server_cert_by_alias['uri']))

# Get by uri
print("\nGet a server certificate by uri")
server_cert_by_uri = certificate_server.get_by_uri(server_certificate.data['uri'])
pprint(server_cert_by_uri.data)

# Update alias name of recently added certificate
print("\nUpdate recently created server certificate")
data_to_update = {'name': 'Updated vcenter'}
server_certificate.update(data=data_to_update)
print("\nUpdated server certificate {} successfully.\n".format(server_certificate.data['certificateDetails'][0]['aliasName']))

# Delete the added server certificate
server_certificate.delete()
print("\nSuccessfully deleted server certificate")
