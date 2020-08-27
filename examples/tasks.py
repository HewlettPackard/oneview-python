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
from hpeOneView.exceptions import HPEOneViewException
from config_loader import try_load_from_file

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
tasks = oneview_client.tasks

# Getting the first 5 tasks
print("Getting the first 5 tasks")
tasks_limited = tasks.get_all(0, 5)
pprint(tasks_limited)

# Get a specific task by id
print("Get a specific task")
try:
    tasks = tasks.get_by_id("36BD6806-71CD-4F1B-AA12-5E3E67379659")
    pprint(tasks.data)
except HPEOneViewException as e:
    print(e.msg)

# Get a tree of tasks with specified filter
print("Get a tree of tasks")
tasks_filtered = tasks.get_all(filter="\"taskState='Completed'\"", view="tree", count=10)
pprint(tasks_filtered)

# Performs a patch operation
if oneview_client.api_version >= 1200:
    task = tasks.get_by_id("36BD6806-71CD-4F1B-AA12-5E3E67379659")
    if task.data.get('isCancellable') and task.data['isCancellable'] is False:
        try:
            updated_tasks = tasks.patch('Replace', "isCancellable", True)
            pprint(updated_tasks.data)
        except HPEOneViewException as e:
            print(e.msg)
