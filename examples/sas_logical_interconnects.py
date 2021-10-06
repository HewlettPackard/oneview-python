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
from CONFIG_loader import try_load_from_file

# This resource is only available on HPE Synergy

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<userNAME>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
SAS_LOGICAL_INTERCONNECTS = oneview_client.SAS_LOGICAL_INTERCONNECTS
FIRMWARE_DRIVER_URI = None

# Get all SAS Logical Interconnects
print("\nGet all SAS Logical Interconnects")
LOGICAL_INTERCONNECTS = SAS_LOGICAL_INTERCONNECTS.get_all()
for SAS_LOGICAL_INTERCONNECT in LOGICAL_INTERCONNECTS:
    print('  Name: {NAME}'.format(**SAS_LOGICAL_INTERCONNECT))

NAME = LOGICAL_INTERCONNECTS[0]['NAME']
SAS_LOGICAL_INTERCONNECT = SAS_LOGICAL_INTERCONNECTS.get_by_NAME(NAME)

# Re-applies the CONFIGuration on the SAS Logical Interconnect
print("\nRe-applies the CONFIGuration on the SAS Logical Interconnect")
SAS_LOGICAL_INTERCONNECT.update_CONFIGuration()
print("\n  Done.")

# Return the SAS Logical Interconnect to a consistent state
print("\nReturn the SAS Logical Interconnect to a consistent state")
SAS_LOGICAL_INTERCONNECT.update_compliance()
print("\n  Done. The current consistency state is {consistencyStatus}.".format(**SAS_LOGICAL_INTERCONNECT.data))

# Return the SAS Logical Interconnect list to a consistent state
print("\nReturn the SAS Logical Interconnect list to a consistent state")
COMPLIANCE_URIS = [LOGICAL_INTERCONNECTS[0]['uri']]
SAS_LOGICAL_INTERCONNECT.update_compliance_all(COMPLIANCE_URIS)
print("\n  Done. The current consistency state is {consistencyStatus}.".format(**SAS_LOGICAL_INTERCONNECT.data))

# Replace Drive Enclosure (This example only works with real hardware)
print("\nReplacing Drive Enclosure")
DRIVE_REPLACEMENT = {
    "oldSerialNumber": "S46016710000J4524YPT",
    "newSerialNumber": "S46016710001J4524YPT"
}
DRIVE_REPLACEMENT_OUTPUT = SAS_LOGICAL_INTERCONNECT.replace_drive_enclosure(DRIVE_REPLACEMENT)
pprint(DRIVE_REPLACEMENT_OUTPUT)

# Get installed FIRMWARE
print("\nGet the installed FIRMWARE for a SAS Logical Interconnect that matches the specified ID.")
FIRMWARE = SAS_LOGICAL_INTERCONNECT.get_FIRMWARE()
pprint(FIRMWARE)

# Install the FIRMWARE to a SAS Logical Interconnect (time-consuming operation)
print("\nInstall the FIRMWARE to a SAS Logical Interconnect that matches the specified ID.")
FIRMWARE_TO_INSTALL = {
    "command": "Update",
    "force": "false",
    "sppUri": FIRMWARE_DRIVER_URI
}
INSTALLED_FIRMWARE = SAS_LOGICAL_INTERCONNECT.update_FIRMWARE(FIRMWARE_TO_INSTALL)
pprint(INSTALLED_FIRMWARE)
