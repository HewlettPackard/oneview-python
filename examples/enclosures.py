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

from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException
from CONFIG_loader import try_load_from_file

# This example is compatible only for C7000 ENCLOSURES
CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>",
    "ENCLOSURE_group_URI": "/rest/ENCLOSURE-groups/06475bf3-084b-4874",
    "ENCLOSURE_hostname": "",
    "ENCLOSURE_username": "",
    "ENCLOSURE_password": "",
}

ENCLOSURE_NAME = "0000A66101"

# Specify variant of your appliance before running this example
API_VARIANT = "Synergy"

# Declare a CA signed CERTIFICATE file path.
CERTIFICATE_FILE = ""

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

# The hostname, ENCLOSURE group URI, username, and password must be set on the CONFIGURATION file
OPTIONS = {
    "ENCLOSUREGroupUri": CONFIG['ENCLOSURE_group_URI'],
    "hostname": CONFIG['ENCLOSURE_hostname'],
    "username": CONFIG['ENCLOSURE_username'],
    "password": CONFIG['ENCLOSURE_password'],
    "licensingIntent": "OneView"
}

# Get Enclosure resource object
oneview_client = OneViewClient(CONFIG)
ENCLOSURE_resource = oneview_client.ENCLOSURES
SCOPEs = oneview_client.SCOPEs

# Get all ENCLOSURES
print("Get all ENCLOSURES")
ENCLOSURES = ENCLOSURE_resource.get_all()
for enc in ENCLOSURES:
    print('  {name}'.format(**enc))

ENCLOSURE = ENCLOSURE_resource.get_by_name(ENCLOSURE_NAME)
if not ENCLOSURE:
    # Creates an ENCLOSURE and returns created ENCLOSURE object
    ENCLOSURE = ENCLOSURE_resource.add(OPTIONS)
print("Enclosure '{name}'.\n  URI = '{URI}'".format(**ENCLOSURE.data))

# Get by URI.
print("Find an ENCLOSURE by URI")
URI = ENCLOSURE.data['URI']
ENCLOSURE = ENCLOSURE_resource.get_by_URI(URI)
pprint(ENCLOSURE.data)

# Update name of the newly added ENCLOSURE
UPDATE_NAME = ENCLOSURE_NAME + "-Updated"
print("Updating the ENCLOSURE with name " + UPDATE_NAME)
HEADERS = {'If-Match': '*'}
ENCLOSURE.patch('replace', '/name', UPDATE_NAME, custom_HEADERS=HEADERS)
print("  Done.\n  URI = '{URI}', name = {name}".format(**ENCLOSURE.data))

# Revert the name of the ENCLOSURE
print("Reverting the ENCLOSURE name " + ENCLOSURE_NAME)
HEADERS = {'If-Match': '*'}
ENCLOSURE.patch('replace', '/name', ENCLOSURE_NAME, custom_HEADERS=HEADERS)
print("  Done.\n  URI = '{URI}', name = {name}".format(**ENCLOSURE.data))

# Update CONFIGURATION
print("Reapplying the appliance's CONFIGURATION on the ENCLOSURE")
try:
    ENCLOSURE.update_CONFIGURATION()
    print("  Done.")
except HPEOneViewException as e:
    print(e.msg)

print("Retrieve the environmental CONFIGURATION data for the ENCLOSURE")
try:
    ENVIRONMENTAL_CONFIGURATION = ENCLOSURE.get_ENVIRONMENTAL_CONFIGURATION()
    print("  Enclosure calibratedMaxPower = {calibratedMaxPower}".format(**ENVIRONMENTAL_CONFIGURATION))
except HPEOneViewException as e:
    print(e.msg)

# Set the calibrated max power of an unmanaged or unsupported ENCLOSURE
# update_ENVIRONMENTAL_CONFIGURATION is available only in C7000
if API_VARIANT == 'C7000':
    print("Set the calibrated max power of an unmanaged or unsupported ENCLOSURE")

    try:
        CONFIGURATION = {
            "calibratedMaxPower": 2500
        }
        ENCLOSURE_UPDATED_ENCCONF = ENCLOSURE.update_ENVIRONMENTAL_CONFIGURATION(CONFIGURATION)
        print("  Done.")
    except HPEOneViewException as e:
        print(e.msg)

# Refresh the ENCLOSURE
print("Refreshing the ENCLOSURE")
try:
    REFRESH_STATE = {"refreshState": "RefreshPending"}
    ENCLOSURE.REFRESH_STATE(REFRESH_STATE)
    print("  Done")
except HPEOneViewException as e:
    print(e.msg)

# Buid the SSO URL parameters
# get_sso is available only in C7000
if API_VARIANT == 'C7000':
    print("Build the SSO (Single Sign-On) URL parameters for the ENCLOSURE")
    try:
        SSO_URL_PARAMETERS = ENCLOSURE.get_sso('Active')
        pprint(SSO_URL_PARAMETERS)
    except HPEOneViewException as e:
        print(e.msg)

# Get Statistics specifying parameters
print("Get the ENCLOSURE statistics")
try:
    ENCLOSURE_STATISTICS = ENCLOSURE.get_utilization(fields='AveragePower',
                                                     filter='startDate=2016-06-30T03:29:42.000Z',
                                                     view='day')
    pprint(ENCLOSURE_STATISTICS)
except HPEOneViewException as e:
    print(e.msg)

# Create a Certificate Signing Request (CSR) for the ENCLOSURE.
if API_VARIANT == 'C7000':
    BAY_NUMBER = 1  # Required for C7000 ENCLOSURE
else:
    BAY_NUMBER = None

CSR_DATA = {
    "type": "CertificateDtoV2",
    "organization": "organization",
    "organizationalUnit": "organization unit",
    "locality": "locality",
    "state": "state",
    "country": "country",
    "commonName": "name"
}
try:
    ENCLOSURE.generate_CSR(CSR_DATA, BAY_NUMBER=BAY_NUMBER)
    print("Generated CSR for the ENCLOSURE.")
except HPEOneViewException as e:
    print(e.msg)

# Get the CERTIFICATE Signing Request (CSR) that was generated by previous POST.
try:
    CSR = ENCLOSURE.get_CSR(BAY_NUMBER=BAY_NUMBER)
    with open('ENCLOSURE.CSR', 'w') as CSR_file:
        CSR_file.write(CSR["base64Data"])
    print("Saved CSR(generated by previous POST) to 'ENCLOSURE.CSR' file")
except HPEOneViewException as e:
    print(e.msg)

# Import CA signed CERTIFICATE to the ENCLOSURE.
try:
    # Certificate has to be signed by CA before running the task.
    CERTIFICATE_FILE = "ENCLOSURE.CSR"
    CERTIFICATE = open(CERTIFICATE_FILE).read()

    CERTIFICATE_DATA = {
        "type": "CertificateDataV2",
        "base64Data": CERTIFICATE
    }

    ENCLOSURE.import_CERTIFICATE(CERTIFICATE_DATA, BAY_NUMBER=BAY_NUMBER)
    print("Imported Signed Certificate  to the ENCLOSURE.")
except HPEOneViewException as e:
    print(e.msg)
except Exception as e:
    print(e)

print("\n## Create the SCOPE")
OPTIONS = {
    "name": "SampleScopeForTest",
    "description": "Sample Scope description"
}
SCOPE = SCOPEs.create(OPTIONS)

# Get Enclosure by SCOPE_URIs
if oneview_client.api_version >= 600:
    try:
        ENCLOSURES_BY_SCOPE_URIS = ENCLOSURE.get_all(SCOPE_URIs=SCOPE.data['URI'])
        if len(ENCLOSURES_BY_SCOPE_URIS) > 0:
            print("Found %d Enclosures" % (len(ENCLOSURES_BY_SCOPE_URIS)))
            i = 0
            while i < len(ENCLOSURES_BY_SCOPE_URIS):
                print("Found Enclosures by SCOPE_URIs: '%s'.\n  URI = '%s'" % (ENCLOSURES_BY_SCOPE_URIS[i]['name'], ENCLOSURES_BY_SCOPE_URIS[i]['URI']))
                i += 1
            pprint(ENCLOSURES_BY_SCOPE_URIS)
        else:
            print("No Enclosures found with SCOPE.")
    except HPEOneViewException as e:
        print(e.msg)

# Delete the SCOPE
SCOPE.delete()
print("\n## Scope deleted successfully.")

if API_VARIANT == 'C7000':
    # Remove the recently added ENCLOSURE
    ENCLOSURE.remove()
    print("Enclosure removed successfully")
