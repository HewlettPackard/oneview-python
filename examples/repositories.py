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

remote_server_options = {
    "name": "172.18.13.11",
}

options = {
    "repositoryName": "Repo_Name",
    "userName": "Admin",
    "password": "*******",
    "repositoryURI": "https://172.20.3.65/repositoryFolder",
    "repositoryType": "FirmwareExternalRepo",
    "base64data": ""
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
repositories = oneview_client.repositories
certificate_server = oneview_client.certificates_server

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
repo = repositories.get_by_name(repos_limited[0]['name'])
print(repo.data)

# Get all in descending order
print("\nGet all repositories sorting by name")
repos_sorted = repositories.get_all(sort='name:descending')
print(repos_sorted)

if repo:
    print("\nFound repo by name: '%s'.\n  uri = '%s'" % (repo.data['name'], repo.data['uri']))

# Create a Repository with the options provided
try:
    print("\nGet server certificate of remote server by ip address")
    remote_server_cert = certificate_server.get_remote(remote_server_options['name'])
    if remote_server_cert:
        ca_certificate = remote_server_cert.data['certificateDetails'][0]['base64Data']
        print(ca_certificate)
        options['base64Data'] = ca_certificate
    created_repo = repositories.create(data=options)
    print("\nCreated a repo with name: '%s'.\n  uri = '%s'" % (created_repo.data['name'], created_repo.data['uri']))
except HPEOneViewException as e:
    print("Exception {} occurred while creating repository".format(str(e)))

# Get by repositoryId
print("\nGet a repo by id")
repos_by_id = repositories.get_by_id(repo.data['uuid'])
print(repos_by_id.data)

# Update repositoryName from recently created repository
print("\n Update repositoryName from recently created repository")
try:
    repo_with_updated_name = created_repo.patch('replace',
                                        '/repositoryName',
                                        repo.data['name'])
    print(repo_with_updated_name)
except HPEOneViewException as e:
    print("Exception {} occurred while patch operation of repository".format(str(e)))

# Edit a repository
print("Edit a repository")
try:
    data_to_edit = {
        "id": repo_with_updated_name['id'],
        "repositoryName": "Repo_Name",
        "userName": "Admin",
        "password": "*******",
        "repositoryURI": "https://172.20.3.65/repositoryFolder",
        "base64data": ca_certificate
    }
    created_repo.update(data=data_to_edit)
    print("\nUpdated repo '%s' successfully." % (created_repo.data['repositoryName']))
except HPEOneViewException as e:
    print("Exception {} occurred while update operation of repository".format(str(e)))

# Delete the created repository
created_repo.delete()
print("\nSuccessfully deleted repo")
