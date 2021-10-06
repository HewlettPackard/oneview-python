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
        "USERName": "",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

oneview_client = OneViewClient(CONFIG)
USERs = oneview_client.USERs
SCOPEs = oneview_client.SCOPEs

# Get the SCOPE Uri
SCOPE_OPTIONS = {
    "name": "SampleScopeForTest",
    "description": "Sample Scope description"
}
SCOPE = SCOPEs.get_by_name(SCOPE_OPTIONS['name'])
if not SCOPE:
    SCOPE = SCOPEs.create(SCOPE_OPTIONS)
SCOPE_URI = SCOPE.DATA['uri']

OPTIONS = {
    'emailAddress': 'testUser@example.com',
    'enabled': 'true',
    'fullName': 'testUser101',
    'mobilePhone': '555-2121',
    'officePhone': '555-1212',
    'password': 'myPass1234',
    'permissions': [
        {
            'ROLEName': 'Infrastructure administrator',
            'SCOPEUri': SCOPE_URI
        }
    ],
    'type': 'UserAndPermissions',
    'USERName': 'testUser'
}

MULTI_USERS = [
    {
        'emailAddress': 'testUser@example.com',
        'enabled': 'true',
        'fullName': 'testUser101',
        'mobilePhone': '555-2121',
        'officePhone': '555-1212',
        'password': 'myPass1234',
        'permissions': [
            {
                'ROLEName': 'Read only',
            }
        ],
        'type': 'UserAndPermissions',
        'USERName': 'testUser1'
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
                'ROLEName': 'Read only',
            }
        ],
        'type': 'UserAndPermissions',
        'USERName': 'testUser2'
    }
]

# Create a User
USER = USERs.create(OPTIONS)
print("Created USER '%s' successfully.\n  uri = '%s'\n" % (USER.DATA['USERName'], USER.DATA['uri']))
print(USER.DATA)

# Create a Multiple Users
MULTI_USER = USERs.create_multiple_USER(MULTI_USERS)
print("\nCreated multiple USERs successfully.\n")
print(MULTI_USER.DATA)

# UpDATA the USER
DATA = USER.DATA.copy()
DATA["password"] = "change1234"
UPDATED_USER = USER.update(DATA)
print("\nThe USERs is updated successfully....\n")
print(UPDATED_USER.DATA)

# Add ROLE to USERName
ROLE_OPTIONS = [
    {
        "ROLEName": "Backup administrator"
    }
]
ROLE = USERs.add_ROLE_to_USERName("testUser1", ROLE_OPTIONS)
print("\nSuccessfully added new ROLE to existing one....\n")
print(ROLE.DATA)

# Update ROLE to USERName (it will replace entrie ROLE with specified ROLE)
ROLE_OPTIONS = [
    {
        "ROLEName": "Scope administrator"
    },
    {
        "ROLEName": "Backup administrator"
    },
    {
        "ROLEName": "Infrastructure administrator"
    }
]

ROLE = USERs.update_ROLE_to_USERName("testUser1", ROLE_OPTIONS)
print("\nSuccessfully updated the ROLE to the USERname....\n")
print(ROLE)

# Remove mulitple ROLE from the USER
# If a single ROLE is to be removed, just specifiy ["ROLE_name"] or "ROLE_name" instead of list.
ROLE = USERs.remove_ROLE_from_USERname("testUser1", ["Scope administrator", "Backup administrator"])
print("\nRemoved ROLE from the USER successfully...\n")
print(ROLE)

# Get USER by name
USER = USERs.get_by_USERName(OPTIONS['USERName'])
if USER:
    print("\nFound USER by uri = '%s'\n" % USER.DATA['uri'])

# Get all USERs
print("\nGet all USERs")
ALL_USERS = USERs.get_all()
pprint(ALL_USERS)

# Validates if full name is already in use
BOL = USERs.validate_full_name(OPTIONS['fullName'])
print("Is full name already in use? %s" % (BOL.DATA))

# Validates if USER name is already in use
BOL = USERs.validate_USER_NAME(OPTIONS['USERName'])
print("Is USER name already in use? %s" % (BOL.DATA))

# Get the USER's ROLE list
ROLELIST = USERs.get_ROLE_associated_with_USERName("testUser")
print("\n>> Got all the ROLEs for the USERs\n")
print(ROLELIST)

# Get by ROLE
ROLE = USERs.get_USER_by_ROLE("Infrastructure administrator")
print("\n>> Got the USERs by ROLE name\n")
print(ROLE)

# Remove single USER
USER_TO_DELETE = USERs.get_by_USERName("testUser")
if USER_TO_DELETE:
    USER_TO_DELETE.delete()
    print("\nSuccessfully deleted the testUSER2 USER.....\n")

# Remove Multiple USERs
USER_NAME = ["testUser1", "testUser2"]
USERs.delete_multiple_USER(USER_NAME)
print("\nDeleted multiple USERs successfully...\n")

# NOTE: The below script changes the default administrator's password during first-time appliance
# setup only.
'''
# Change Password only during the initial setup of the appliance.
change_password_request = {
    "oldPassword": "mypass1234",
    "newPassword": "admin1234",
    "USERName": "testUser3"
}
changePasswordResponse = USERs.change_password(change_password_request)
print("Changed Password successfully")
print(changePasswordResponse)
'''
