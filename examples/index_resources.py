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
index_resource_obj = oneview_client.index_resources
server_hardware_obj = oneview_client.server_hardware

print('\nGetting all index resources:')
index_resources = index_resource_obj.get_all()
pprint(index_resources)

sh = server_hardware_obj.get_all()[0]
print('\nGetting index resource for server hardware with uri "{0}":'.format(sh['uri']))
index_resource = index_resource_obj.get_by_uri(sh['uri'])
pprint(index_resource.data)

print('\nGetting aggregated index resources with attribute: "{0}" and category: "{1}"'.format(attribute, category))
index_resources_aggr = index_resource_obj.get_aggregated(attribute, category)
pprint(index_resources_aggr.data)
