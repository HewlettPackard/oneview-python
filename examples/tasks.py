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
tasks = oneview_client.tasks

# Getting the first 5 tasks
print("Getting the first 5 tasks")
tasks_limited = tasks.get_all(0, 5)
pprint(tasks_limited)

# Get a specific task by id
component = tasks_limited[0]["uri"].split('/')[-1]
print("Get a specific task")
try:
    tasks = tasks.get_by_id(component)
    pprint(tasks.data)
except HPEOneViewException as e:
    print(e.msg)

# Get a tree of tasks with specified filter
print("Get a tree of tasks")
tasks_filtered = tasks.get_all(filter="\"taskState='Completed'\"", view="tree", count=10)
pprint(tasks_filtered)

# Get an aggregate tree of tasks with specified filter
print("Get a aggregate tree")
tasks_filtered = tasks.get_all(filter="\"taskState='Completed'\"", view="aggregatedTree", childLimit=2, topCount=2)
pprint(tasks_filtered)

# Get a flat tree of tasks with specified filter
print("Get a flat tree")
tasks_filtered = tasks.get_all(view="flat-tree", start=0, count=1, filter="status=Warning OR status=OK")
pprint(tasks_filtered)

# Performs a patch operation
if oneview_client.api_version >= 1200:
    try:
        tasks_filtered = tasks.get_all(filter=["\"taskState='Running'\"", "\"isCancellable='true'\""])
        task_uri = tasks_filtered[0]['uri']
        response = tasks.patch(task_uri)
        print(response)
    except IndexError as e:
        print("Task state running and isCancellable true is not found")
        print(e)
