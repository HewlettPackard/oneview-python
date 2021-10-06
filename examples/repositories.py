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

from hpeOneView.oneview_client import OneViewClient
from hpeOneView.exceptions import HPEOneViewException
from config_loader import try_load_from_file

# To run this example fill the ip and the credentials below or use a configuration file
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": "<api_version>"
}

options = {
    "repositoryName": "Repo_Name",
    "userName": "<repository_username>",
    "password": "<repository_password>",
    "repositoryURI": "<repositoryURI>",
    "repositoryType": "FirmwareExternalRepo"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
repositories = oneview_client.repositories

# Get all, with defaults
print("\nGet all repositories")
repos = repositories.get_all()
print(repos)

# Get the first 10 repositories
print("\nGet the first ten repositories")
repos_limited = repositories.get_all(0, 10)
print(repos_limited)

# Get by name
print("\nGet all repositories filtering by name")
repo = repositories.get_by_name(repos[0]['name'])
print(repo.data)

# Get all in descending order
print("\nGet all repositories sorting by name")
repos_sorted = repositories.get_all(sort='name:descending')
print(repos_sorted)

if repo:
    print("\nFound repo by name: '%s'.\n  uri = '%s'" % (repo.data['name'], repo.data['uri']))

# Create a Repository with the options provided
try:
    created_repo = repositories.create(data=options)
    print("\nCreated a repo with name: '%s'.\n  uri = '%s'" % (created_repo.data['name'], created_repo.data['uri']))
except HPEOneViewException as e:
    print("Exception {} occurred while creating repository".format(str(e)))

# Get by repositoryId
print("\nGet a repo by id")
repos_by_id = repositories.get_by_id(repo.data['uuid'])
print(repos_by_id.data)

# Update repositoryName
print("\n Update repositoryName from recently created repository")
try:
    repo_with_updated_name = repo.patch('replace',
                                        '/repositoryName',
                                        'TestUpdated')
    print(repo_with_updated_name.data['name'])
except HPEOneViewException as e:
    print("Exception {} occurred while patch operation of repository".format(str(e)))

# Delete the created repository
repo.delete()
print("\nSuccessfully deleted repo")
