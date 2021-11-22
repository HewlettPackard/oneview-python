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

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

ATTRIBUTE = 'Model'
CATEGORY = 'server-hardware'

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

ONEVIEW_CLIENT = OneViewClient(CONFIG)
INDEX_RESOURCE_OBJ = ONEVIEW_CLIENT.index_resources
SERVER_HARDWARE_OBJ = ONEVIEW_CLIENT.server_hardware

print('\nGetting all index resources:')
INDEX_RESOURCES = INDEX_RESOURCE_OBJ.get_all()
pprint(INDEX_RESOURCES)

SH = SERVER_HARDWARE_OBJ.get_all()[0]
print('\nGetting index resource for server hardware with uri "{0}":'.format(SH['uri']))
INDEX_RESOURCE = INDEX_RESOURCE_OBJ.get_by_uri(SH['uri'])
pprint(INDEX_RESOURCE.data)

print('\nGetting aggregated index resources with ATTRIBUTE: "{0}" and CATEGORY:\
	 "{1}"'.format(ATTRIBUTE, CATEGORY))
INDEX_RESOURCES_AGGR = INDEX_RESOURCE_OBJ.get_aggregated(ATTRIBUTE, CATEGORY)
pprint(INDEX_RESOURCES_AGGR.data)
