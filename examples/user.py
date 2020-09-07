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
from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file
from copy import deepcopy

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
    'roles': ['Read only'],
    'type': 'UserAndRoles',
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
    "newPassword" : "password123",
    "oldPassword" : "password1234",
    "userName" : "user1"
}
changePasswordResponse = users.change_password(change_password_request)
print("Changed Password successfully")
print(changePasswordResponse)

# Adds different roles to the recently created user
user = oneview_client.users.get_by_name(options['userName'])
print(user.data)
print("\n user: %s, roles before update: %s" % (user.data['userName'], user.data['roles']))
user_copy = deepcopy(user.data)
user_copy['replaceRoles'] = True
user_copy['roles'] = ['Infrastructure administrator']
user_update = user.update(user_copy)
print("\n user: %s, roles after update: %s" % (user_update.data['userName'], user_update.data['roles']))

# Get user by role
user = oneview_client.users.get_by_name(options['role'])
print("Found users by role: '%s'.\n '\n" % (user.data))

# Get user by name
user = oneview_client.users.get_by_name(options['userName'])
print("Found user by name: '%s'. uri = '%s'\n" % (user.data['userName'], user.data['uri']))

# Get all users
print("Get all users")
users = oneview_client.users.get_all()
pprint(users)

# # Validates if full name is already in use
bol = oneview_client.users.validate_full_name(options['fullName'])
print("Is full name already in use? %s" % (bol))

# # Validates if user name is already in use
bol = oneview_client.users.validate_user_name(options['userName'])
print("Is user name already in use? %s" % (bol))

# Delete the created user
oneview_client.users.delete(user)
print("\nSuccessfully deleted user")
