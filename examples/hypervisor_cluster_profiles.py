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

# This example requires a ServerProfileTemplate with name "spt_hcp" and HypervisorManager
# with name "172.18.13.11"

from pprint import pprint

from config_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

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
hypervisor_cluster_profiles = oneview_client.hypervisor_cluster_profiles
hypervisor_managers = oneview_client.hypervisor_managers
profile_templates = oneview_client.server_profile_templates
os_deployment_plans = oneview_client.os_deployment_plans

hypervisor_manager = "172.18.13.11"
spt_name = "ProfileTemplate-1"  # spt without os deployment plan and one mgmt connection
deployment_plan = "Basic Deployment Plan"

# Getting the uris from name
hyp_mgr_uri = hypervisor_managers.get_by_name(hypervisor_manager).data['uri']
spt_uri = profile_templates.get_by_name(spt_name).data['uri']
dp_uri = os_deployment_plans.get_by_name(deployment_plan).data['uri']

options = {
    "name": "Test_cluster_profile",
    "description": "test cluster",
    "hypervisorType": "Vmware",
    "hypervisorClusterSettings": {
        "type": "Vmware",
        "drsEnabled": True,
        "haEnabled": False,
        "multiNicVMotion": False,
        "virtualSwitchType": "Standard"
    },
    "hypervisorHostProfileTemplate": {
        "serverProfileTemplateUri": spt_uri,
        "deploymentPlan": {
            "deploymentPlanUri": dp_uri,
            "serverPassword": "",
            "deploymentCustomArgs": []
        },
        "hostprefix": "Test_cluster_profile",
        "virtualSwitches": [],
        "hostConfigPolicy": {
            "leaveHostInMaintenance": False,
            "useHostnameToRegister": False
        },
        "virtualSwitchConfigPolicy": {
            "manageVirtualSwitches": True,
            "configurePortGroups": True
        }
    },
    "mgmtIpSettingsOverride": None,
    "hypervisorManagerUri": hyp_mgr_uri,
    "path": "DC1",
    "initialScopeUris": []
}

vswitch_options = {
    "hypervisorManagerUri": hyp_mgr_uri,
    "serverProfileTemplateUri": spt_uri
}

# Get all cluster profiles
print("\nGet all hypervisor cluster profiles")
cluster_profiles_all = hypervisor_cluster_profiles.get_all()
for profile in cluster_profiles_all:
    print('  - {}'.format(profile['name']))

# Find recently created hypervisor cluster profile by name
print("\nGet Hypervisor cluster profile by name")
hypervisor_cluster_profile = hypervisor_cluster_profiles.get_by_name(options['name'])

if hypervisor_cluster_profile:
    print("\nFound hypervisor cluster profile by name: {}.\n  uri = {}".format(
        hypervisor_cluster_profile.data['name'], hypervisor_cluster_profile.data['uri']))
else:
    # Create virtual switch layout
    print("\nCreate virtual switch layout")

    vswitch_layout = hypervisor_cluster_profiles.create_virtual_switch_layout(data=vswitch_options)
    pprint(vswitch_layout)

    # Create a Hypervisor Cluster Profile with the options provided
    options['hypervisorHostProfileTemplate']['virtualSwitches'] = vswitch_layout

    hypervisor_cluster_profile = hypervisor_cluster_profiles.create(data=options)
    print("\nCreated a hypervisor cluster profile with name: {}.\n  uri = {}".format(
        hypervisor_cluster_profile.data['name'], hypervisor_cluster_profile.data['uri']))

# Get the first 10 records
print("\nGet the first ten hypervisor cluster profiles")
cluster_profiles_top_ten = hypervisor_cluster_profiles.get_all(0, 10)
for profile in cluster_profiles_top_ten:
    print('  - {}'.format(profile['name']))

# Filter by hypervisor type
print("\nGet all hypervisor cluster profiles filtering by hypervisor type")
cluster_profiles_filtered = hypervisor_cluster_profiles.get_all(filter="\"'hypervisorType'='Vmware'\"")
for profile in cluster_profiles_filtered:
    print("Cluster profile with type 'Vmware'  - {}".format(profile['name']))

# Get all sorting by name descending
print("\nGet all hypervisor cluster profiles sorting by name")
clusters_sorted = hypervisor_cluster_profiles.get_all(sort='name:descending')
for profile in clusters_sorted:
    print('  - {}'.format(profile['name']))

# Get by uri
print("\nGet a hypervisor cluster profile by uri")
cluster_profile_by_uri = hypervisor_cluster_profiles.get_by_uri(hypervisor_cluster_profile.data['uri'])
pprint(cluster_profile_by_uri.data)

# Update the name of recently created hypervisor cluster profile
data_to_update = {'name': 'Updated cluster'}
if hypervisor_cluster_profile:
    hypervisor_cluster_profile.update(data=data_to_update)
    print("\nUpdated hypervisor cluster profile name - {0} to {1}".format(
        options['name'], hypervisor_cluster_profile.data['name']))

# Get compliance preview of cluster profile
if hypervisor_cluster_profile:
    profile_compliance = hypervisor_cluster_profile.get_compliance_preview()
    print("   - Compliance preview: '{}'".format(profile_compliance))

# Delete the created hypervisor cluster profile
if hypervisor_cluster_profile:
    hypervisor_cluster_profile.delete(soft_delete=True, force=True)
    print("\nSuccessfully deleted hypervisor cluster profile")
