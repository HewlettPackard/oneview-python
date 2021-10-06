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

from hpeOneView.oneview_client import OneViewClient
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
label = oneview_client.labels

RESOURCE_URI = "/rest/enclosures/0000000000A66102"

print("\nSet the labels assigned to a resource")
LABELS_TO_CREATE = dict(
    resourceUri=RESOURCE_URI,
    labels=["labelSample", "enclosureDemo"]
)
RESOURCE_LABELS = label.create(LABELS_TO_CREATE)
pprint(RESOURCE_LABELS.data)

print("\nGet all labels")
ALL_LABELS = label.get_all(category=['fc-networks', 'enclosures'], name_prefix="label")
pprint(ALL_LABELS)

LABEL_NAME = ALL_LABELS[0]["name"]
print("\nGet a label by name: ", LABEL_NAME)
LABEL_BY_NAME = label.get_by_name(LABEL_NAME)
pprint(LABEL_BY_NAME.data)

LABEL_URI = ALL_LABELS[0]["uri"]
print("\nGet a label by uri: ", LABEL_URI)
LABEL_BY_URI = label.get_by_uri(LABEL_URI)
pprint(LABEL_BY_URI.data)

print("\nGet all the labels for the resource %s" % RESOURCE_URI)
LABELS_BY_RESOURCE = label.get_by_resource(RESOURCE_URI)
pprint(LABELS_BY_RESOURCE.data)

print("\nGets all resources assigned with label name: "), ALL_LABELS[0]["name"]
ASSIGNED_RESOURCES = label.get_ASSIGNED_RESOURCES(ALL_LABELS[0]["name"])
pprint(ASSIGNED_RESOURCES)

print("\nUpdate the resource labels")
LABELS_TO_UPDATE = dict(
    labels=[
        dict(name="renamed label", uri=LABELS_BY_RESOURCE.data['labels'][0]['uri']),
        dict(name="enclosureDemo1")
    ]
)
UPDATED_RESOURCE_LABELS = LABELS_BY_RESOURCE.update(LABELS_TO_UPDATE)
pprint(UPDATED_RESOURCE_LABELS.data)

print("\nDelete all the labels for a resource")
LABELS_BY_RESOURCE.delete()
