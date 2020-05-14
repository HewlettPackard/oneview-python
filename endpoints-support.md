***Legend***

| Item | Meaning |
| ------------------ | --------------------------------------------- |
|  :white_check_mark: | Endpoint implemented in the Python SDK and tested for this API version :tada: |
|  :heavy_multiplication_x:  | Endpoint considered as 'out-of-scope' for the Python SDK               |
|  :heavy_minus_sign: | Endpoint not available for this API Version |

<br />

***Notes***

* If an endpoint is marked as implemented in a previous version of the API, it will likely already be working for newer API versions, however in these cases it is important to:
1. Specify the 'type' of the resource when using an untested API, as it will not get set by default
2. If an example is not working, verify the [HPE OneView REST API Documentation](https://techlibrary.hpe.com/docs/enterprise/servers/oneview5.0/cicf-api/en/index.html) for the API version being used, since the expected attributes for that resource might have changed.

<br />

## HPE OneView

| Endpoints                                                                               | Verb     |  V800                 | V1000               | V1200                | V1600               |
| --------------------------------------------------------------------------------------- | -------- |  :------------------: | :------------------:| :------------------: | :-----------------: |
|     **Connection Templates**
|<sub>/rest/connection-templates</sub>                                                    |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/connection-templates/defaultConnectionTemplate</sub>                          |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/connection-templates/{id}</sub>                                               |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/connection-templates/{id}</sub>                                               |PUT       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Certificates Server**
|<sub>/rest/certificates/servers</sub>                                                    |POST      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/certificates/https/remote/example.com</sub>                                   |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/certificates/servers/{aliasName}</sub>                                        |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/certificates/servers/{aliasName}</sub>                                        |PUT       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/certificates/servers/{aliasName}</sub>                                        |DELETE    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Enclosure Groups**
|<sub>/rest/enclosure-groups</sub>                                                        | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosure-groups</sub>                                                        | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosure-groups/{id}</sub>                                                   | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosure-groups/{id}</sub>                                                   | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosure-groups/{id}</sub>                                                   | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosure-groups/{id}/script</sub>                                            | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosure-groups/{id}/script</sub>                                            | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Enclosures**
|<sub>/rest/enclosures</sub>                                                              | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures</sub>                                                              | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}</sub>                                                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}</sub>                                                         | PATCH    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}</sub>                                                         | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/configuration</sub>                                           | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/environmentalConfiguration</sub>                              | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/environmentalConfiguration</sub>                              | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/refreshState</sub>                                            | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/script</sub>                                                  | GET      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/enclosures/{id}/sso</sub>                                                     | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/utilization</sub>                                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/https/certificaterequest</sub>                                | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/https/certificaterequest</sub>                                | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/enclosures/{id}/https/certificaterequest</sub>                                | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Ethernet Networks**
|<sub>/rest/ethernet-networks</sub>                                                       | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks</sub>                                                       | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks/bulk</sub>                                                  | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks/{id}</sub>                                                  | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks/{id}</sub>                                                  | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks/{id}</sub>                                                  | PATCH    |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |  :heavy_minus_sign:   |
|<sub>/rest/ethernet-networks/{id}</sub>                                                  | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks/{id}/associatedProfiles</sub>                               | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/ethernet-networks/{id}/associatedUplinkGroups</sub>                           | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **FC Networks**
|<sub>/rest/fc-networks</sub>                                                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fc-networks</sub>                                                             | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fc-networks/{id}</sub>                                                        | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fc-networks/{id}</sub>                                                        | PATCH    |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |  :heavy_minus_sign:   |
|<sub>/rest/fc-networks/{id}</sub>                                                        | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fc-networks/{id}</sub>                                                        | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **FCoE Networks**
|<sub>/rest/fcoe-networks</sub>                                                           | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fcoe-networks</sub>                                                           | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fcoe-networks/{id}</sub>                                                      | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fcoe-networks/{id}</sub>                                                      | PATCH    |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |  :heavy_minus_sign:   |
|<sub>/rest/fcoe-networks/{id}</sub>                                                      | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/fcoe-networks/{id}</sub>                                                      | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Hypervisor Cluster Profiles**
|<sub>/rest/hypervisor-cluster-profiles</sub>                                             |POST      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-cluster-profiles</sub>                                             |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-cluster-profiles/{id}</sub>                                        |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-cluster-profiles/{id}</sub>                                        |PUT       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-cluster-profiles/{id}</sub>                                        |DELETE    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-cluster-profiles/virtualswitch-layout</sub>                        |POST      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-cluster-profiles/{id}/compliance-preview</sub>                     |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Hypervisor Managers**
|<sub>/rest/hypervisor-managers</sub>                                                     |POST      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-managers</sub>                                                     |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-managers/{id}</sub>                                                |GET       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-managers/{id}</sub>                                                |PUT       |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/hypervisor-managers/{id}</sub>                                                |DELETE    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Interconnects**
|<sub>/rest/interconnects</sub>                                                           | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}</sub>                                                      | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}</sub>                                                      | PATCH    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/configuration</sub>                                        | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/pluggableModuleInformation</sub>                           | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/ports</sub>                                                | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/ports</sub>                                                | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/ports/{portId:.+}</sub>                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/resetportprotection</sub>                                  | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/statistics</sub>                                           | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/statistics/{portName:.+}</sub>                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/statistics/{portName:.+}/subport/{subportNum}</sub>        | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/update-ports</sub>                                         | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnects/{id}/nameServers</sub>                                          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Interconnect Types**
|<sub>/rest/interconnect-types</sub>                                                      | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/interconnect-types/{id}</sub>                                                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Internal Link Sets**
|<sub>/rest/internal-link-sets</sub>                                                      | GET      | :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|<sub>/rest/internal-link-sets/{id}</sub>                                                 | GET      | :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|     **Logical Enclosures**
|<sub>/rest/logical-enclosures</sub>                                                      | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures</sub>                                                      | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}</sub>                                                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}</sub>                                                 | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}</sub>                                                 | PATCH    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}</sub>                                                 | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}/configuration</sub>                                   | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}/script</sub>                                          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}/script</sub>                                          | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}/support-dumps</sub>                                   | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-enclosures/{id}/updateFromGroup</sub>                                 | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Logical Interconnect Groups**
|<sub>/rest/logical-interconnect-groups</sub>                                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | 
|<sub>/rest/logical-interconnect-groups</sub>                                             | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnect-groups/defaultSettings</sub>                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnect-groups/{id}</sub>                                        | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnect-groups/{id}</sub>                                        | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnect-groups/{id}</sub>                                        | PATCH    |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/logical-interconnect-groups/{id}</sub>                                        | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnect-groups/{id}/settings</sub>                               | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Logical Interconnects**
|<sub>/rest/logical-interconnects</sub>                                                   | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/locations/interconnects</sub>                           | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/locations/interconnects</sub>                           | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}</sub>                                              | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/compliance</sub>                                   | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/ethernetSettings</sub>                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/ethernetSettings</sub>                             | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/firmware</sub>                                     | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/firmware</sub>                                     | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/forwarding-information-base</sub>                  | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/forwarding-information-base</sub>                  | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/forwarding-information-base/{dumpFileName}.{suffix}</sub>| GET   | :heavy_multiplication_x:   | :heavy_multiplication_x:   | :heavy_multiplication_x:   |   :heavy_multiplication_x:   |
|<sub>/rest/logical-interconnects/{id}/internalNetworks</sub>                             | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/internalVlans</sub>                                | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/qos-aggregated-configuration</sub>                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/qos-aggregated-configuration</sub>                 | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/settings</sub>                                     | PUT      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/logical-interconnects/{id}/snmp-configuration</sub>                           | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/snmp-configuration</sub>                           | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/support-dumps</sub>                                | POST     |  :heavy_multiplication_x:   | :heavy_multiplication_x:  |  :heavy_multiplication_x:|  :heavy_multiplication_x:  |
|<sub>/rest/logical-interconnects/{id}/unassignedPortsForPortMonitor</sub>                | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/unassignedUplinkPortsForPortMonitor</sub>          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/configuration</sub>                                | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/port-monitor</sub>                                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/port-monitor</sub>                                 | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/telemetry-configurations/{tcId}</sub>              | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/{id}/telemetry-configurations/{tcId}</sub>              | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/logical-interconnects/compliance</sub>                                        | POST     |  :heavy_multiplication_x:     | :heavy_multiplication_x:     | :heavy_multiplication_x:  |  :heavy_multiplication_x:   |
|<sub>/rest/logical-interconnects/{id}</sub>                                              | PATCH    |  :heavy_minus_sign:  |  :white_check_mark:  | :white_check_mark:  | :white_check_mark:   |
|     **Logical Switch Groups**
|<sub>/rest/logical-switch-groups</sub>                                                   | GET      |  :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|<sub>/rest/logical-switch-groups</sub>                                                   |POST      |  :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|<sub>/rest/logical-switch-groups/{id}</sub>                                              |GET       |  :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|<sub>/rest/logical-switch-groups/{id}</sub>                                              | PATCH    |  :heavy_minus_sign:  | :heavy_minus_sign:  | :heavy_minus_sign:  |
|<sub>/rest/logical-switch-groups/{id}</sub>                                              |PUT       |  :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|<sub>/rest/logical-switch-groups/{id}</sub>                                              |DELETE    |  :white_check_mark:  | :white_check_mark:  | :white_check_mark:  |
|     **Managed SANs**
|<sub>/rest/fc-sans/managed-sans</sub>                                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/fc-sans/managed-sans/{id}</sub>                                               | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/fc-sans/managed-sans/{id}</sub>                                               | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/fc-sans/managed-sans/{id}/endpoints</sub>                                     | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/fc-sans/managed-sans/{id}/endpoints</sub>                                     | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/fc-sans/managed-sans/{id}/issues</sub>                                        | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/fc-sans/managed-sans/WWN+</sub>                                               | GET      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|     **Network Sets**
|<sub>/rest/network-sets</sub>                                                            | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets</sub>                                                            | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets/withoutEthernet</sub>                                            | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets/{id}</sub>                                                       | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets/{id}</sub>                                                       | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets/{id}</sub>                                                       | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets/{id}/withoutEthernet</sub>                                       | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/network-sets/{id}</sub>                                                       | PATCH    |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |  :heavy_minus_sign:   |
|     **OS Deployment Plans**
|<sub>/rest/os-deployment-plans/</sub>                                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/os-deployment-plans/{id}</sub>                                                | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **SAS Interconnect Types**
|<sub>/rest/sas-interconnect-types</sub>                                                  | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-interconnect-types/{id}</sub>                                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **SAS Interconnects**
|<sub>/rest/sas-interconnects</sub>                                                       | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-interconnects/{id}</sub>                                                  | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-interconnects/{id}</sub>                                                  | PATCH    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-interconnects/{id}/refreshState</sub>                                     | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **SAS Logical Interconnect Groups**
|<sub>/rest/sas-logical-interconnect-groups</sub>                                         | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnect-groups</sub>                                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnect-groups/{id}</sub>                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnect-groups/{id}</sub>                                    | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnect-groups/{id}</sub>                                    | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **SAS Logical Interconnects**
|<sub>/rest/sas-logical-interconnects</sub>                                               | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/{id}</sub>                                          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/{id}/firmware</sub>                                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/{id}/firmware</sub>                                 | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/compliance</sub>                                    | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/{id}/compliance</sub>                               | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/{lsId}/configuration</sub>                          | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/sas-logical-interconnects/{id}/replaceDriveEnclosure</sub>                    | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Scopes**
|<sub>/rest/scopes</sub>                                                                  | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/scopes</sub>                                                                  | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/scopes/{id}</sub>                                                             | POST     | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/scopes/{id}</sub>                                                             | PUT      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/scopes/{id}</sub>                                                             | DELETE   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
     **Server Hardware**
|<sub>/rest/server-hardware</sub>                                                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware</sub>                                                         | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}</sub>                                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}</sub>                                                    | DELETE   |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/server-hardware/{id}/bios</sub>                                               | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/environmentalConfiguration</sub>                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/environmentalConfiguration</sub>                         | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/iloSsoUrl</sub>                                          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/javaRemoteConsoleUrl</sub>                               | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/mpFirmwareVersion</sub>                                  | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/physicalServerHardware</sub>                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/powerState</sub>                                         | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/refreshState</sub>                                       | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/remoteConsoleUrl</sub>                                   | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/utilization</sub>                                        | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}                                                          | PATCH    |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/*/firmware                                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/{id}/firmware                                                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware/discovery                                                     | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Server Hardware Types**
|<sub>/rest/server-hardware-types</sub>                                                   | GET      |  :white_check_mark:   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware-types/{id}</sub>                                              | GET      |  :white_check_mark:   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware-types/{id}</sub>                                              | PUT      |  :white_check_mark:   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-hardware-types/{id}</sub>                                              | DELETE   |  :white_check_mark:   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Server Profile Templates**
|<sub>/rest/server-profile-templates</sub>                                                | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates</sub>                                                | POST     | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates/{id}</sub>                                           | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates/{id}</sub>                                           | PUT      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates/{id}</sub>                                           | DELETE   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates/{id}/new-profile</sub>                               | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates/{id}/transformation</sub>                            | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profile-templates/available-networks</sub>                             | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Server Profiles**
|<sub>/rest/server-profiles</sub>                                                         | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles</sub>                                                         | POST     | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles</sub>                                                         | DELETE   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/available-networks</sub>                                      | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/available-servers</sub>                                       | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :heavy_minus_sign:   |
|<sub>/rest/server-profiles/available-storage-system</sub>                                | GET      | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/server-profiles/available-storage-systems</sub>                               | GET      | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/server-profiles/available-targets</sub>                                       | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/profile-ports</sub>                                           | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/{id}</sub>                                                    | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/{id}</sub>                                                    | PUT      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/{id}</sub>                                                    | DELETE   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/{id}</sub>                                                    | PATCH    | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/{id}/compliance-preview</sub>                                 | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/server-profiles/{id}/new-profile-template</sub>                               | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :heavy_minus_sign:   |
|<sub>/rest/server-profiles/{id}/messages</sub>                                           | GET      | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/server-profiles/{id}/transformation</sub>                                     | GET      | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Storage Pools**
|<sub>/rest/storage-pools</sub>                                                           | GET      | :white_check_mark:   | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-pools</sub>                                                           | POST     | :heavy_minus_sign:   | :heavy_minus_sign: | :heavy_minus_sign:
|<sub>/rest/storage-pools/reachable-storage-pools</sub>                                   | GET      | :white_check_mark:   | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-pools/{id}</sub>                                                      | GET      | :white_check_mark:   | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-pools/{id}</sub>                                                      | PUT      | :white_check_mark:   | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-pools/{id}</sub>                                                      | DELETE   | :heavy_minus_sign:   | :heavy_minus_sign: | :heavy_minus_sign:
|     **Storage Systems**
|<sub>/rest/storage-systems</sub>                                                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems</sub>                                                         | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/host-types</sub>                                              | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/{arrayId}/storage-pools</sub>                                 | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/{id}</sub>                                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/{id}</sub>                                                    | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/{id}</sub>                                                    | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/{id}/managedPorts</sub>                                       | GET      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/storage-systems/{id}/managedPorts/{portId}</sub>                              | GET      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/storage-systems/{id}/reachable-ports</sub>                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-systems/{id}/templates</sub>                                          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Storage Volume Attachments**
|<sub>/rest/storage-volume-attachments</sub>                                              | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volume-attachments/{id}</sub>                                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volume-attachments/repair</sub>                                       | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volume-attachments/repair</sub>                                       | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volume-attachments/{attachmentId}/paths</sub>                         | GET      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|<sub>/rest/storage-volume-attachments/{attachmentId)/paths/{id}</sub>                    | GET      |  :heavy_minus_sign:   | :heavy_minus_sign:   | :heavy_minus_sign:   |
|     **Storage Volume Templates**
|<sub>/rest/storage-volume-templates</sub>                                                | GET      | :white_check_mark: | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-volume-templates</sub>                                                | POST     | :white_check_mark: | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-volume-templates/connectable-volume-templates</sub>                   | GET      | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign:
|<sub>/rest/storage-volume-templates/reachable-volume-templates</sub>                     | GET      | :white_check_mark: | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-volume-templates/{id}</sub>                                           | GET      | :white_check_mark: | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-volume-templates/{id}</sub>                                           | PUT      | :white_check_mark: | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-volume-templates/{id}</sub>                                           | DELETE   | :white_check_mark: | :white_check_mark: | :white_check_mark:
|<sub>/rest/storage-volume-templates/{id}/compatible-systems</sub>                        | GET      | :white_check_mark: | :white_check_mark: | :white_check_mark:
|     **Switch Types**
|<sub>/rest/switch-types</sub>                                                            | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/switch-types/{id}</sub>                                                       | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|     **Uplink Sets**
|<sub>/rest/uplink-sets</sub>                                                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/uplink-sets</sub>                                                             | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/uplink-sets/{id}</sub>                                                        | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/uplink-sets/{id}</sub>                                                        | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|<sub>/rest/uplink-sets/{id}</sub>                                                        | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |  :white_check_mark:   |
|     **Volumes**
|<sub>/rest/storage-volumes</sub>                                                         | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes</sub>                                                         | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/attachable-volumes</sub>                                      | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/from-existing</sub>                                           | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/from-snapshot</sub>                                           | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/repair</sub>                                                  | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/repair</sub>                                                  | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}</sub>                                                    | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}</sub>                                                    | PUT      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}</sub>                                                    | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}/snapshots</sub>                                          | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}/snapshots</sub>                                          | POST     |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}/snapshots/{snapshotId}</sub>                             | GET      |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |
|<sub>/rest/storage-volumes/{id}/snapshots/{snapshotId}</sub>                             | DELETE   |  :white_check_mark:   | :white_check_mark:   | :white_check_mark:   |

## HPE Synergy Image Streamer

| Endpoints                                                                       | Verb             | V800                 | V1000                 | V1020
| ------------------------------------------------------------------------------  | ---------------- | :------------------: | :------------------:  | :------------------:  |
|     **Deployment Plans**
|<sub> /rest/deployment-plans </sub>                                              | POST             |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
|<sub> /rest/deployment-plans </sub>                                              | GET              |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
|<sub> /rest/deployment-plans/{id} </sub>                                         | GET              |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
|<sub> /rest/deployment-plans/{id} </sub>                                         | PUT              |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
|<sub> /rest/deployment-plans/{id} </sub>                                         | DELETE           |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
|<sub> /rest/deployment-plans/{id}/usedby </sub>                                  | GET              |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
|<sub> /rest/deployment-plans/{id}/osdp </sub>                                    | GET              |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
