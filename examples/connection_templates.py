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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 800
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
connection_templates = oneview_client.connection_templates

# The name and ID of an existent Connection Template must be set to run this example
connection_template_name = 'defaultConnectionTemplate'

# Get all connection templates
print("Get all connection templates")
con_templates = connection_templates.get_all()
pprint(con_templates)

# Get all sorting by name descending
print("Get all connection templates sorting by name")
con_templates_sorted = connection_templates.get_all(sort='name:descending')
pprint(con_templates_sorted)

# Get default template
print("Get default connection template")
con_template_default = connection_templates.get_default()
pprint(con_template_default)

# Get by name
print("Get a connection_template by name")
con_template_byname = connection_templates.get_by_name(connection_template_name)
pprint(con_template_byname.data)

# Update the connection_template retrieved in the last operation
print("Update the retrieved connection_template typicalBandwidth")
template_byname = con_template_byname.data.copy()
template_byname['bandwidth']['typicalBandwidth'] = 5000
con_template_updated = con_template_byname.update(template_byname)
pprint(con_template_updated.data)
