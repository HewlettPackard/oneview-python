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

import logging

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

"""
hpeOneView do not add any handlers other than NullHandler.
The configuration of handlers is the prerogative of the developer who uses hpeOneView library.
This example uses a StreamHandler to send the logging output to streams sys.stdout and sys.stderr.
"""

logger = logging.getLogger('hpeOneView')

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a FC Network
fc_network = oneview_client.fc_networks.create(options)

# Find recently created network by name
fc_network = oneview_client.fc_networks.get_by('name', 'OneViewSDK Test FC Network')[0]

# Update autoLoginRedistribution from recently created network
fc_network['autoLoginRedistribution'] = False
fc_network = oneview_client.fc_networks.update(fc_network)

# Get all, with defaults
fc_nets = oneview_client.fc_networks.get_all()
# Filter by name
fc_nets_filtered = oneview_client.fc_networks.get_all(filter="\"'name'='OneViewSDK Test FC Network'\"")

# Get all sorting by name descending
fc_nets_sorted = oneview_client.fc_networks.get_all(sort='name:descending')

# Get the first 10 records
fc_nets_limited = oneview_client.fc_networks.get_all(0, 10)

# Get the created network by uri
oneview_client.fc_networks.get(fc_network['uri'])

# Delete the created network
oneview_client.fc_networks.delete(fc_network)

# Get by Id. This Id doesn't exist
oneview_client.fc_networks.get('3518be0e-17c1-4189-8f81-66t3444f6155')
