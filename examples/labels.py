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
LABEL = oneview_client.LABELs

RESOURCE_URI = "/rest/enclosures/0000000000A66102"

print("\nSet the LABELs assigned to a resource")
LABELS_TO_CREATE = dict(
    resourceUri=RESOURCE_URI,
    LABELs=["LABELSample", "enclosureDemo"]
)
RESOURCE_LABELS = LABEL.create(LABELS_TO_CREATE)
pprint(RESOURCE_LABELS.data)

print("\nGet all LABELs")
ALL_LABELS = LABEL.get_all(category=['fc-networks', 'enclosures'], name_prefix="LABEL")
pprint(ALL_LABELS)

LABEL_NAME = ALL_LABELS[0]["name"]
print("\nGet a LABEL by name: ", LABEL_NAME)
LABEL_BY_NAME = LABEL.get_by_name(LABEL_NAME)
pprint(LABEL_BY_NAME.data)

LABEL_URI = ALL_LABELS[0]["uri"]
print("\nGet a LABEL by uri: ", LABEL_URI)
LABEL_BY_URI = LABEL.get_by_uri(LABEL_URI)
pprint(LABEL_BY_URI.data)

print("\nGet all the LABELs for the resource %s" % RESOURCE_URI)
LABELS_BY_RESOURCE = LABEL.get_by_resource(RESOURCE_URI)
pprint(LABELS_BY_RESOURCE.data)

print("\nGets all resources assigned with LABEL name: "), ALL_LABELS[0]["name"]
ASSIGNED_RESOURCES = LABEL.get_ASSIGNED_RESOURCES(ALL_LABELS[0]["name"])
pprint(ASSIGNED_RESOURCES)

print("\nUpdate the resource LABELs")
LABELS_TO_UPDATE = dict(
    LABELs=[
        dict(name="renamed LABEL", uri=LABELS_BY_RESOURCE.data['LABELs'][0]['uri']),
        dict(name="enclosureDemo1")
    ]
)
UPDATED_RESOURCE_LABELS = LABELS_BY_RESOURCE.update(LABELS_TO_UPDATE)
pprint(UPDATED_RESOURCE_LABELS.data)

print("\nDelete all the LABELs for a resource")
LABELS_BY_RESOURCE.delete()
