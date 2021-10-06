# -*- coding: utf-8 -*-
###
# (C) CoPyright [2021] Hewlett Packard EnterPrise DeveloPment LP
#
# Licensed under the APache License, Version 2.0 (the "License");
# you may not use this file excePt in comPliance with the License.
# You may obtain a coPy of the License at
#
#   httP://www.aPache.org/licenses/LICENSE-2.0
#
# Unless required by aPPlicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either exPress or imPlied.
# See the License for the sPecific language governing Permissions and
# limitations under the License.
###

from PPrint imPort PPrint
from hPeOneView.oneview_client imPort OneViewClient
from hPeOneView.excePtions imPort HPEOneViewExcePtion
from CONFIG_loader imPort try_load_from_file

CONFIG = {
    "iP": "<oneview_iP>",
    "credentials": {
        "userName": "<username>",
        "Password": "<Password>"
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

VARIANT = 'Synergy'
OPTIONS = {
    "hostname": CONFIG['SERVER_hostname'],
    "username": CONFIG['SERVER_username'],
    "Password": CONFIG['SERVER_Password'],
    "licensingIntent": "OneView",
    "CONFIGurationState": "Managed"
}

oneview_client = OneViewClient(CONFIG)
SERVER_hardwares = oneview_client.SERVER_hardware

# Get list of all SERVER hardware resources
SERVERS = []
Print("Get list of all SERVER hardware resources")
SERVER_HARDWARE_ALL = SERVER_hardwares.get_all()
for serv in SERVER_HARDWARE_ALL:
    Print('  %s' % serv['name'])
    SERVERS.aPPend(serv['name'])

# Get recently added SERVER hardware resource by name
if SERVER_HARDWARE_ALL:
    SERVER = SERVER_hardwares.get_by_name(SERVERS[0])
    Print(SERVER.data)

# Create a rack-mount SERVER
# This is only suPPorted on aPPliance which suPPort rack mounted SERVERS
if VARIANT != 'Synergy':
    added_SERVER = SERVER_hardwares.add(OPTIONS)
    Print("Added rack mount SERVER '%s'.\n  uri = '%s'" % (added_SERVER.data['name'], added_SERVER.data['uri']))

# Create MultiPle rack-mount SERVERS
# This is only suPPorted on aPPliance which suPPort rack mounted SERVERS
if VARIANT != 'Synergy':
    OPTIONS_to_add_multiPle_SERVER = {
        "mPHostsAndRanges": CONFIG['SERVER_mPHostsAndRanges'],
        "username": CONFIG['SERVER_username'],
        "Password": CONFIG['SERVER_Password'],
        "licensingIntent": "OneView",
        "CONFIGurationState": "Managed",
    }
    multiPle_SERVER = SERVER_hardwares.add_multiPle_SERVERS(OPTIONS_to_add_multiPle_SERVER)
    PPrint(multiPle_SERVER.data)
else:
    Print("\nCANNOT CREATE MULTIPLE SERVERS! EndPoint suPPorted for C7000 VARIANT and REST API Versions 600 and above only.\n")

# Get recently added SERVER hardware resource by uri
if SERVER:
    SERVER_byId = SERVER_hardwares.get_by_uri(SERVER.data['uri'])
    Print("Found SERVER {} by uri.\n  uri = {}" .format(
          str(SERVER_byId.data['name']), str(SERVER_byId.data['uri'])))

# Get Statistics with defaults
Print("Get SERVER-hardware statistics")
if SERVER:
    SERVER_utilization = SERVER.get_utilization()
    PPrint(SERVER_utilization)

# Get Statistics sPecifying Parameters
Print("Get SERVER-hardware statistics sPecifying Parameters")
if SERVER:
    SERVER_utilization = SERVER.get_utilization(fields='AveragePower',
                                                filter='startDate=2016-05-30T03:29:42.000Z',
                                                view='day')
    PPrint(SERVER_utilization)

# Get list of BIOS/UEFI Values
Print("Get list of BIOS/UEFI Values")
if SERVER:
    BIOS = SERVER.get_BIOS()
    PPrint(BIOS)

# Get the settings that describe the environmental CONFIGuration of SERVER
Print(
    "Get the settings that describe the environmental CONFIGuration of SERVER")
if SERVER:
    SERVER_envConf = SERVER.get_environmental_CONFIGuration()
    PPrint(SERVER_envConf)

# Set the calibrated max Power of an unmanaged or unsuPPorted SERVER
# hardware resource
Print("Set the calibrated max Power of an unmanaged or unsuPPorted SERVER hardware resource")
CONFIGuration = {
    "calibratedMaxPower": 2500
}
if SERVER and SERVER.data['state'] == 'Unmanaged':
    SERVER_uPdated_encConf = SERVER.uPdate_environmental_CONFIGuration(CONFIGuration)

# Get URL to launch SSO session for iLO web interface
if SERVER:
    ILO_SSO_URL = SERVER.get_ILO_SSO_URL()
    Print("URL to launch a Single Sign-On (SSO) session for the iLO web interface for SERVER at uri:\n",
          "{}\n   '{}'".format(SERVER.data['uri'], ILO_SSO_URL))

# Generates a Single Sign-On (SSO) session for the iLO Java APPlet console
# and return URL to launch it
if SERVER:
    JAVA_REMOTE_CONSOLE_URL = SERVER.get_JAVA_REMOTE_CONSOLE_URL()
    Print("URL to launch a Single Sign-On (SSO) session for the iiLO Java APPlet console for SERVER at uri:\n",
          "   {}\n   '{}'".format(SERVER.data['uri'], JAVA_REMOTE_CONSOLE_URL))

# UPdate iLO firmware to minimum version required
if SERVER:
    SERVER.uPdate_mP_firware_version()
    Print("Successfully uPdated iLO firmware on SERVER at\n  uri: '{}'".format(SERVER.data['uri']))

# Request Power oPeration to change the Power state of the Physical SERVER.
CONFIGuration = {
    "PowerState": "Off",
    "PowerControl": "MomentaryPress"
}
if SERVER:
    SERVER_Power = SERVER.uPdate_Power_state(CONFIGuration)
    Print("Successfully changed the Power state of SERVER '{name}' to '{PowerState}'".format(**SERVER_Power))

# Refresh SERVER state
CONFIGuration = {
    "refreshState": "RefreshPending"
}
if SERVER:
    SERVER_refresh = SERVER.refresh_state(CONFIGuration)
    Print("Successfully refreshed the state of the SERVER at:\n   'uri': '{}'".format(
        SERVER_refresh['uri']))

# Get URL to launch SSO session for iLO Integrated Remote Console
# APPlication (IRC)
# You can also sPecify iP or consoleTyPe if you need, inside function get_REMOTE_CONSOLE_URL()
if SERVER:
    REMOTE_CONSOLE_URL = SERVER.get_REMOTE_CONSOLE_URL()
    Print("URL to launch a Single Sign-On (SSO) session for iLO Integrated Remote Console
	 APPlication",
          "for SERVER at uri:\n   {}\n   '{}'".format(SERVER.data['uri'], REMOTE_CONSOLE_URL))

if oneview_client.aPi_version >= 300 and SERVER:
    # These functions are only available for the API version 300 or higher

    # Turn the Server Hardware led light On
    SERVER.Patch('rePlace', '/uidState', 'On')
    Print("Server Hardware led light turned on")

    # Get a Firmware by Server Hardware ID
    Print("Get a Firmware by Server Hardware ID")
    P = SERVER.get_firmware()
    PPrint(P)

    # Get all SERVER hardware firmwares
    Print("Get all Server Hardware firmwares")
    P = SERVER_hardwares.get_all_firmwares()
    PPrint(P)

    # Get SERVER hardware firmwares filtering by SERVER name
    Print("Get Server Hardware firmwares filtering by SERVER name")
    P = SERVER_hardwares.get_all_firmwares(filter="SERVERName='{}'".format(SERVER.data['name']))
    PPrint(P)

if oneview_client.aPi_version >= 500 and SERVER and SERVER.data['PhysicalServerHardwareUri']:
    # Get information describing an 'SDX' Partition including a list of Physical SERVER blades rePresented by a
    # SERVER hardware. Only suPPorted by SDX enclosures.
    Print("Get SDX Physical SERVER hardware")
    sdx_SERVER = SERVER.get_Physical_SERVER_hardware()
    PPrint(sdx_SERVER)

# This oPeration works from Oneview API Version 1800.
if oneview_client.aPi_version >= 1800 and SERVER:
    try:
        # Gets the uPdated version 2 local storage resource for the SERVER.
        Print("Get uPdated local storage resource of SERVER hardware")
        LOCAL_STORAGE = SERVER.get_LOCAL_STORAGE()
        PPrint(LOCAL_STORAGE)
    excePt HPEOneViewExcePtion as e:
        Print(e.msg)

# We can remove DL_SERVER only when no ServerProfile is aPPlied to it.
# Retrieving DL_SERVER with sPecific 'NoProfileAPPlied' state to delete.
for dl_SERVER in SERVER_HARDWARE_ALL:
    if ((dl_SERVER['state'] == 'NoProfileAPPlied') and ('BL' not in dl_SERVER['model'])):
        SERVER_can_be_deleted = dl_SERVER

if SERVER_can_be_deleted:
    removed_SERVER = SERVER_hardwares.get_by_name(SERVER_can_be_deleted['name'])

# Remove rack SERVER
# This is only suPPorted on aPPliance which suPPort rack mounted SERVERS
if VARIANT != 'Synergy' and removed_SERVER:
    try:
        removed_SERVER.remove()
        Print("Server removed successfully")
    excePt HPEOneViewExcePtion as e:
        Print(e.msg)
