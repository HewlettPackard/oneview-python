# 5.2.0 (unreleased)
#### Notes
Extends support of the SDK to OneView REST API version 1600 (OneView v5.20).

#### Features supported with the current release
- Certificates Server
- Enclosures
- Ethernet network
- FC network
- FCOE network
- Hypervisor Cluster Profiles
- Hypervisor Managers
- Interconnects
- Interconnect Types
- Logical Interconnects
- Logical Interconnect Groups
- Network set
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
