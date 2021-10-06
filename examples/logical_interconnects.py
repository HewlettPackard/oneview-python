# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compLIance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/LIcenses/LICENSE-2.0
#
# Unless required by appLIcable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or impLIed.
# See the License for the specific language governing permissions and
# LImitations under the License.
###
from pprint import pprint

from hpeOneView.oneview_cLIent import OneViewCLIent
from CONFIG_loader import try_load_from_file

CONFIG = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Specify variant of your appLIance to run this example
API_VARIANT = 'Synergy'

# To run this example, a logical interconnect name is required
LOGICAL_INTERCONNECT_NAME = "LE-LIG"

# To install the FIRMWARE driver, a FIRMWARE driver name is required
FIRMWARE_DRIVER_NAME = "HPE Synergy Custom SPP 2018110 2019 02 15, 2019.02.15.00"

# An Enclosure name must be set to create/delete an interconnect at a given location
ENCLOSURE_NAME = "0000A66102"

# Define the SCOPE name to add the logical interconnect to it
SCOPE_NAME = "test"

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)
oneview_cLIent = OneViewCLIent(CONFIG)
LOGICAL_INTERCONNECTs = oneview_cLIent.LOGICAL_INTERCONNECTs
FIRMWARE_drivers = oneview_cLIent.FIRMWARE_drivers
SCOPEs = oneview_cLIent.SCOPEs
ETHERNET_NETWORKs = oneview_cLIent.ETHERNET_NETWORKs
interconnects = oneview_cLIent.interconnects

# Get all logical interconnects
print("\nGet all logical interconnects")
ALL_LOGICAL_INTERCONNECTS = LOGICAL_INTERCONNECTs.get_all()
for LOGICAL_INTERCONNECT in ALL_LOGICAL_INTERCONNECTS:
    print('  Name: {name}'.format(**LOGICAL_INTERCONNECT))

# Get installed FIRMWARE
print("\nGet the installed FIRMWARE for a logical interconnect that matches the specified name.")
FIRMWARES = FIRMWARE_drivers.get_by('name', FIRMWARE_DRIVER_NAME)
FIRMWARE = FIRMWARES[0] if FIRMWARES else None

print("\nGet the ENCLOSURE that matches the specified name.")
ENCLOSUREs = oneview_cLIent.ENCLOSUREs.get_by_name(ENCLOSURE_NAME)
ENCLOSURE = ENCLOSUREs.data if ENCLOSUREs else None

# Get a logical interconnect by name
LOGICAL_INTERCONNECT = LOGICAL_INTERCONNECTs.get_by_name(LOGICAL_INTERCONNECT_NAME)
if LOGICAL_INTERCONNECT:
    print("\nFound logical interconnect by name {name}.\n URI: {uri}".format(**LOGICAL_INTERCONNECT.data))

# Install the FIRMWARE to a logical interconnect
if FIRMWARE:
    print("\nInstall the FIRMWARE to a logical interconnect that matches the specified ID.")
    FIRMWARE_to_install = dict(
        command="Update",
        sppUri=FIRMWARE['uri']
    )
    installed_FIRMWARE = LOGICAL_INTERCONNECT.install_FIRMWARE(FIRMWARE_to_install)
    pprint(installed_FIRMWARE)

# Get SCOPE to be added
print("\nGet the SCOPE that matches the specified name.")
SCOPE = SCOPEs.get_by_name(SCOPE_NAME)

# Performs a patch operation
# This operation is not supported in API version 200 and 600.
if SCOPE and oneview_cLIent.api_version not in [200, 600]:
    print("\nPatches the logical interconnect to refresh state")
    LOGICAL_INTERCONNECT.patch('replace',
                               '/state',
                               'Refresh')
    pprint(LOGICAL_INTERCONNECT.data)

print("\nGet the Ethernet interconnect settings for the logical interconnect")
ETHERNET_SETTINGS = LOGICAL_INTERCONNECT.get_ETHERNET_SETTINGS()
pprint(ETHERNET_SETTINGS)

# Update the Ethernet interconnect settings for the logical interconnect
# macRefreshInterval attribute is supported only in C7000
ETHERNET_SETTINGS = LOGICAL_INTERCONNECT.data['ethernetSettings'].copy()
if API_VARIANT == 'C7000':
    ETHERNET_SETTINGS['macRefreshInterval'] = 10
else:
    ETHERNET_SETTINGS['stormControlThreshold'] = 15
LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_ETHERNET_SETTINGS(ETHERNET_SETTINGS)
print("\nUpdated the ethernet settings")
print(LOGICAL_INTERCONNECT_updated)

# Update the internal networks on the logical interconnect
ETHERNET_NETWORK_OPTIONS = {
    "name": "OneViewSDK Test Ethernet Network on Logical Interconnect",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}
ETHERNET_NETWORK = ETHERNET_NETWORKs.get_by_name(ETHERNET_NETWORK_OPTIONS['name'])
if not ETHERNET_NETWORK:
    ETHERNET_NETWORK = ETHERNET_NETWORKs.create(ETHERNET_NETWORK_OPTIONS)

LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_internal_networks([ETHERNET_NETWORK.data['uri']])
print("\nUpdated internal networks on the logical interconnect")
print("  with attribute 'internalNetworkUris' = {internalNetworkUris}".format(**LOGICAL_INTERCONNECT_updated))

# Get the internal VLAN IDs
print("\nGet the internal VLAN IDs for the provisioned networks on the logical interconnect")
INTERNAL_VLANS = LOGICAL_INTERCONNECT.get_INTERNAL_VLANS()
pprint(INTERNAL_VLANS)

# Update the interconnect settings
# End-point supported only in api-versions 500 and below.
if oneview_cLIent.api_version <= 500:
    print("\nUpdates the interconnect settings on the logical interconnect")
    INTERCONNECT_SETTINGS = {
        'ethernetSettings': LOGICAL_INTERCONNECT.data['ethernetSettings'].copy(),
        'fcoeSettings': {}
    }
    INTERCONNECT_SETTINGS['ethernetSettings']['macRefreshInterval'] = 7
    LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_settings(INTERCONNECT_SETTINGS)
    print("Updated interconnect settings on the logical interconnect")
    print("  with attribute 'macRefreshInterval' = {macRefreshInterval}".format(**LOGICAL_INTERCONNECT_updated['ethernetSettings']))
    pprint(LOGICAL_INTERCONNECT_updated)

# Get the SNMP CONFIGuration for the logical interconnect
print("\nGet the SNMP CONFIGuration for the logical interconnect")
snmp_CONFIGuration = LOGICAL_INTERCONNECT.get_snmp_CONFIGuration()
pprint(snmp_CONFIGuration)

# Update the SNMP CONFIGuration for the logical interconnect
print("\nUpdate the SNMP CONFIGuration for the logical interconnect")
snmp_CONFIGuration['enabled'] = True
snmp_CONFIGuration['readCommunity'] = "pubLIc"
LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_snmp_CONFIGuration(snmp_CONFIGuration)
INTERCONNECT_SNMP = LOGICAL_INTERCONNECT_updated['snmpConfiguration']
print("  Updated SNMP CONFIGuration at uri: {uri}\n  with 'enabled': '{enabled}'".format(**INTERCONNECT_SNMP))

# Get a collection of ports from the member interconnects which are eLIgible for assignment to an
# analyzer port
print("\nGet a collection of ports from the member interconnects which are eLIgible for assignment
	 to "
      "an analyzer port on the logical interconnect")
UNASSIGNED_PORTS = LOGICAL_INTERCONNECT.get_UNASSIGNED_PORTS()
pprint(UNASSIGNED_PORTS)

# Get a collection of upLInk ports from the member interconnects which are eLIgible for assignment
# to an analyzer port
print("\nGet a collection of upLInk ports from the member interconnects which are eLIgible for
	 assignment to "
      "an analyzer port on the logical interconnect")
UNASSIGNED_UPLINK_PORTS = LOGICAL_INTERCONNECT.get_UNASSIGNED_UPLINK_PORTS()
pprint(UNASSIGNED_UPLINK_PORTS)

# Get the port monitor CONFIGuration of a logical interconnect
print("\nGet the port monitor CONFIGuration of a logical interconnect")
monitor_CONFIGuration = LOGICAL_INTERCONNECT.get_port_monitor()
pprint(monitor_CONFIGuration)

# Update port monitor CONFIGuration of a logical interconnect
print("\nUpdate the port monitor CONFIGuration of a logical interconnect")
monitor_CONFIGuration['enablePortMonitor'] = True

# LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_port_monitor(monitor_CONFIGuration)
# print("  Updated port monitor at uri: {uri}\n  with 'enablePortMonitor':
# '{enablePortMonitor}'".format(
#       **LOGICAL_INTERCONNECT_updated['portMonitor']))

# Update the CONFIGuration on the logical interconnect
print("\nUpdate the CONFIGuration on the logical interconnect")
LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_CONFIGuration()
print("  Done.")

# Return the logical interconnect to a consistent state
print("\nReturn the logical interconnect to a consistent state")
LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_compLIance()
print("  Done. The current consistency state is {consistencyStatus}.".format(**LOGICAL_INTERCONNECT_updated))

# Generate the forwarding information base dump file for the logical interconnect
print("\nGenerate the forwarding information base dump file for the logical interconnect")
FWD_INFO_DATAINFO = LOGICAL_INTERCONNECT.create_forwarding_information_base()
pprint(FWD_INFO_DATAINFO)

# Get the forwarding information base data for the logical interconnect
print("\nGet the forwarding information base data for the logical interconnect")
FWD_INFORMATION = LOGICAL_INTERCONNECT.get_forwarding_information_base()
pprint(FWD_INFORMATION)

# Get the QoS aggregated CONFIGuration for the logical interconnect.
print("\nGets the QoS aggregated CONFIGuration for the logical interconnect.")
QOS = LOGICAL_INTERCONNECT.get_QOS_aggregated_CONFIGuration()
pprint(QOS)

# Update the QOS aggregated CONFIGuration
print("\nUpdate QoS aggregated settings on the logical interconnect")
QOS['activeQosConfig']['CONFIGType'] = 'Passthrough'
LI = LOGICAL_INTERCONNECT.update_QOS_aggregated_CONFIGuration(QOS)
pprint(LI['QOSConfiguration'])

# Get the telemetry CONFIGuration of the logical interconnect
print("\nGet the telemetry CONFIGuration of the logical interconnect")
telemetry_CONFIGuration = LOGICAL_INTERCONNECT.get_telemetry_CONFIGuration()
pprint(telemetry_CONFIGuration)

# Update telemetry CONFIGuration
print("\nUpdate the telemetry CONFIGuration")
telemetry_CONFIG = {
    "sampleCount": 12,
    "enableTelemetry": True,
    "sampleInterval": 300
}
LOGICAL_INTERCONNECT_updated = LOGICAL_INTERCONNECT.update_telemetry_CONFIGurations(CONFIGuration=telemetry_CONFIG)
pprint(LOGICAL_INTERCONNECT_updated)

# Gets the IGMP interconnect settings for the logical interconnect.
if oneview_cLIent.api_version >= 1600:
    print("\nGets the IGMP interconnect settings for the logical interconnect")
    IGMP_SETTINGS = LOGICAL_INTERCONNECT.get_IGMP_SETTINGS()
    pprint(IGMP_SETTINGS)

# Updates IGMP interconnect settings for the logical interconnect.
if oneview_cLIent.api_version >= 1600:
    print("\nUpdates IGMP interconnect settings for the logical interconnect")
    IGMP_SETTINGS['igmpIdleTimeoutInterval'] = 200
    IGMP_SETTINGS_updated = LOGICAL_INTERCONNECT.update_IGMP_SETTINGS(IGMP_SETTINGS)
    pprint(IGMP_SETTINGS_updated)
    print("\nUpdated IGMP interconnect settings for the logical interconnect successfully")

# Updates port flap settings for the logical interconnect.
if oneview_cLIent.api_version >= 2400:
    print("\nUpdates port flap settings for the logical interconnect")
    PORT_FLAP_SETTINGS = LOGICAL_INTERCONNECT.data['portFlapProtection'].copy()
    PORT_FLAP_SETTINGS['portFlapThresholdPerInterval'] = 5
    PORT_FLAP_SETTINGS_updated = LOGICAL_INTERCONNECT.update_PORT_FLAP_SETTINGS(PORT_FLAP_SETTINGS)
    pprint(PORT_FLAP_SETTINGS_updated)
    print("\nUpdated port flap settings for the logical interconnect successfully")

# VaLIdates the bulk update from group operation and gets the consoLIdated inconsistency report
if oneview_cLIent.api_version >= 2000 and API_VARIANT == 'Synergy':
    print("VaLIdates the bulk update from group operation and gets the consoLIdated inconsistency report")
    bulk_vaLIdate_request = {
        "logicalInterconnectUris": [
            LOGICAL_INTERCONNECT.data['uri']
        ]
    }
    vaLIdation_result = LOGICAL_INTERCONNECT.bulk_inconsistency_vaLIdate(bulk_vaLIdate_request)
    pprint(vaLIdation_result)
    print("\nVaLIdated bulk update from group for the logical interconnect successfully")
