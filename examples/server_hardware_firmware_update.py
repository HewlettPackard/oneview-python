from hpeOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
        "server_hardware_hostname": "",
        "server_hardware_username": "",
        "server_hardware_password": "",
        "variant": "",
        "firmware_baseline_id": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware
firmware_drivers = oneview_client.firmware_drivers

# Get all firmwares
print("\nGet list of firmwares managed by the appliance.")
all_firmwares = firmware_drivers.get_all()
for firmware in all_firmwares:
    print('  - {}'.format(firmware['name']))

firmware_driver = firmware_drivers.get_by_uri(all_firmwares[1]['uri'])
firmwareBaselineId = firmware_driver.data['resourceId']
server = server_hardwares.get_by_name("<server name>")

# Get list of all server hardware resources
servers = []
print("Get list of all server hardware resources")
server_hardware_all = server_hardwares.get_all()
for serv in server_hardware_all:
    print('  %s' % serv['name'])
    servers.append(serv['name'])

# Get recently added server hardware resource by name
if server_hardware_all:
    server = server_hardwares.get_by_name(servers[0])
    print(server.data)

# Request power operation to change the power state of the physical server.
configuration = {
    "powerState": "Off",
    "powerControl": "MomentaryPress"
}
if server:
    server_power = server.update_power_state(configuration)
    print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))

# Perform a firmware update on server
# Firmware update can only be done on server hardware(Gen10 and later) with no server profile assigned, and server hardware
# should be in powered off state

#configuration 
compliance_configuration = {
    "firmwareBaselineId": firmwareBaselineId,
    "serverUUID": server.data['uuid']
}
#state 

firmware_update_configuration = [{"op": "replace", "value": {"baselineUri": "/rest/firmware-drivers/" + firmwareBaselineId,
                                  "firmwareInstallType": "FirmwareOnlyOfflineMode", "installationPolicy": "LowerThanBaseline"}
                                  }]
# if server loop 
        
if oneview_client.api_version >=4600:
    if server:
        print("Checking if firmware compliance required..")
        firmware_compliance = server.check_firmware_compliance(compliance_configuration)
        print(firmware_compliance['serverFirmwareUpdateRequired'])
        if firmware_compliance['serverFirmwareUpdateRequired']:
            print("Updating firmware for the server hardware..")
            server.perform_firmware_update(firmware_update_configuration)
        else:
            print("Firmware update is not required for this server")
else:
    print("Firmware update feature is supported only for api version above 4600")