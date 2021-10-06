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

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 800
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
connection_templates = oneview_client.connection_templates

# The name and ID of an existent Connection Template must be set to run this example
CONNECTION_TEMPLATE_NAME = 'defaultConnectionTemplate'

# Get all connection templates
print("Get all connection templates")
CON_TEMPLATES = connection_templates.get_all()
pprint(CON_TEMPLATES)

# Get all sorting by name descending
print("Get all connection templates sorting by name")
CON_TEMPLATES_SORTED = connection_templates.get_all(sort='name:descending')
pprint(CON_TEMPLATES_SORTED)

# Get default template
print("Get default connection template")
CON_TEMPLATE_DEFAULT = connection_templates.get_default()
pprint(CON_TEMPLATE_DEFAULT)

# Get by name
print("Get a connection_template by name")
CON_TEMPLATE_BYNAME = connection_templates.get_by_name(CONNECTION_TEMPLATE_NAME)
pprint(CON_TEMPLATE_BYNAME.data)

# Update the connection_template retrieved in the last operation
print("Update the retrieved connection_template typicalBandwidth")
if CON_TEMPLATE_BYNAME:
    TEMPLATE_BYNAME = CON_TEMPLATE_BYNAME.data.copy()
    TEMPLATE_BYNAME['bandwidth']['typicalBandwidth'] = 5000
    CON_TEMPLATE_UPDATED = CON_TEMPLATE_BYNAME.update(TEMPLATE_BYNAME)
    pprint(CON_TEMPLATE_UPDATED.data)
