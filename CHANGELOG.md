# 6.3.0(unreleased)
#### Notes
Extends support of the SDK to OneView REST API version 3200 (OneView v6.30)

##### Features supported with the current release
- Appliance Proxy Configuration
- Firmware Bundles

# 6.2.0
#### Notes
Extends support of the SDK to OneView REST API version 3000 (OneView v6.20)

#### Bug fixes & Enhancements
- [#157] (https://github.com/HewlettPackard/oneview-python/issues/157) Add appliance ha-nodes endpoint to sdk

##### Features supported with the current release
- Appliance Configuration Timeconfig
- Appliance Health Status
- Appliance Node Information
- Appliance SNMPv1 Trap Destinations
- Appliance SNMPv3 Trap Destinations
- Appliance SNMPv3 Users
- Appliance SSH Access
- Appliance Time and Locale Configuration
- Connection Templates
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- HA Nodes
- Hypervisor Cluster Profiles
- Hypervisor Managers
- ID Pools
- ID Pool IPv4 Range
- ID Pool IPv4 Subnets
- Index Resources
- Interconnects
- Interconnect Types
- Labels 
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Group
- Network set
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volume
- Tasks
- Uplink set
- Users
- Version

# 6.1.0
#### Notes
Extends support of the SDK to OneView REST API version 2800 (OneView v6.10) and ImageStreamer REST API version 2020 (I3S v6.10).

#### Bug fixes & Enhancements
- [#139] (https://github.com/HewlettPackard/oneview-python/issues/139) Hardware needs attachment to existing SCOPE and PROFILE
- [#140] (https://github.com/HewlettPackard/oneview-python/issues/140) Detach a profile from the hardware resource
- [#145] (https://github.com/HewlettPackard/oneview-python/issues/145) get_by_uri() method in scope is not listing few category resources like drive-enclosures & sas-interconnects

#### Features supported

- Appliance Configuration Timeconfig
- Appliance SNMPv1 Trap Destinations
- Appliance SNMPv3 Trap Destinations
- Appliance SNMPv3 Users
- Appliance SSH Access
- Appliance Time and Locale Configuration
- Artifact Bundles
- Certificates Server
- Connection Templates
- Deployment Plans
- Deployment Groups
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- Golden Images
- Hypervisor Cluster Profiles
- Hypervisor Managers
- ID Pools
- ID Pool IPv4 Range
- ID Pool IPv4 Subnets
- Index Resources
- Interconnects
- Interconnect Types
- Lables
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Group
- Network set
- OS Build Plans
- OS Deployment Plans
- OS Volumes
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volume 
- Tasks
- Uplink set
- Users
- Version

# 6.0.0
#### Notes
Extends support of the SDK to OneView REST API version 2600 (OneView v6.00) and ImageStreamer REST API version 2010 (I3S v6.00).

#### Features supported
- Appliance Configuration Timeconfig
- Appliance SNMPv1 Trap Destinations
- Appliance SNMPv3 Trap Destinations
- Appliance SNMPv3 Users
- Appliance SSH Access
- Appliance Time and Locale Configuration
- Artifact Bundles
- Certificates Server
- Connection Templates
- Deployment Plans
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- Hypervisor Cluster Profiles
- Hypervisor Managers
- ID Pools
- ID Pool IPv4 Range
- ID Pool IPv4 Subnets
- Interconnects
- Interconnect Types
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Group
- Network set
- OS Deployment Plans
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volume 
- Tasks
- Uplink set

# 5.6.0
#### Notes
Extends support of the SDK to OneView REST API version 2400 (OneView v5.60).

#### Bug fixes & Enhancements
- [#110] (https://github.com/HewlettPackard/oneview-python/issues/110) certificate_authority.get() does not return certificate string

#### Features supported with the current release
- Appliance SNMPv1 Trap Destinations
- Connection Templates
- Certificates Server
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- Hypervisor Cluster Profiles
- Hypervisor Managers
- Interconnects
- Interconnect Types
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Group
- Network set
- OS Deployment Plans
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volume 
- Tasks
- Uplink set

# 5.5.0
#### Notes
Extends support of the SDK to OneView REST API version 2200 (OneView v5.50) and ImageStreamer REST API version 2000 (I3S v5.40).

#### Bug fixes & Enhancements
- [#103] (https://github.com/HewlettPackard/oneview-python/issues/103) enclosure_groups.create() Does not take valid data and returns JSON error.

#### Features supported with the current release
- Appliance SNMPv1 Trap Destinations
- Artifact Bundles
- Certificates Server
- Connection Templates
- Deployment plan
- Enclosures
- Enclosure Groups
- Ethernet Network
- FC Network
- FCoE Network
- Firmware Drivers
- Hypervisor Cluster Profiles
- Hypervisor Managers
- Interconnect Types
- Interconnects
- Logical Enclosures
- Logical Interconnect Groups
- Logical Interconnects
- Network Sets
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profile Templates
- Server Profiles
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volumes
- Tasks
- Uplink Sets

# 5.4.0
#### Notes
Extends support of the SDK to OneView REST API version 2000 (OneView v5.40).

#### Breaking Changes
  Enhancement made in this version breaks the previous version of the SDK.
  From this version onwards, hpOneView module name is renamed to hpeOneView and all the oneview libraries and examples will import the hpeOneView module as parent.

  E.g.
```
       from hpeOneView.oneview_client import OneViewClient
       oneview_client = OneViewClient(config)              # Create OneView client
       fc_networks = oneview_client.fc_networks            # Get FCNetowrk resource client
```

#### Major changes
- Refactored base class to take default API version as per provided Oneview appliance.
- Removed provision of "type" field as those are optional from API1600.
- Added support for automatic publish of Docker Image when there is a new release in GitHub

#### Features supported with the current release
- Appliance SNMPv1 Trap Destinations
- Connection Templates
- Certificates Server
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- Hypervisor Cluster Profiles
- Hypervisor Managers
- Interconnects
- Interconnect Types
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Group
- Network set
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volume 
- Tasks
- Uplink set

#### Bug fixes & Enhancements
- [#81](https://github.com/HewlettPackard/oneview-python/issues/81) EthernetNetworks Update does not work.
- [#91](https://github.com/HewlettPackard/oneview-python/issues/91) Change Password Sample?


# 5.3.0
#### Notes
Extends support of the SDK to OneView REST API version 1800 (OneView v5.30).

#### Features supported with the current release
- Appliance SNMPv1 Trap Destinations
- Certificates Server
- Connection Templates
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- Hypervisor Cluster Profiles
- Hypervisor Managers
- Interconnects
- Interconnect Types
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Group
- Network set
- Restores
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Pools
- Storage Systems
- Storage Templates
- Storage Volume Attachments
- Storage Volume 
- Tasks
- Uplink set

# 5.2.1
#### Notes
Added support to OneView 'Restores' feature for REST API versions 800, 1000, 1200 and 1600.
Added code to handle login acknowledgement.

#### Bug fixes & Enhancements
- [#21](https://github.com/HewlettPackard/oneview-python/issues/21) In correct endpoint passed when uploading a downloaded appliance backup
- [#23](https://github.com/HewlettPackard/oneview-python/issues/23) MISSING_JSON_TYPE error code is thrown when attempting to restore the appliance
- [#58](https://github.com/HewlettPackard/oneview-python/issues/58) loginMsgAck is not handled in python code
- [#60](https://github.com/HewlettPackard/oneview-python/issues/60) SPT type for api1600 should be ServerProfileTemplateV8
- [#67](https://github.com/HewlettPackard/oneview-python/issues/67) raise exception with proper error message when ip is not provided in config

# 5.2.0
#### Notes
Extends support of the SDK to OneView REST API version 1600 (OneView v5.20).

#### Features supported with the current release
- Appliance SNMPv1 Trap Destinations
- Artifact Bundles
- Certificates Server
- Deployment plan
- Enclosures
- Enclosure Groups
- Ethernet network
- FC network
- FCOE network
- Firmware Drivers
- Hypervisor Cluster Profiles
- Hypervisor Managers
- Interconnects
- Interconnect Types
- Logical Enclosures
- Logical Interconnects
- Logical Interconnect Groups
- Network set
- Scopes
- Server Hardware
- Server Hardware Types
- Server Profiles
- Server Profile Templates
- Storage Systems
- Storage Pools
- Storage Templates
- Storage Volume Attachments
- Storage Volume
- Tasks
- Uplink set

# 5.1.1

#### Bug fixes & Enhancements
- #34 Handle exception of get_by_aliasname method in certificates_server resource and return resource object

# 5.1.0
#### Notes
Extends support of the SDK to OneView REST API version 800, 1000 and 1200.

#### Features supported
- Certificates Server
- Hypervisor Cluster Profiles
- Hypervisor Managers

# 5.0.0
#### Notes
Extends support of the SDK to OneView REST API version 1200 (OneView v5.00).

#### Major changes
 1. Extending support of the SDK to API version 1200.
 2. Refactored base classes to make resource data available with the resource object.
    This will help to add more helper methods for the resources and hide data complexity from the user.
 3. Introduced mixin classes to include the optional features of the resources.
 4. Added below methods for all the resources by introducing a base class for the resource client classes.
    Appropriate exception will be raised, if any of the features are not available for a resource.
    
    | Method              | Returns                                       |
    | ------------------  | --------------------------------------------- |
    | create              |   resource object                             |
    | update              |   resource object                             |
    | delete              |   boolean                                     |
    | get_all             |   list of resource data                       |
    | get_by_name         |   resource object                             |
    | get_by_uri          |   resource object                             |
    | get_by              |   resource data                               |
    
#### Breaking
  Enhancement made in this version breaks the previous version of the SDK.
  From this version onwards, create/update/get_by_name/get_by_uri will return an object of the resource instead of data.

  E.g.
```
       oneview_client = OneViewClient(config)              # Create OneView client
       fc_networks = oneview_client.fc_networks            # Get FCNetowrk resource client
       fc_network = fc_networks.get_by_name(name) / create # Get an existing FCNetwork's object by it's name or create one
       fc_network.update(update_data)                      # Update FCNetwork
       fc_network.delete()                                 # Delete FCNetwork
```
  Refer example directory for more examples.

#### Features supported with the current release
- Connection template
- Deployment plan
- Enclosure
- Enclosure group
- Ethernet network
- FC network
- FCOE network
- Interconnect
- Interconnect type
- Internal link set
- Logical enclosure
- Logical switch group
- Logical interconnect
- Logical interconnect group
- Managed SAN
- Network set
- OS deployment plan
- SAS interconnect
- SAS interconnect type
- SAS logical interconnect
- SAS logical interconnect group
- Network set
- Server hardware
- Server hardware type
- Server profile
- Server profile template
- Storage pool
- Storage system
- Storage volume
- Storage volume attachment
- Storage volume template
- Switch type
- Uplink set
