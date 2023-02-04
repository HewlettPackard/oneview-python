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
from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# This resource is only available on HPE Synergy

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
sas_logical_jbods = oneview_client.sas_logical_jbods

print("\nGet all SAS logical JBODs")
all_sas_logical_jbods = sas_logical_jbods.get_all()
pprint(all_sas_logical_jbods)

if all_sas_logical_jbods:

    sas_logical_jbod_uri = all_sas_logical_jbods[0]["uri"]

    print("\nGet the SAS logical JBOD by uri")
    sas_logical_jbod_by_uri = sas_logical_jbods.get_by_uri(sas_logical_jbod_uri)
    pprint(sas_logical_jbod_by_uri)

drive_enclosure_uri_list = []
drive_enclosures = oneview_client.drive_enclosures.get_all()
if drive_enclosures:
    drive_enclosure_uri_list.append(drive_enclosures[0]['uri'])

options = {
    "numPhysicalDrives": 1,
    "name": "SasLogicalJBOD1",
    "description": "Sas Jbod description",
    "minSizeGB": 200,
    "maxSizeGB": 600,
    "eraseData": "true",
    "driveTechnology":
    {
        "deviceInterface": "SAS",
        "driveMedia": "HDD"
    },
    "driveEnclosureUris": drive_enclosure_uri_list,
}

print("\nCreate a SAS logical JBOD")
sas_logical_jbod1 = sas_logical_jbods.create(options)
pprint(sas_logical_jbod1)

# Ensure that the selected drive bays are not already part of another logical JBOD
drive_bay_uris = []
drive_bays = drive_enclosures[1]['driveBays']
drive_bay_uris.append(drive_bays[0]['uri'])
drive_bay_uris.append(drive_bays[1]['uri'])
options2 = {
    "name": "SasLogicalJBOD2",
    "description": "Sas Jbod description",
    "eraseData": "true",
    "driveBayUris": drive_bay_uris
}
print("\nCreates a SAS logical JBOD by providing specific drive bay URIs")
sas_logical_jbod2 = sas_logical_jbods.create(options2)
pprint(sas_logical_jbod2)

if sas_logical_jbod1:
    drives_list = sas_logical_jbod1.get_drives()
    print("\nList of drives allocated to SAS Logical JBOD: {}".format(drives_list))

    print("\nPatch Operations on SAS logical JBOD")
    sas_logical_jbod_changed1 = sas_logical_jbod1.patch(
        operation="replace",
        path="/name",
        value="SasLogicalJBOD-Renamed"
    )
    print("\nChanged SAS logical JBOD name to {}".format(sas_logical_jbod_changed1.data['name']))

    sas_logical_jbod_changed2 = sas_logical_jbod_changed1.patch(
        operation="replace",
        path="/description",
        value="New Description"
    )
    print("\nChanged Description of JBOD {} to {}".format(sas_logical_jbod_changed1.data['name'], sas_logical_jbod_changed1.data['description']))

    sas_logical_jbod_changed3 = sas_logical_jbod_changed2.patch(
        operation="replace",
        path="/eraseData",
        value="false"
    )
    print("\nDisabled drive sanitize option of {}".format(sas_logical_jbod_changed3.data['name']))

    sas_logical_jbod_changed4 = sas_logical_jbod_changed3.patch(
        operation="replace",
        path="/clearMetadata",
        value="true"
    )
    print("\nCleared metadata of {}".format(sas_logical_jbod_changed4.data['name']))

    print("\nRemove a SAS logical JBOD")
    sas_logical_jbod_changed4.delete()
