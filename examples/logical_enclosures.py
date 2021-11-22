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

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)

ENCLOSURE_GROUPs = oneview_client.ENCLOSURE_GROUPs
enclosures = oneview_client.enclosures
LOGICAL_ENCLOSUREs = oneview_client.LOGICAL_ENCLOSUREs
SCOPEs = oneview_client.SCOPEs
FIRMWARE_DRIVERs = oneview_client.FIRMWARE_DRIVERs

# The valid enclosure URIs need to be inserted sorted by URI
# The number of enclosure URIs must be equal to the enclosure count in the enclosure group
OPTIONS = dict(
    enclosureUris=[],
    enclosureGroupUri="EG",
    forceInstallFirmware=False,
    name="LE"
)

VARIANT = 'synergy'
SCOPE_NAME = 'test_SCOPE'
FIRMWARE_DRIVER_NAME = "SPP_2018_06_20180709_for_HPE_Synergy_Z7550-96524"

# Create SCOPE
SCOPE_OPTIONS = {
    "name": SCOPE_NAME,
    "deSCRIPTion": "Sample Scope deSCRIPTion"
}
SCOPE = SCOPEs.get_by_name(SCOPE_NAME)
if SCOPE:
    print("Scope '{}' already exists".format(SCOPE_NAME))
else:
    print(" Creating the SCOPE '{}'".format(SCOPE_NAME))
    SCOPE = SCOPEs.create(SCOPE_OPTIONS)

# Get all logical enclosures
print("Get all logical enclosures")
LOGICAL_ENCLOSURES_ALL = LOGICAL_ENCLOSUREs.get_all()
for enc in LOGICAL_ENCLOSURES_ALL:
    print('   %s' % enc['name'])

# Get first logical enclosure
LOGICAL_ENCLOSURE_ALL = LOGICAL_ENCLOSUREs.get_all()
if LOGICAL_ENCLOSURE_ALL:
    LOGICAL_ENCLOSURE = LOGICAL_ENCLOSURE_ALL[0]
    print("Found logical enclosure '{}' at\n   uri: '{}'".format(
        LOGICAL_ENCLOSURE['name'], LOGICAL_ENCLOSURE['uri']))

    # Get logical enclosure by uri
    LOGICAL_ENCLOSURE = LOGICAL_ENCLOSUREs.get_by_uri(LOGICAL_ENCLOSURE['uri'])
    print("Got logical enclosure '{}' by\n   uri: '{}'".format(
        LOGICAL_ENCLOSURE.data['name'], LOGICAL_ENCLOSURE.data['uri']))

# Get Logical Enclosure by SCOPE_uris
if oneview_client.api_version >= 600:
    le_by_SCOPE_uris = LOGICAL_ENCLOSUREs.get_all(SCOPE_uris=SCOPE.data['uri'])
    if len(le_by_SCOPE_uris) > 0:
        print("Got Logical Enclosure by SCOPE_uris: '%s'.\n  uri = '%s'" % (le_by_SCOPE_uris[0]['name'], le_by_SCOPE_uris[0]['uri']))
        pprint(le_by_SCOPE_uris)
    else:
        print("No Logical Enclosure found by SCOPE_uris")

# Get Logical Enclosure by name
LOGICAL_ENCLOSURE = LOGICAL_ENCLOSUREs.get_by_name(OPTIONS["name"])
if not LOGICAL_ENCLOSURE:
    # Get enclosure group uri for creating logical enclosure
    ENCLOSURE_GROUP = ENCLOSURE_GROUPs.get_by_name(OPTIONS['enclosureGroupUri'])
    OPTIONS["enclosureGroupUri"] = ENCLOSURE_GROUP.data["uri"]
    ENCLOSURE_COUNT = ENCLOSURE_GROUP.data["enclosureCount"]

    # Get enclosures
    ENCLOSURES_ALL = enclosures.get_all()
    ENCLOSURE_URIS = []
    for i in range(0, ENCLOSURE_COUNT):
        ENCLOSURE_URIS.append(ENCLOSURES_ALL[i]["uri"])
    OPTIONS["enclosureUris"] = sorted(ENCLOSURE_URIS)
    print(OPTIONS)

    # Create a logical enclosure
    # This method is only available on HPE Synergy.
    try:
        LOGICAL_ENCLOSURE = LOGICAL_ENCLOSUREs.create(OPTIONS)
        print("Created logical enclosure'%s' successfully.\n  uri = '%s'" % (
            LOGICAL_ENCLOSURE.data['name'],
            LOGICAL_ENCLOSURE.data['uri'])
        )
    except HPEOneViewException as e:
        print(e.msg)

# Update the logical enclosure name
print("Update the logical enclosure to have a name of '%s'" %
      OPTIONS["name"])
RESOURCE = LOGICAL_ENCLOSURE.data.copy()
PREVIOUS_NAME = RESOURCE["name"]
RESOURCE["name"] = RESOURCE["name"] + "-Renamed"
LOGICAL_ENCLOSURE.update(RESOURCE)
print("   Done. uri: '%s', 'name': '%s'" %
      (LOGICAL_ENCLOSURE.data['uri'], LOGICAL_ENCLOSURE.data['name']))

print("Reset name")
RESOURCE = LOGICAL_ENCLOSURE.data.copy()
RESOURCE["name"] = PREVIOUS_NAME
LOGICAL_ENCLOSURE.update(RESOURCE)
print("   Done. uri: '%s', 'name': '%s'" %
      (LOGICAL_ENCLOSURE.data['uri'],
       LOGICAL_ENCLOSURE.data['name']))

# Update CONFIGuration
print("Reapply the appliance's CONFIGuration to the logical enclosure")
LOGICAL_ENCLOSURE.update_CONFIGuration()
print("   Done.")

# Update and get SCRIPT
# This method is available for API version 300 in synergy and in all API versions in c7000
if VARIANT == 'synergy' and oneview_client.api_version == 300:
    print("Update SCRIPT")
    SCRIPT = "# TEST COMMAND"
    LOGICAL_ENCLOSURE_updated = LOGICAL_ENCLOSURE.update_SCRIPT(LOGICAL_ENCLOSURE.data['uri'], SCRIPT)
    print("   updated SCRIPT: '{}'".format(LOGICAL_ENCLOSURE.get_SCRIPT()))

# Create support dumps
print("Generate support dump")
INFO = {
    "errorCode": "MyDump16",
    "encrypt": True,
    "excludeApplianceDump": False
}
SUPPORT_DUMP = LOGICAL_ENCLOSURE.generate_SUPPORT_DUMP(INFO)
print("   Done")

# update from group
try:
    print("Update from group")
    LOGICAL_ENCLOSURE_updated = LOGICAL_ENCLOSURE.update_from_group()
    print("   Done")
except Exception as e:
    print(e)

# Replace firmware of LE
FIRMWARE_DRIVER = FIRMWARE_DRIVERs.get_by('name', FIRMWARE_DRIVER_NAME)
if oneview_client.api_version >= 300:
    if LOGICAL_ENCLOSURE and len(FIRMWARE_DRIVER) != 0:
        print("Update firmware for a logical enclosure with the logical-interconnect validation set
	 as true.")

        LOGICAL_ENCLOSURE_updated = LOGICAL_ENCLOSURE.patch(
            operation="replace",
            path="/firmware",
            value={
                "firmwareBaselineUri": FIRMWARE_DRIVER[0]['uri'],
                "firmwareUpdateOn": "EnclosureOnly",
                "forceInstallFirmware": "true",
                "validateIfLIFirmwareUpdateIsNonDisruptive": "true",
                "logicalInterconnectUpdateMode": "Orchestrated",
                "updateFirmwareOnUnmanagedInterconnect": "true"
            },
            custom_headers={"if-Match": "*"}
        )
        pprint(LOGICAL_ENCLOSURE_updated.data)

# Delete the logical enclosure created (commented this to achieve continuty of automation SCRIPT execution)
# This method is only available on HPE Synergy.
# LOGICAL_ENCLOSURE.delete()
# print("Delete logical enclosure")
