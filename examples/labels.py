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
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

resource_uri = "/rest/enclosures/09SGH100X6J1"

print("\nSet the labels assigned to a resource")
labels_to_create = dict(
    resourceUri=resource_uri,
    labels=["labelSample2", "enclosureDemo"]
)

resource_labels = oneview_client.labels.create(labels_to_create)
pprint(resource_labels)

print("\nUpdate the resource labels")
labels_to_update = dict(
    uri="/rest/labels/resources/" + resource_uri,
    resourceUri=resource_uri,
    type="ResourceLabels",
    labels=[
        dict(name="new label"),
        dict(name="enclosureDemo")
    ]
)
updated_resource_labels = oneview_client.labels.update(labels_to_update)
pprint(updated_resource_labels)

print("\nGet all labels")
all_labels = oneview_client.labels.get_all()
pprint(all_labels)

label_uri = all_labels[0]["uri"]

print("\nGet a label by uri")
label_by_uri = oneview_client.labels.get(label_uri)
pprint(label_by_uri)

print("\nGet all the labels for the resource %s" % resource_uri)
labels_by_resource = oneview_client.labels.get_by_resource(resource_uri)
pprint(labels_by_resource)

print("\nDelete all the labels for a resource")
oneview_client.labels.delete(dict(uri="/rest/labels/resources/" + resource_uri))
print("Done!")
