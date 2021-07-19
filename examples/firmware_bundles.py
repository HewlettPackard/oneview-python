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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run this example you must define a path to a valid file
spp_path = "<spp_path>"
hotfix_path = "<hotfix_path>"
compsig_path = "<compsig_path>"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
firmware_bundles = oneview_client.firmware_bundles
firmware_drivers = oneview_client.firmware_drivers

# Upload a firmware bundle
firmware = firmware_bundles.get_by_name(spp_path)
if not firmware:
    print("\nUpload a firmware bundle")
    firmware_bundle_information = firmware_bundles.upload(file_path=spp_path)
    print("\n Upload successful! Firmware information returned: \n")
    pprint(firmware_bundle_information)
else:
    print("\n Firmware Bundle already present")

# Upload a hotfix
hotfix = firmware_bundles.get_by_name(hotfix_path)
if not hotfix:
    print("\nUpload a hotfix")
    hotfix_information = firmware_bundles.upload(file_path=hotfix_path)
    print("\n Upload successful! Hotfix information returned: \n")
    pprint(hotfix_information)
else:
    print("\n Hotfix already present")

# Upload a compsig to hotfix
compsig = firmware_bundles.get_by_name(compsig_path)
if compsig and compsig.data['resourceState'] == 'AddFailed':
    print("\nUpload a compsig to hotfix")
    compsig_information = firmware_bundles.upload_compsig(file_path=compsig_path)
    print("\n Upload successful! CompSig information returned: \n")
    pprint(compsig_information)
else:
    print("\nHotfix is not present or compsig is already added")
