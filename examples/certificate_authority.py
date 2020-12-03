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
certificate_authority = oneview_client.certificate_authority

# Retrieve Internal CA Certificate
print("\n\nGet all the internal Certificate Authorities:\n")
certificates_all = certificate_authority.get_all(cert_details=False)
print(certificates_all)

# Retrieve Internal CA Certificate with certificate details
print("\n\nGet the certificate details of internal Certificate Authority:\n")
certificate = certificate_authority.get_all()
for cert in certificate:
    if cert['certificateDetails']['aliasName'] == 'localhostSelfSignedCertificate':
        print(cert['certificateDetails']['base64Data'])

# Retrieve Certificate Revocation List
print("\n\nGetting the Certificate Revocation List:\n")
certificate_visual_content = certificate_authority.get_crl()
pprint(certificate_visual_content.data)

# Revoke Internal CA Signed Certificate
print("\n\nRevoking Internal CA Signed Certificate\n")
# success = certificate_authority.delete("default")
# print(success)
