# 5.0.0
#### Notes
Extends support of the SDK to OneView REST API version 1200 (OneView v5.00).

#### Major changes
 1. Extending support of the SDK to API version 1200.
 2. Refactored base classes to make resource data available with the resource object.
    This will help to add more helper methods for the resources and hide data complexity from the user.
 3. Introduced mixin classes to include the optional features of the resources.

#### Breaking
  Enhancement made in this version breaks the previous version of the SDK.
  From this version onwards, create/update/get_by_name/get_by_id will return an object of the resource instead of data.

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
- Network set
- Storage volume

# TODO: Move the below resources to the above list once the resource module is updated to use API versions 1000 and 1200
- Connection template
- Enclosure
- Enclosure group
- Ethernet network
- FC network
- FCOE network
- Interconnect type
- Internal link set
- Logical enclosure
- Logical interconnect
- Logical interconnect group
- Logical switch group
- Managed SAN
- OS deployment plan
- SAS interconnect
- SAS interconnect type
- SAS logical interconnect
- SAS logical interconnect group
- Server hardware
- Server hardware type
- Server profile
- Server profile template
- Switch type
- Uplink set
