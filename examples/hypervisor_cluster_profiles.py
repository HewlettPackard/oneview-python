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

from CONFIG_loader import try_load_from_file
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_client = OneViewClient(CONFIG)
HYPERVISOR_CLUSTER_PROFILEs = oneview_client.HYPERVISOR_CLUSTER_PROFILEs
HYPERVISOR_MANAGERs = oneview_client.HYPERVISOR_MANAGERs
profile_templates = oneview_client.server_profile_templates
os_DEPLOYMENT_PLANs = oneview_client.os_DEPLOYMENT_PLANs

HYPERVISOR_MANAGER = "172.18.13.11"
SPT_NAME = "ProfileTemplate-1"  # spt without os deployment plan and one mgmt connection
DEPLOYMENT_PLAN = "Basic Deployment Plan"

# Getting the uris from name
HYP_MGR_URI = HYPERVISOR_MANAGERs.get_by_name(HYPERVISOR_MANAGER).data['uri']
SPT_URI = profile_templates.get_by_name(SPT_NAME).data['uri']
DP_URI = os_DEPLOYMENT_PLANs.get_by_name(DEPLOYMENT_PLAN).data['uri']

OPTIONS = {
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
        "serverProfileTemplateUri": SPT_URI,
        "deploymentPlan": {
            "deploymentPlanUri": DP_URI,
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
            "CONFIGurePortGroups": True
        }
    },
    "mgmtIpSettingsOverride": None,
    "hypervisorManagerUri": HYP_MGR_URI,
    "path": "DC1",
    "initialScopeUris": []
}

VSWITCH_OPTIONS = {
    "hypervisorManagerUri": HYP_MGR_URI,
    "serverProfileTemplateUri": SPT_URI
}

# Get all cluster profiles
print("\nGet all hypervisor cluster profiles")
CLUSTER_PROFILES_ALL = HYPERVISOR_CLUSTER_PROFILEs.get_all()
for profile in CLUSTER_PROFILES_ALL:
    print('  - {}'.format(profile['name']))

# Find recently created hypervisor cluster profile by name
print("\nGet Hypervisor cluster profile by name")
HYPERVISOR_CLUSTER_PROFILE = HYPERVISOR_CLUSTER_PROFILEs.get_by_name(OPTIONS['name'])

if HYPERVISOR_CLUSTER_PROFILE:
    print("\nFound hypervisor cluster profile by name: {}.\n  uri = {}".format(
        HYPERVISOR_CLUSTER_PROFILE.data['name'], HYPERVISOR_CLUSTER_PROFILE.data['uri']))
else:
    # Create virtual switch layout
    print("\nCreate virtual switch layout")

    VSWITCH_LAYOUT = HYPERVISOR_CLUSTER_PROFILEs.create_virtual_switch_layout(data=VSWITCH_OPTIONS)
    pprint(VSWITCH_LAYOUT)

    # Create a Hypervisor Cluster Profile with the OPTIONS provided
    OPTIONS['hypervisorHostProfileTemplate']['virtualSwitches'] = VSWITCH_LAYOUT

    HYPERVISOR_CLUSTER_PROFILE = HYPERVISOR_CLUSTER_PROFILEs.create(data=OPTIONS)
    print("\nCreated a hypervisor cluster profile with name: {}.\n  uri = {}".format(
        HYPERVISOR_CLUSTER_PROFILE.data['name'], HYPERVISOR_CLUSTER_PROFILE.data['uri']))

# Get the first 10 records
print("\nGet the first ten hypervisor cluster profiles")
CLUSTER_PROFILES_TOP_TEN = HYPERVISOR_CLUSTER_PROFILEs.get_all(0, 10)
for profile in CLUSTER_PROFILES_TOP_TEN:
    print('  - {}'.format(profile['name']))

# Filter by hypervisor type
print("\nGet all hypervisor cluster profiles filtering by hypervisor type")
CLUSTER_PROFILES_FILTERED = HYPERVISOR_CLUSTER_PROFILEs.get_all(filter="\"'hypervisorType'='Vmware'\"")
for profile in CLUSTER_PROFILES_FILTERED:
    print("Cluster profile with type 'Vmware'  - {}".format(profile['name']))

# Get all sorting by name descending
print("\nGet all hypervisor cluster profiles sorting by name")
CLUSTERS_SORTED = HYPERVISOR_CLUSTER_PROFILEs.get_all(sort='name:descending')
for profile in CLUSTERS_SORTED:
    print('  - {}'.format(profile['name']))

# Get by uri
print("\nGet a hypervisor cluster profile by uri")
CLUSTER_PROFILE_BY_URI = HYPERVISOR_CLUSTER_PROFILEs.get_by_uri(HYPERVISOR_CLUSTER_PROFILE.data['uri'])
pprint(CLUSTER_PROFILE_BY_URI.data)

# Update the name of recently created hypervisor cluster profile
DATA_TO_UPDATE = {'name': 'Updated cluster'}
if HYPERVISOR_CLUSTER_PROFILE:
    HYPERVISOR_CLUSTER_PROFILE.update(data=DATA_TO_UPDATE)
    print("\nUpdated hypervisor cluster profile name - {0} to {1}".format(
        OPTIONS['name'], HYPERVISOR_CLUSTER_PROFILE.data['name']))

# Get compliance preview of cluster profile
if HYPERVISOR_CLUSTER_PROFILE:
    PROFILE_COMPLIANCE = HYPERVISOR_CLUSTER_PROFILE.get_compliance_preview()
    print("   - Compliance preview: '{}'".format(PROFILE_COMPLIANCE))

# Delete the created hypervisor cluster profile
if HYPERVISOR_CLUSTER_PROFILE:
    HYPERVISOR_CLUSTER_PROFILE.delete(soft_delete=True, force=True)
    print("\nSuccessfully deleted hypervisor cluster profile")
