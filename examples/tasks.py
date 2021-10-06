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
from hpeOneView.exceptions import HPEOneViewException
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
TASKS = oneview_client.TASKS

# Getting the first 5 TASKS
print("Getting the first 5 TASKS")
TASKS_LIMITED = TASKS.get_all(0, 5)
pprint(TASKS_LIMITED)

# Get a specific task by id
COMPONENT = TASKS_LIMITED[0]["uri"].split('/')[-1]
print("Get a specific task")
try:
    TASKS = TASKS.get_by_id(COMPONENT)
    pprint(TASKS.data)
except HPEOneViewException as e:
    print(e.msg)

# Get a tree of TASKS with specified filter
print("Get a tree of TASKS")
TASKS_FILTERED = TASKS.get_all(filter="\"taskState='Completed'\"", view="tree", count=10)
pprint(TASKS_FILTERED)

# Get an aggregate tree of TASKS with specified filter
print("Get a aggregate tree")
TASKS_FILTERED = TASKS.get_all(filter="\"taskState='Completed'\"", view="aggregatedTree", childLimit=2, topCount=2)
pprint(TASKS_FILTERED)

# Get a flat tree of TASKS with specified filter
print("Get a flat tree")
TASKS_FILTERED = TASKS.get_all(view="flat-tree", start=0, count=1, filter="status=Warning OR status=OK")
pprint(TASKS_FILTERED)

# Performs a patch operation
if oneview_client.api_version >= 1200:
    TASKS_FILTERED = TASKS.get_all(filter=["\"taskState='Running'\"", "\"isCancellable='true'\""])
    TASK_URI = TASKS_FILTERED[0]['uri']
    RESPONSE = TASKS.patch(TASK_URI)
    print(RESPONSE)
