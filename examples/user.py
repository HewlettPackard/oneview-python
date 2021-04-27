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
users = oneview_client.users
scopes = oneview_client.scopes

# Get the scope Uri
scope_options = {
    "name": "SampleScopeForTest",
    "description": "Sample Scope description"
}
scope = scopes.get_by_name(scope_options['name'])
if not scope:
    scope = scopes.create(scope_options)
scope_uri = scope.data['uri']

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
            'scopeUri': scope_uri
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

# Create a User
user = users.create(options)
print("Created user '%s' successfully.\n  uri = '%s'\n" % (user.data['userName'], user.data['uri']))
print(user.data)

# Create a Multiple Users
multi_user = users.create_multiple_user(multi_users)
print("\nCreated multiple users successfully.\n")
print(multi_user)

# Updata the user
data = user.data.copy()
data["password"] = "change1234"
updated_user = user.update(data)
print("\nThe users is updated successfully....\n")
print(updated_user.data)

# Add role to userName
role_options = [
    {
        "roleName": "Backup administrator"
    }
]
role = users.add_role_to_userName("testUser1", role_options)
print("\nSuccessfully added new role to existing one....\n")
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
print("\nSuccessfully updated the role to the username....\n")
print(role)

# Remove a role from the user
role = users.remove_role_from_username("testUser1", "Scope administrator")
print("\nRemoved role from the user successfully...\n")
print(role)

# Get user by name
user = users.get_by_userName(options['userName'])
print("\nFound user by uri = '%s'\n" % user.data['uri'])

# Get all users
print("\nGet all users")
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
print("\n>> Got all the roles for the users\n")
print(rolelist)

# Get by role
role = users.get_user_by_role("Infrastructure administrator")
print("\n>> Got the users by role name\n")
print(role)

# Remove single user
user_to_delete = users.get_by_userName("testUser")
user_to_delete.delete()
print("\nSuccessfully deleted the testuser2 user.....\n")

# Remove Multiple users
user_name = ["testUser1", "testUser2"]
users.delete_multiple_user(user_name)
print("\nDeleted multiple users successfully...\n")

# NOTE: The below script changes the default administrator's password during first-time appliance setup only.
'''
# Change Password only during the initial setup of the appliance.
change_password_request = {
    "oldPassword": "mypass1234",
    "newPassword": "admin1234",
    "userName": "testUser3"
}
changePasswordResponse = users.change_password(change_password_request)
print("Changed Password successfully")
print(changePasswordResponse)
'''
