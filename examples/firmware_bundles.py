# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run this example you must define a path to a valid file
SPP_PATH = "<SPP_PATH>"
HOTFIX_PATH = "<HOTFIX_PATH>"
COMPSIG_PATH = "<COMPSIG_PATH>"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
ONEVIEW_CLIENT = OneViewClient(CONFIG)
FIRMWARE_BUNDLES = ONEVIEW_CLIENT.firmware_bundles
FIRMWARE_DRIVERS = ONEVIEW_CLIENT.firmware_drivers

# Upload a FIRMWARE bundle
FIRMWARE = FIRMWARE_BUNDLES.get_by_name(SPP_PATH)
if not FIRMWARE:
    print("\nUpload a FIRMWARE bundle")
    FIRMWARE_BUNDLE_INFORMATION = FIRMWARE_BUNDLES.upload(file_path=SPP_PATH)
    print("\n Upload successful! Firmware information returned: \n")
    pprint(FIRMWARE_BUNDLE_INFORMATION)
else:
    print("\n Firmware Bundle already present")

# Upload a HOTFIX
HOTFIX = FIRMWARE_BUNDLES.get_by_name(HOTFIX_PATH)
if not HOTFIX:
    print("\nUpload a HOTFIX")
    HOTFIX_INFORMATION = FIRMWARE_BUNDLES.upload(file_path=HOTFIX_PATH)
    print("\n Upload successful! Hotfix information returned: \n")
    pprint(HOTFIX_INFORMATION)
else:
    print("\n Hotfix already present")

# Upload a COMPSIG to HOTFIX
COMPSIG = FIRMWARE_BUNDLES.get_by_name(COMPSIG_PATH)
if COMPSIG and COMPSIG.data['resourceState'] == 'AddFailed':
    print("\nUpload a COMPSIG to HOTFIX")
    COMPSIG_INFORMATION = FIRMWARE_BUNDLES.upload_compsig(file_path=COMPSIG_PATH)
    print("\n Upload successful! CompSig information returned: \n")
    pprint(COMPSIG_INFORMATION)
else:
    print("\nHotfix is not present or COMPSIG is already added")
