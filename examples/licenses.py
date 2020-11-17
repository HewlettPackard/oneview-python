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

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient
from pprint import pprint

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

# Example license Key
# ACDE B9MA H9PY CHW3 U7B5 HWW5 Y9JL KMPL B89H MZVU DXAU 2CSM GHTG L762 KQL7 EG5M KJVT D5KM AFVW TT5J F77K NXWW BPSM YF26 28JS EWTZ X36Q
# M5G7 WZJL HH5Q L975 SNJT 288F ADT2 LK44 56UG V8MC 2K9X 7KG2 F6AD EMVA 9GEB 95Y6 XBM3 HVDY LBSS PU24 KEWY JSJC FPZC 2JJE
# ZLAB\"24R2-02192-002 T1111A HP_OneView_w/o_iLO_Explicit_Feature J4E8IAMANEON\"

options = {
    "key": "<your license Key>",
    "type": "LicenseV500"
}

# Add a License
license = oneview_client.licenses.create(options)
print("\n\nLicense added '%s' successfully.\n" % license['key'])

# Get all licenses
print("\n\n\n\n **********   Displaying all the Licenses loaded on the appliance:  ********** \n\n\n\n")
licenses = oneview_client.licenses.get_all()
pprint(licenses)

# Get License by ID
uri = license['uri']
print(uri)
print("\n License fetched by ID is: \n")
license = oneview_client.licenses.get_by_id(uri)
pprint(license)

# Delete License by ID
print("\n\n   ********** Delete the license by ID:  **********")
print(uri)
oneview_client.licenses.delete(uri)

print("\n Check if the license is Deleted: \n")
lic = oneview_client.licenses.get_by_id(uri)
pprint(lic)
