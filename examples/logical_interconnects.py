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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Specify variant of your appliance to run this example
api_variant = 'Synergy'

# To run this example, a logical interconnect name is required
logical_interconnect_name = "testlg1-Renamed Logical Interconnect Group"

# To install the firmware driver, a firmware driver name is required
firmware_driver_name = "HPE Synergy Custom SPP 2018110 2019 02 15, 2019.02.15.00"

# An Enclosure name must be set to create/delete an interconnect at a given location
enclosure_name = "0000A66102"

# Define the scope name to add the logical interconnect to it
scope_name = "test"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
logical_interconnects = oneview_client.logical_interconnects

# Get all logical interconnects
print("\nGet all logical interconnects")
all_logical_interconnects = logical_interconnects.get_all()
for logical_interconnect in all_logical_interconnects:
    print('  Name: {name}'.format(**logical_interconnect))

# Get installed firmware
print("\nGet the installed firmware for a logical interconnect that matches the specified name.")
firmwares = oneview_client.firmware_drivers.get_by('name', firmware_driver_name)
firmware = firmwares[0] if firmwares else None

print("\nGet the enclosure that matches the specified name.")
enclosures = oneview_client.enclosures.get_by_name(enclosure_name)
enclosure = enclosures.data if enclosures else None

# Get a logical interconnect by name
logical_interconnect = logical_interconnects.get_by_name(logical_interconnect_name)
print("\nFound logical interconnect by name {name}.\n URI: {uri}".format(**logical_interconnect.data))
print(logical_interconnect.data)

# Install the firmware to a logical interconnect
if firmware:
    print("\nInstall the firmware to a logical interconnect that matches the specified ID.")
    firmware_to_install = dict(
        command="Update",
        sppUri=firmware['uri']
    )
    installed_firmware = logical_interconnect.install_firmware(firmware_to_install)
    pprint(installed_firmware)

# Get scope to be added
print("\nGet the scope that matches the specified name.")
scope = oneview_client.scopes.get_by_name(scope_name)

# Performs a patch operation
# This operation is not supported in API version 200 and 600.
if scope and oneview_client.api_version not in [200, 600]:
    print("\nPatches the logical interconnect adding one scope to it")
    logical_interconnect.patch('replace',
                               '/scopeUris',
                               [scope.data['uri']])
    pprint(logical_interconnect.data)

print("\nGet the Ethernet interconnect settings for the logical interconnect")
ethernet_settings = logical_interconnect.get_ethernet_settings()
pprint(ethernet_settings)

# Update the Ethernet interconnect settings for the logical interconnect
ethernet_settings = logical_interconnect.data['ethernetSettings'].copy()
ethernet_settings['macRefreshInterval'] = 10  #This attribute is only supported in C7000
ethernet_settings['stormControlThreshold'] = 15  #This attribute is supported in Synergy
logical_interconnect_updated = logical_interconnect.update_ethernet_settings(ethernet_settings)
print("\nUpdated the ethernet settings")
print(logical_interconnect_updated.data)

# Update the internal networks on the logical interconnect
ethernet_network_options = {
    "name": "OneViewSDK Test Ethernet Network on Logical Interconnect",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}
ethernet_network = oneview_client.ethernet_networks.get_by_name(ethernet_network_options['name'])
if not ethernet_network:
    ethernet_network = oneview_client.ethernet_networks.create(ethernet_network_options)

logical_interconnect_updated = logical_interconnect.update_internal_networks([ethernet_network.data['uri']])
print("\nUpdated internal networks on the logical interconnect")
print("  with attribute 'internalNetworkUris' = {internalNetworkUris}".format(**logical_interconnect_updated))

# Get the internal VLAN IDs
print("\nGet the internal VLAN IDs for the provisioned networks on the logical interconnect")
internal_vlans = logical_interconnect.get_internal_vlans()
pprint(internal_vlans)

# Update the interconnect settings
# End-point supported only in api-versions 500 and below.
if oneview_client.api_version <= 500:
    print("\nUpdates the interconnect settings on the logical interconnect")
    interconnect_settings = {
        'ethernetSettings': logical_interconnect.data['ethernetSettings'].copy(),
        'fcoeSettings': {}
    }
    interconnect_settings['ethernetSettings']['macRefreshInterval'] = 7
    logical_interconnect_updated = logical_interconnect.update_settings(interconnect_settings)
    print("Updated interconnect settings on the logical interconnect")
    print("  with attribute 'macRefreshInterval' = {macRefreshInterval}".format(**logical_interconnect_updated['ethernetSettings']))
    pprint(logical_interconnect_updated)

# Get the SNMP configuration for the logical interconnect
print("\nGet the SNMP configuration for the logical interconnect")
snmp_configuration = logical_interconnect.get_snmp_configuration()
pprint(snmp_configuration)

# Update the SNMP configuration for the logical interconnect
print("\nUpdate the SNMP configuration for the logical interconnect")
snmp_configuration['enabled'] = True
snmp_configuration['readCommunity'] = "public"
logical_interconnect_updated = logical_interconnect.update_snmp_configuration(snmp_configuration)
interconnect_snmp = logical_interconnect_updated['snmpConfiguration']
print("  Updated SNMP configuration at uri: {uri}\n  with 'enabled': '{enabled}'".format(**interconnect_snmp))

# Get a collection of ports from the member interconnects which are eligible for assignment to an analyzer port
print("\nGet a collection of ports from the member interconnects which are eligible for assignment to "
      "an analyzer port on the logical interconnect")
unassigned_ports = logical_interconnect.get_unassigned_ports()
pprint(unassigned_ports)

# Get a collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port
print("\nGet a collection of uplink ports from the member interconnects which are eligible for assignment to "
      "an analyzer port on the logical interconnect")
unassigned_uplink_ports = logical_interconnect.get_unassigned_uplink_ports()
pprint(unassigned_uplink_ports)

# Get the port monitor configuration of a logical interconnect
print("\nGet the port monitor configuration of a logical interconnect")
monitor_configuration = logical_interconnect.get_port_monitor()
pprint(monitor_configuration)

# Update port monitor configuration of a logical interconnect
print("\nUpdate the port monitor configuration of a logical interconnect")
monitor_configuration['enablePortMonitor'] = True
logical_interconnect_updated = logical_interconnect.update_port_monitor(monitor_configuration)
print("  Updated port monitor at uri: {uri}\n  with 'enablePortMonitor': '{enablePortMonitor}'".format(
      **logical_interconnect_updated['portMonitor']))

# Update the configuration on the logical interconnect
print("\nUpdate the configuration on the logical interconnect")
logical_interconnect_updated = logical_interconnect.update_configuration()
print("  Done.")

# Return the logical interconnect to a consistent state
print("\nReturn the logical interconnect to a consistent state")
logical_interconnect_updated = logical_interconnect.update_compliance()
print("  Done. The current consistency state is {consistencyStatus}.".format(**logical_interconnect_updated))

# Generate the forwarding information base dump file for the logical interconnect
print("\nGenerate the forwarding information base dump file for the logical interconnect")
fwd_info_datainfo = logical_interconnect.create_forwarding_information_base()
pprint(fwd_info_datainfo)

# Get the forwarding information base data for the logical interconnect
print("\nGet the forwarding information base data for the logical interconnect")
fwd_information = logical_interconnect.get_forwarding_information_base()
pprint(fwd_information)

# Get the QoS aggregated configuration for the logical interconnect.
print("\nGets the QoS aggregated configuration for the logical interconnect.")
qos = logical_interconnect.get_qos_aggregated_configuration()
pprint(qos)

# Update the QOS aggregated configuration
print("\nUpdate QoS aggregated settings on the logical interconnect")
qos['activeQosConfig']['configType'] = 'Passthrough'
li = logical_interconnect.update_qos_aggregated_configuration(qos)
pprint(li['qosConfiguration'])

# Get the telemetry configuration of the logical interconnect
print("\nGet the telemetry configuration of the logical interconnect")
telemetry_configuration = logical_interconnect.get_telemetry_configuration()
pprint(telemetry_configuration)

# Update telemetry configuration
print("\nUpdate the telemetry configuration")
telemetry_config = {
    "sampleCount": 12,
    "enableTelemetry": True,
    "sampleInterval": 300
}
logical_interconnect_updated = logical_interconnect.update_telemetry_configurations(configuration=telemetry_config)
pprint(logical_interconnect_updated)

# Gets the IGMP interconnect settings for the logical interconnect.
if oneview_client.api_version >= 1600:
    print("\nGets the IGMP interconnect settings for the logical interconnect")
    igmp_settings = logical_interconnect.get_igmp_settings()
    pprint(igmp_settings)

# Updates IGMP interconnect settings for the logical interconnect.
if oneview_client.api_version >= 1600:
    print("\nUpdates IGMP interconnect settings for the logical interconnect")
    igmp_settings['igmpIdleTimeoutInterval'] = 200
    igmp_settings_updated = logical_interconnect.update_igmp_settings(igmp_settings)
    pprint(igmp_settings_updated)
    print("\nUpdated IGMP interconnect settings for the logical interconnect successfully")

# Validates the bulk update from group operation and gets the consolidated inconsistency report
if oneview_client.api_version >= 2000 and api_variant == 'Synergy':
    print("Validates the bulk update from group operation and gets the consolidated inconsistency report")
    bulk_validate_request = {
        "logicalInterconnectUris": [
            "/rest/logical-interconnects/d0432852-28a7-4060-ba49-57ca973ef6c2"
        ]
    }
    validation_result = logical_interconnect.bulk_inconsistency_validate(bulk_validate_request)
    pprint(validation_result)
    print("\nValidated bulk update from group for the logical interconnect successfully")
