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
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
label = oneview_client.labels

resource_uri = "/rest/enclosures/0000000000A66102"

print("\nSet the labels assigned to a resource")
labels_to_create = dict(
    resourceUri=resource_uri,
    labels=["labelSample", "enclosureDemo"]
)
resource_labels = label.create(labels_to_create)
pprint(resource_labels.data)

print("\nGet all labels")
all_labels = label.get_all(category=['fc-networks', 'enclosures'], name_prefix="label")
pprint(all_labels)

label_name = all_labels[0]["name"]
print("\nGet a label by name: ", label_name)
label_by_name = label.get_by_name(label_name)
pprint(label_by_name.data)

label_uri = all_labels[0]["uri"]
print("\nGet a label by uri: ", label_uri)
label_by_uri = label.get_by_uri(label_uri)
pprint(label_by_uri.data)

print("\nGet all the labels for the resource %s" % resource_uri)
labels_by_resource = label.get_by_resource(resource_uri)
pprint(labels_by_resource.data)

print("\nUpdate the resource labels")
labels_to_update = dict(
    labels=[
        dict(name="renamed label", uri=labels_by_resource.data['labels'][0]['uri']),
        dict(name="enclosureDemo1")
    ]
)
updated_resource_labels = labels_by_resource.update(labels_to_update)
pprint(updated_resource_labels.data)

print("\nDelete all the labels for a resource")
labels_by_resource.delete()
