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

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)
CERTIFICATE_AUTHORITY = ONEVIEW_CLIENT.certificate_authority

# Retrieve Internal CA Certificate
print("\n\nGet all the internal Certificate Authorities:\n")
CERTIFICATES_ALL = CERTIFICATE_AUTHORITY.get_all(cert_details=False)
print(CERTIFICATES_ALL)

# Retrieve Internal CA Certificate with CERTIFICATE details
print("\n\nGet the CERTIFICATE details of internal Certificate Authority:\n")
CERTIFICATE = CERTIFICATE_AUTHORITY.get_all()
for cert in CERTIFICATE:
    if cert['CERTIFICATEDetails']['aliasName'] == 'localhostSelfSignedCertificate':
        print(cert['CERTIFICATEDetails']['base64Data'])

# Retrieve Certificate Revocation List
print("\n\nGetting the Certificate Revocation List:\n")
CERTIFICATE_VISUAL_CONTENT = CERTIFICATE_AUTHORITY.get_crl()
pprint(CERTIFICATE_VISUAL_CONTENT.data)

# Revoke Internal CA Signed Certificate
print("\n\nRevoking Internal CA Signed Certificate\n")
# success = CERTIFICATE_AUTHORITY.delete("default")
# print(success)
