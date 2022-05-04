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

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

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

metrics_configuration = {
    "sourceTypeList": [
        {
            "sourceType": "/rest/power-devices",
            "sampleIntervalInSeconds": "300",
            "frequencyOfRelayInSeconds": "3600"
        },
        {
            "sourceType": "/rest/enclosures",
            "sampleIntervalInSeconds": "600",
            "frequencyOfRelayInSeconds": "3600"
        },
        {
            "sourceType": "/rest/server-hardware",
            "sampleIntervalInSeconds": "600",
            "frequencyOfRelayInSeconds": "1800"
        },
    ]
}

# Configure metric relay for server-hardware, enclosures and power-devices.
print("Configure metric streaming")
updated_metrics_configuration = oneview_client.metric_streaming.update_configuration(metrics_configuration)
pprint(updated_metrics_configuration)

# Get current relay configuration
print("Get current configuration")
current_configuration = oneview_client.metric_streaming.get_configuration()
pprint(current_configuration)

# Gets the list of all supported metrics and resource types.
print("Gets the list of all supported metrics and resource types")
supported_metrics = oneview_client.metric_streaming.get_capability()
pprint(supported_metrics)
