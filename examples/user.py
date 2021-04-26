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
            'roleName': 'Infrastructure administrator',
            'scopeUri': '/rest/scopes/6cf6d4da-1b5e-4322-9dff-6ef545ad700f'
        }
    ],
    'type': 'UserAndPermissions',
    'userName': 'testUser'
}

multi_users = [
    {
        'emailAddress': 'testUser@example.com',
        'enabled': 'true',
        'fullName': 'testUser101',
        'mobilePhone': '555-2121',
        'officePhone': '555-1212',
        'password': 'myPass1234',
        'permissions': [
            {
                'roleName': 'Read only',
            }
        ],
        'type': 'UserAndPermissions',
        'userName': 'testUser1'
    },
    {
        'emailAddress': 'testUser@example.com',
        'enabled': 'true',
        'fullName': 'testUser101',
        'mobilePhone': '555-2121',
        'officePhone': '555-1212',
        'password': 'myPass1234',
        'permissions': [
            {
                'roleName': 'Read only',
            }
        ],
        'type': 'UserAndPermissions',
        'userName': 'testUser2'
    }
]
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
users = oneview_client.users

# Create a User
user = users.create(options)
print("Created user '%s' successfully.\n  uri = '%s'\n" % (user.data['userName'], user.data['uri']))
print(user.data)

# Create a Multiple Users
multi_user = users.create_multiple_user(multi_users)
print("Created multiple users successfully.\n")
print(multi_user)

# Updata the user
data = user.data.copy()
data["password"] = "change1234"
updated_user = user.update(data)
print("The users is updated successfully....\n")
print(updated_user.data)

# Add role to userName
role_options = [
    {
        "roleName": "Backup administrator"
    }
]
role = users.add_role_to_userName("testUser1", role_options)
print("Successfully added new role to existing one....\n")
print(role)

# Update role to userName (it will replace entrie role with specified role)
role_options = [
    {
        "roleName": "Scope administrator"
    },
    {
        "roleName": "Backup administrator"
    }
]

role = users.update_role_to_userName("testUser1", role_options)
print("Successfully updated the role to the username....\n")
print(role)

# Remove a role from the user
role = users.remove_role_from_username("testUser1", "Scope administrator")
print("Removed role from the user successfully...\n")
print(role)

# Get user by name
user = users.get_by_userName(options['userName'])
print("Found user by uri = '%s'\n" % user.data['uri'])

# Get all users
print("Get all users")
all_users = users.get_all()
pprint(all_users)

# Validates if full name is already in use
bol = users.validate_full_name(options['fullName'])
print("Is full name already in use? %s" % (bol))

# Validates if user name is already in use
bol = users.validate_user_name(options['userName'])
print("Is user name already in use? %s" % (bol))

# Get the user's role list
rolelist = users.get_role_by_userName("testUser")
print(">> Got all the roles for the users")
print(rolelist)

# Get by role
role = users.get_user_by_role("Infrastructure administrator")
print(">> Got the users by role name\n")
print(role)

# Remove single user
user_to_delete = users.get_by_userName("testUser")
user_to_delete.delete()
print("Successfully deleted the testuser2 user.....\n")

# Remove Multiple users
user_name = ["testUser1", "testUser2"]
users.delete_multiple_user(user_name)
print("Deleted multiple users successfully...\n")

# Change Password only during the initial setup of the appliance.
change_password_request = {
    "oldPassword": "mypass1234",
    "newPassword": "admin1234",
    "userName": "testUser3"
}
changePasswordResponse = users.change_password(change_password_request)
print("Changed Password successfully")
print(changePasswordResponse)
