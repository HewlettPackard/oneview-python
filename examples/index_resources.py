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

from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

attribute = 'Model'
category = 'server-hardware'

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

print('\nGetting all index resources:')
index_resources = oneview_client.index_resources.get_all()
pprint(index_resources)

sh = oneview_client.server_hardware.get_all()[0]
print('\nGetting index resource for server hardware with uri "{0}":'.format(sh['uri']))
index_resource = oneview_client.index_resources.get(sh['uri'])
pprint(index_resource)

print('\nGetting aggregated index resources with attribute: "{0}" and category: "{1}"'.format(attribute, category))
index_resources = oneview_client.index_resources.get_aggregated(attribute, category)
pprint(index_resources)
