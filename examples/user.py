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

options = {
    'emailAddress': 'testUser@example.com',
    'enabled': 'true',
    'fullName': 'testUser101',
    'mobilePhone': '555-2121',
    'officePhone': '555-1212',
    'password': 'myPass1234',
    'permissions': [
        {
            'roleName': 'Read only',
            'scopeUri': '/rest/scopes/6a6bb53c-5502-4f89-8573-cd1fb5b02a54',
        }
    ],
    'type': 'UserAndPermissions',
    'userName': 'testUser'
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
users = oneview_client.users

# Create a User
user = users.create(options)
print("Created user '%s' successfully.\n  uri = '%s'\n" % (user.data['userName'], user.data['uri']))

# Change Password
change_password_request = {
    "currentPassword": "myPass1234",
    "enabled": "true",
    "password": "admin1234",
    "userName": "testUser"
}
changePasswordResponse = users.change_password(change_password_request)
print("Changed Password successfully")
print(changePasswordResponse)

# Get user by name
user = users.get_by_userName(options['userName'])
print("Found user by uri = '%s'\n" % user.data['uri'])

# Get all users
print("Get all users")
all_users = users.get_all()
pprint(all_users)

# # Validates if full name is already in use
bol = users.validate_full_name(options['fullName'])
print("Is full name already in use? %s" % (bol))

# # Validates if user name is already in use
bol = users.validate_user_name(options['userName'])
print("Is user name already in use? %s" % (bol))
