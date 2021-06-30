# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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
"""
This module implements a common client for HPE OneView REST API.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

import json
import os

from hpeOneView.connection import connection
from hpeOneView.image_streamer.image_streamer_client import ImageStreamerClient
from hpeOneView.resources.security.certificate_authority import CertificateAuthority
from hpeOneView.resources.servers.connections import Connections
from hpeOneView.resources.networking.fc_networks import FcNetworks
from hpeOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpeOneView.resources.networking.ethernet_networks import EthernetNetworks
from hpeOneView.resources.networking.connection_templates import ConnectionTemplates
from hpeOneView.resources.networking.fabrics import Fabrics
from hpeOneView.resources.networking.network_sets import NetworkSets
from hpeOneView.resources.data_services.metric_streaming import MetricStreaming
from hpeOneView.resources.networking.switches import Switches
from hpeOneView.resources.networking.switch_types import SwitchTypes
from hpeOneView.resources.activity.tasks import Tasks
from hpeOneView.resources.settings.restores import Restores
from hpeOneView.resources.settings.scopes import Scopes
from hpeOneView.resources.settings.licenses import Licenses
from hpeOneView.resources.servers.enclosures import Enclosures
from hpeOneView.resources.servers.logical_enclosures import LogicalEnclosures
from hpeOneView.resources.servers.enclosure_groups import EnclosureGroups
from hpeOneView.resources.servers.server_hardware import ServerHardware
from hpeOneView.resources.servers.server_hardware_types import ServerHardwareTypes
from hpeOneView.resources.servers.id_pools_ranges import IdPoolsRanges
from hpeOneView.resources.servers.id_pools_ipv4_ranges import IdPoolsIpv4Ranges
from hpeOneView.resources.servers.id_pools_ipv4_subnets import IdPoolsIpv4Subnets
from hpeOneView.resources.servers.id_pools import IdPools
from hpeOneView.resources.networking.interconnects import Interconnects
from hpeOneView.resources.networking.interconnect_types import InterconnectTypes
from hpeOneView.resources.networking.interconnect_link_topologies import InterconnectLinkTopologies
from hpeOneView.resources.networking.sas_interconnect_types import SasInterconnectTypes
from hpeOneView.resources.networking.internal_link_sets import InternalLinkSets
from hpeOneView.resources.uncategorized.unmanaged_devices import UnmanagedDevices
from hpeOneView.resources.networking.logical_downlinks import LogicalDownlinks
from hpeOneView.resources.facilities.power_devices import PowerDevices
from hpeOneView.resources.facilities.racks import Racks
from hpeOneView.resources.facilities.datacenters import Datacenters
from hpeOneView.resources.fc_sans.managed_sans import ManagedSANs
from hpeOneView.resources.fc_sans.san_managers import SanManagers
from hpeOneView.resources.fc_sans.endpoints import Endpoints
from hpeOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpeOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpeOneView.resources.networking.sas_logical_interconnects import SasLogicalInterconnects
from hpeOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpeOneView.resources.networking.logical_switches import LogicalSwitches
from hpeOneView.resources.networking.sas_interconnects import SasInterconnects
from hpeOneView.resources.servers.server_profiles import ServerProfiles
from hpeOneView.resources.servers.server_profile_templates import ServerProfileTemplate
from hpeOneView.resources.storage.sas_logical_jbods import SasLogicalJbods
from hpeOneView.resources.storage.storage_systems import StorageSystems
from hpeOneView.resources.storage.storage_pools import StoragePools
from hpeOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpeOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpeOneView.resources.storage.drive_enclosures import DriveEnclosures
from hpeOneView.resources.settings.firmware_drivers import FirmwareDrivers
from hpeOneView.resources.settings.firmware_bundles import FirmwareBundles
from hpeOneView.resources.settings.backups import Backups
from hpeOneView.resources.storage.volumes import Volumes
from hpeOneView.resources.storage.sas_logical_jbod_attachments import SasLogicalJbodAttachments
from hpeOneView.resources.networking.uplink_sets import UplinkSets
from hpeOneView.resources.servers.migratable_vc_domains import MigratableVcDomains
from hpeOneView.resources.networking.sas_logical_interconnect_groups import SasLogicalInterconnectGroups
from hpeOneView.resources.search.index_resources import IndexResources
from hpeOneView.resources.search.labels import Labels
from hpeOneView.resources.activity.alerts import Alerts
from hpeOneView.resources.activity.events import Events
from hpeOneView.resources.uncategorized.os_deployment_plans import OsDeploymentPlans
from hpeOneView.resources.uncategorized.os_deployment_servers import OsDeploymentServers
from hpeOneView.resources.security.certificate_rabbitmq import CertificateRabbitMQ
from hpeOneView.resources.security.login_details import LoginDetails
from hpeOneView.resources.security.roles import Roles
from hpeOneView.resources.security.users import Users
from hpeOneView.resources.settings.appliance_device_read_community import ApplianceDeviceReadCommunity
from hpeOneView.resources.settings.appliance_device_snmp_v1_trap_destinations import ApplianceDeviceSNMPv1TrapDestinations
from hpeOneView.resources.settings.appliance_device_snmp_v3_trap_destinations import ApplianceDeviceSNMPv3TrapDestinations
from hpeOneView.resources.settings.appliance_device_snmp_v3_users import ApplianceDeviceSNMPv3Users
from hpeOneView.resources.settings.appliance_node_information import ApplianceNodeInformation
from hpeOneView.resources.settings.appliance_health_status import ApplianceHealthStatus
from hpeOneView.resources.settings.ha_nodes import HANodes
from hpeOneView.resources.settings.appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfiguration
from hpeOneView.resources.settings.versions import Versions
from hpeOneView.resources.hypervisors.hypervisor_managers import HypervisorManagers
from hpeOneView.resources.security.certificates_server import CertificatesServer
from hpeOneView.resources.hypervisors.hypervisor_cluster_profiles import HypervisorClusterProfiles
from hpeOneView.resources.settings.appliance_configuration_timeconfig import ApplianceConfigurationTimeconfig
from hpeOneView.resources.settings.appliance_ssh_access import ApplianceSshAccess

ONEVIEW_CLIENT_INVALID_PROXY = 'Invalid Proxy format'
ONEVIEW_CLIENT_INVALID_I3S_IP = 'Image streamer ip address is missing'
ONEVIEW_CLIENT_MISSING_IP = 'Oneview ip address is missing'


class OneViewClient(object):

    def __init__(self, config):
        self.__connection = connection(config.get('ip'), config.get('api_version'), config.get('ssl_certificate', False),
                                       config.get('timeout'))
        self.__image_streamer_ip = config.get("image_streamer_ip")
        self.__validate_host()
        self.__set_proxy(config)
        self.__connection.login(config["credentials"])
        self.__certificate_authority = None
        self.__connections = None
        self.__connection_templates = None
        self.__fc_networks = None
        self.__fcoe_networks = None
        self.__ethernet_networks = None
        self.__fabrics = None
        self.__network_sets = None
        self.__switches = None
        self.__switch_types = None
        self.__tasks = None
        self.__scopes = None
        self.__enclosures = None
        self.__logical_enclosures = None
        self.__enclosure_groups = None
        self.__metric_streaming = None
        self.__server_hardware = None
        self.__server_hardware_types = None
        self.__id_pools_vsn_ranges = None
        self.__id_pools_vmac_ranges = None
        self.__id_pools_vwwn_ranges = None
        self.__id_pools_ipv4_ranges = None
        self.__id_pools_ipv4_subnets = None
        self.__id_pools = None
        self.__interconnects = None
        self.__interconnect_types = None
        self.__interconnect_link_topologies = None
        self.__sas_interconnect_types = None
        self.__internal_link_sets = None
        self.__power_devices = None
        self.__unmanaged_devices = None
        self.__racks = None
        self.__roles = None
        self.__datacenters = None
        self.__san_managers = None
        self.__endpoints = None
        self.__logical_interconnects = None
        self.__sas_logical_interconnects = None
        self.__logical_interconnect_groups = None
        self.__logical_switch_groups = None
        self.__logical_switches = None
        self.__logical_downlinks = None
        self.__restores = None
        self.__server_profiles = None
        self.__server_profile_templates = None
        self.__sas_logical_jbods = None
        self.__storage_systems = None
        self.__storage_pools = None
        self.__storage_volume_templates = None
        self.__storage_volume_attachments = None
        self.__firmware_drivers = None
        self.__firmware_bundles = None
        self.__uplink_sets = None
        self.__volumes = None
        self.__sas_logical_jbod_attachments = None
        self.__managed_sans = None
        self.__migratable_vc_domains = None
        self.__sas_interconnects = None
        self.__index_resources = None
        self.__labels = None
        self.__sas_logical_interconnect_groups = None
        self.__alerts = None
        self.__events = None
        self.__drive_enclures = None
        self.__os_deployment_plans = None
        self.__os_deployment_servers = None
        self.__certificate_rabbitmq = None
        self.__users = None
        self.__appliance_device_read_community = None
        self.__appliance_device_snmp_v1_trap_destinations = None
        self.__appliance_device_snmp_v3_trap_destinations = None
        self.__appliance_device_snmp_v3_users = None
        self.__appliance_time_and_locale_configuration = None
        self.__appliance_node_information = None
        self.__appliance_health_status = None
        self.__versions = None
        self.__backups = None
        self.__login_details = None
        self.__licenses = None
        self.__hypervisor_managers = None
        self.__certificates_server = None
        self.__appliance_configuration_timeconfig = None
        self.__appliance_ssh_access = None
        self.__ha_nodes = None

    @classmethod
    def from_json_file(cls, file_name):
        """
        Construct OneViewClient using a json file.

        Args:
            file_name: json full path.

        Returns:
            OneViewClient:
        """
        with open(file_name) as json_data:
            config = json.load(json_data)

        return cls(config)

    @classmethod
    def from_environment_variables(cls):
        """
        Construct OneViewClient using environment variables.

        Allowed variables: ONEVIEWSDK_IP (required), ONEVIEWSDK_USERNAME (required), ONEVIEWSDK_PASSWORD (required),
        ONEVIEWSDK_AUTH_LOGIN_DOMAIN, ONEVIEWSDK_API_VERSION, ONEVIEWSDK_IMAGE_STREAMER_IP, ONEVIEWSDK_SESSIONID, ONEVIEWSDK_SSL_CERTIFICATE,
        ONEVIEWSDK_CONNECTION_TIMEOUT and ONEVIEWSDK_PROXY.

        Returns:
            OneViewClient:
        """
        ip = os.environ.get('ONEVIEWSDK_IP', '')
        image_streamer_ip = os.environ.get('ONEVIEWSDK_IMAGE_STREAMER_IP', '')
        api_version = os.environ.get('ONEVIEWSDK_API_VERSION', '')
        ssl_certificate = os.environ.get('ONEVIEWSDK_SSL_CERTIFICATE', '')
        username = os.environ.get('ONEVIEWSDK_USERNAME', '')
        auth_login_domain = os.environ.get('ONEVIEWSDK_AUTH_LOGIN_DOMAIN', '')
        password = os.environ.get('ONEVIEWSDK_PASSWORD', '')
        proxy = os.environ.get('ONEVIEWSDK_PROXY', '')
        sessionID = os.environ.get('ONEVIEWSDK_SESSIONID', '')
        timeout = os.environ.get('ONEVIEWSDK_CONNECTION_TIMEOUT')

        config = dict(ip=ip,
                      image_streamer_ip=image_streamer_ip,
                      api_version=api_version,
                      ssl_certificate=ssl_certificate,
                      credentials=dict(userName=username, authLoginDomain=auth_login_domain, password=password, sessionID=sessionID),
                      proxy=proxy, timeout=timeout)

        return cls(config)

    def __set_proxy(self, config):
        """
        Set proxy if needed
        Args:
            config: Config dict
        """
        if "proxy" in config and config["proxy"]:
            proxy = config["proxy"]
            splitted = proxy.split(':')
            if len(splitted) != 2:
                raise ValueError(ONEVIEW_CLIENT_INVALID_PROXY)

            proxy_host = splitted[0]
            proxy_port = int(splitted[1])
            self.__connection.set_proxy(proxy_host, proxy_port)

    def __validate_host(self):
        """
        Fails if oneview ip is not provided
        """
        if not self.__connection._host:
            raise ValueError(ONEVIEW_CLIENT_MISSING_IP)

    @property
    def api_version(self):
        """
        Gets the OneView API Version.

        Returns:
            int: API Version.
        """
        return self.__connection._apiVersion

    @property
    def connection(self):
        """
        Gets the underlying HPE OneView connection used by the OneViewClient.

        Returns:
            connection:
        """
        return self.__connection

    def create_image_streamer_client(self):
        """
        Create the Image Streamer API Client.

        Returns:
            ImageStreamerClient:
        """
        if not self.__image_streamer_ip:
            raise ValueError(ONEVIEW_CLIENT_INVALID_I3S_IP)

        image_streamer = ImageStreamerClient(self.__image_streamer_ip,
                                             self.__connection.get_session_id(),
                                             self.__connection._apiVersion,
                                             self.__connection._sslBundle)

        return image_streamer

    @property
    def certificate_authority(self):
        """
        Gets the Certificate Authority API client.

        Returns:
            CertificateAuthority:
        """
        return CertificateAuthority(self.__connection)

    @property
    def connections(self):
        """
        Gets the Connections API client.

        Returns:
            Connections:
        """
        if not self.__connections:
            self.__connections = Connections(
                self.__connection)
        return self.__connections

    @property
    def connection_templates(self):
        """
        Gets the ConnectionTemplates API client.

        Returns:
            ConnectionTemplates:
        """
        return ConnectionTemplates(self.__connection)

    @property
    def fc_networks(self):
        """
        Gets the FcNetworks API client.

        Returns:
            FcNetworks:
        """
        return FcNetworks(self.__connection)

    @property
    def fcoe_networks(self):
        """
        Gets the FcoeNetworks API client.

        Returns:
            FcoeNetworks:
        """
        return FcoeNetworks(self.__connection)

    @property
    def ethernet_networks(self):
        """
        Gets the EthernetNetworks API client.

        Returns:
            EthernetNetworks:
        """
        return EthernetNetworks(self.__connection)

    @property
    def fabrics(self):
        """
        Gets the Fabrics API client.

        Returns:
            Fabrics:
        """
        if not self.__fabrics:
            self.__fabrics = Fabrics(self.__connection)
        return self.__fabrics

    @property
    def restores(self):
        """
        Gets the Restores API client.

        Returns:
            Restores:
        """
        return Restores(self.__connection)

    @property
    def scopes(self):
        """
        Gets the Scopes API client.

        Returns:
            Scopes:
        """
        return Scopes(self.__connection)

    @property
    def datacenters(self):
        """
        Gets the Datacenters API client.

        Returns:
            Datacenters:
        """
        if not self.__datacenters:
            self.__datacenters = Datacenters(self.__connection)
        return self.__datacenters

    @property
    def network_sets(self):
        """
        Gets the NetworkSets API client.

        Returns:
            NetworkSets:
        """
        return NetworkSets(self.__connection)

    @property
    def server_hardware(self):
        """
        Gets the ServerHardware API client.

        Returns:
            ServerHardware:
        """
        return ServerHardware(self.__connection)

    @property
    def server_hardware_types(self):
        """
        Gets the ServerHardwareTypes API client.

        Returns:
            ServerHardwareTypes:
        """
        return ServerHardwareTypes(self.__connection)

    @property
    def id_pools_vsn_ranges(self):
        """
        Gets the IdPoolsRanges API Client for VSN Ranges.

        Returns:
            IdPoolsRanges:
        """
        if not self.__id_pools_vsn_ranges:
            self.__id_pools_vsn_ranges = IdPoolsRanges('vsn', self.__connection)
        return self.__id_pools_vsn_ranges

    @property
    def id_pools_vmac_ranges(self):
        """
        Gets the IdPoolsRanges API Client for VMAC Ranges.

        Returns:
            IdPoolsRanges:
        """
        if not self.__id_pools_vmac_ranges:
            self.__id_pools_vmac_ranges = IdPoolsRanges('vmac', self.__connection)
        return self.__id_pools_vmac_ranges

    @property
    def id_pools_vwwn_ranges(self):
        """
        Gets the IdPoolsRanges API Client for VWWN Ranges.

        Returns:
            IdPoolsRanges:
        """
        if not self.__id_pools_vwwn_ranges:
            self.__id_pools_vwwn_ranges = IdPoolsRanges('vwwn', self.__connection)
        return self.__id_pools_vwwn_ranges

    @property
    def id_pools_ipv4_ranges(self):
        """
        Gets the IdPoolsIpv4Ranges API client.

        Returns:
            IdPoolsIpv4Ranges:
        """
        return IdPoolsIpv4Ranges(self.__connection)

    @property
    def id_pools_ipv4_subnets(self):
        """
        Gets the IdPoolsIpv4Subnets API client.

        Returns:
            IdPoolsIpv4Subnets:
        """
        return IdPoolsIpv4Subnets(self.__connection)

    @property
    def id_pools(self):
        """
        Gets the IdPools API client.

        Returns:
            IdPools:
        """
        return IdPools(self.__connection)

    @property
    def switches(self):
        """
        Gets the Switches API client.

        Returns:
            Switches:
        """
        if not self.__switches:
            self.__switches = Switches(self.__connection)
        return self.__switches

    @property
    def roles(self):
        """
        Gets the Roles API client.

        Returns:
            Roles:
        """
        if not self.__roles:
            self.__roles = Roles(self.__connection)
        return self.__roles

    @property
    def switch_types(self):
        """
        Gets the SwitchTypes API client.

        Returns:
            SwitchTypes:
        """
        return SwitchTypes(self.__connection)

    @property
    def logical_switch_groups(self):
        """
        Gets the LogicalSwitchGroups API client.

        Returns:
            LogicalSwitchGroups:
        """
        return LogicalSwitchGroups(self.__connection)

    @property
    def logical_switches(self):
        """
        Gets the LogicalSwitches API client.

        Returns:
            LogicalSwitches:
        """
        if not self.__logical_switches:
            self.__logical_switches = LogicalSwitches(self.__connection)
        return self.__logical_switches

    @property
    def tasks(self):
        """
        Gets the Tasks API client.

        Returns:
            Tasks:
        """
        if not self.__tasks:
            self.__tasks = Tasks(self.__connection)
        return self.__tasks

    @property
    def enclosure_groups(self):
        """
        Gets the EnclosureGroups API client.

        Returns:
            EnclosureGroups:
        """
        return EnclosureGroups(self.__connection)

    @property
    def enclosures(self):
        """
        Gets the Enclosures API client.

        Returns:
            Enclosures:
        """
        return Enclosures(self.__connection)

    @property
    def logical_enclosures(self):
        """
        Gets the LogicalEnclosures API client.

        Returns:
            LogicalEnclosures:
        """
        return LogicalEnclosures(self.__connection)

    @property
    def metric_streaming(self):
        """
        Gets the MetricStreaming API client.

        Returns:
            MetricStreaming:
        """
        if not self.__metric_streaming:
            self.__metric_streaming = MetricStreaming(self.__connection)
        return self.__metric_streaming

    @property
    def interconnects(self):
        """
        Gets the Interconnects API client.

        Returns:
            Interconnects:
        """
        return Interconnects(self.__connection)

    @property
    def interconnect_types(self):
        """
        Gets the InterconnectTypes API client.

        Returns:
            InterconnectTypes:
        """
        return InterconnectTypes(self.__connection)

    @property
    def interconnect_link_topologies(self):
        """
        Gets the InterconnectLinkTopologies API client.

        Returns:
            InterconnectLinkTopologies:
        """
        if not self.__interconnect_link_topologies:
            self.__interconnect_link_topologies = InterconnectLinkTopologies(self.__connection)
        return self.__interconnect_link_topologies

    @property
    def sas_interconnect_types(self):
        """
        Gets the SasInterconnectTypes API client.

        Returns:
            SasInterconnectTypes:
        """
        return SasInterconnectTypes(self.__connection)

    @property
    def internal_link_sets(self):
        """
        Gets the InternalLinkSets API client.

        Returns:
            InternalLinkSets:
        """
        return InternalLinkSets(self.__connection)

    @property
    def logical_interconnect_groups(self):
        """
        Gets the LogicalInterconnectGroups API client.

        Returns:
            LogicalInterconnectGroups:
        """
        return LogicalInterconnectGroups(self.__connection)

    @property
    def logical_interconnects(self):
        """
        Gets the LogicalInterconnects API client.

        Returns:
            LogicalInterconnects:
        """
        return LogicalInterconnects(self.__connection)

    @property
    def sas_logical_interconnects(self):
        """
        Gets the SasLogicalInterconnects API client.

        Returns:
            SasLogicalInterconnects:
        """
        return SasLogicalInterconnects(self.__connection)

    @property
    def logical_downlinks(self):
        """
        Gets the LogicalDownlinks API client.

        Returns:
            LogicalDownlinks:
        """
        if not self.__logical_downlinks:
            self.__logical_downlinks = LogicalDownlinks(
                self.__connection)
        return self.__logical_downlinks

    @property
    def power_devices(self):
        """
        Gets the PowerDevices API client.

        Returns:
            PowerDevices:
        """
        if not self.__power_devices:
            self.__power_devices = PowerDevices(self.__connection)
        return self.__power_devices

    @property
    def unmanaged_devices(self):
        """
        Gets the Unmanaged Devices API client.

        Returns:
            UnmanagedDevices:
        """
        if not self.__unmanaged_devices:
            self.__unmanaged_devices = UnmanagedDevices(self.__connection)
        return self.__unmanaged_devices

    @property
    def racks(self):
        """
        Gets the Racks API client.

        Returns:
            Racks:
        """
        if not self.__racks:
            self.__racks = Racks(self.__connection)
        return self.__racks

    @property
    def san_managers(self):
        """
        Gets the SanManagers API client.

        Returns:
            SanManagers:
        """
        if not self.__san_managers:
            self.__san_managers = SanManagers(self.__connection)
        return self.__san_managers

    @property
    def endpoints(self):
        """
        Gets the Endpoints API client.

        Returns:
            Endpoints:
        """
        if not self.__endpoints:
            self.__endpoints = Endpoints(self.__connection)
        return self.__endpoints

    @property
    def server_profiles(self):
        """
        Gets the ServerProfiles API client.

        Returns:
            ServerProfiles:
        """
        return ServerProfiles(self.__connection)

    @property
    def server_profile_templates(self):
        """
        Gets the ServerProfileTemplate API client.

        Returns:
            ServerProfileTemplate:
        """
        return ServerProfileTemplate(self.__connection)

    @property
    def storage_systems(self):
        """
        Gets the StorageSystems API client.

        Returns:
            StorageSystems:
        """
        return StorageSystems(self.__connection)

    @property
    def storage_pools(self):
        """
        Gets the StoragePools API client.

        Returns:
            StoragePools:
        """
        return StoragePools(self.__connection)

    @property
    def storage_volume_templates(self):
        """
        Gets the StorageVolumeTemplates API client.

        Returns:
            StorageVolumeTemplates:
        """
        return StorageVolumeTemplates(self.__connection)

    @property
    def storage_volume_attachments(self):
        """
        Gets the StorageVolumeAttachments API client.

        Returns:
            StorageVolumeAttachments:
        """
        return StorageVolumeAttachments(self.__connection)

    @property
    def firmware_drivers(self):
        """
        Gets the FirmwareDrivers API client.

        Returns:
            FirmwareDrivers:
        """
        return FirmwareDrivers(self.__connection)

    @property
    def firmware_bundles(self):
        """
        Gets the FirmwareBundles API client.

        Returns:
            FirmwareBundles:
        """
        if not self.__firmware_bundles:
            self.__firmware_bundles = FirmwareBundles(self.__connection)
        return self.__firmware_bundles

    @property
    def uplink_sets(self):
        """
        Gets the UplinkSets API client.

        Returns:
            UplinkSets:
        """
        return UplinkSets(self.__connection)

    @property
    def volumes(self):
        """
        Gets the Volumes API client.

        Returns:
            Volumes:
        """
        return Volumes(self.__connection)

    @property
    def sas_logical_jbod_attachments(self):
        """
        Gets the SAS Logical JBOD Attachments client.

        Returns:
            SasLogicalJbodAttachments:
        """
        if not self.__sas_logical_jbod_attachments:
            self.__sas_logical_jbod_attachments = SasLogicalJbodAttachments(self.__connection)
        return self.__sas_logical_jbod_attachments

    @property
    def managed_sans(self):
        """
        Gets the Managed SANs API client.

        Returns:
            ManagedSANs:
        """
        return ManagedSANs(self.__connection)

    @property
    def migratable_vc_domains(self):
        """
        Gets the VC Migration Manager API client.

        Returns:
            MigratableVcDomains:
        """
        if not self.__migratable_vc_domains:
            self.__migratable_vc_domains = MigratableVcDomains(self.__connection)
        return self.__migratable_vc_domains

    @property
    def sas_interconnects(self):
        """
        Gets the SAS Interconnects API client.

        Returns:
            SasInterconnects:
        """
        return SasInterconnects(self.__connection)

    @property
    def sas_logical_interconnect_groups(self):
        """
        Gets the SasLogicalInterconnectGroups API client.

        Returns:
            SasLogicalInterconnectGroups:
        """
        return SasLogicalInterconnectGroups(self.__connection)

    @property
    def drive_enclosures(self):
        """
        Gets the Drive Enclosures API client.

        Returns:
            DriveEnclosures:
        """
        if not self.__drive_enclures:
            self.__drive_enclures = DriveEnclosures(self.__connection)
        return self.__drive_enclures

    @property
    def sas_logical_jbods(self):
        """
        Gets the SAS Logical JBODs API client.

        Returns:
            SasLogicalJbod:
        """
        if not self.__sas_logical_jbods:
            self.__sas_logical_jbods = SasLogicalJbods(self.__connection)
        return self.__sas_logical_jbods

    @property
    def labels(self):
        """
        Gets the Labels API client.

        Returns:
            Labels:
        """
        return Labels(self.__connection)

    @property
    def index_resources(self):
        """
        Gets the Index Resources API client.

        Returns:
            IndexResources:
        """
        return IndexResources(self.__connection)

    @property
    def alerts(self):
        """
        Gets the Alerts API client.

        Returns:
            Alerts:
        """
        if not self.__alerts:
            self.__alerts = Alerts(self.__connection)
        return self.__alerts

    @property
    def events(self):
        """
        Gets the Events API client.

        Returns:
            Events:
        """
        if not self.__events:
            self.__events = Events(self.__connection)
        return self.__events

    @property
    def os_deployment_plans(self):
        """
        Gets the Os Deployment Plans API client.

        Returns:
            OsDeploymentPlans:
        """
        return OsDeploymentPlans(self.__connection)

    @property
    def os_deployment_servers(self):
        """
        Gets the Os Deployment Servers API client.

        Returns:
            OsDeploymentServers:
        """
        if not self.__os_deployment_servers:
            self.__os_deployment_servers = OsDeploymentServers(self.__connection)
        return self.__os_deployment_servers

    @property
    def certificate_rabbitmq(self):
        """
        Gets the Certificate RabbitMQ API client.

        Returns:
            CertificateRabbitMQ:
        """
        if not self.__certificate_rabbitmq:
            self.__certificate_rabbitmq = CertificateRabbitMQ(self.__connection)
        return self.__certificate_rabbitmq

    @property
    def users(self):
        """
        Gets the Users API client.

        Returns:
            Users:
        """
        return Users(self.__connection)

    @property
    def appliance_device_read_community(self):
        """
        Gets the ApplianceDeviceReadCommunity API client.

        Returns:
            ApplianceDeviceReadCommunity:
        """
        if not self.__appliance_device_read_community:
            self.__appliance_device_read_community = ApplianceDeviceReadCommunity(self.__connection)
        return self.__appliance_device_read_community

    @property
    def appliance_device_snmp_v1_trap_destinations(self):
        """
        Gets the ApplianceDeviceSNMPv1TrapDestinations API client.

        Returns:
            ApplianceDeviceSNMPv1TrapDestinations:
        """
        return ApplianceDeviceSNMPv1TrapDestinations(self.__connection)

    @property
    def appliance_device_snmp_v3_trap_destinations(self):
        """
        Gets the ApplianceDeviceSNMPv3TrapDestinations API client.

        Returns:
            ApplianceDeviceSNMPv3TrapDestinations:
        """
        return ApplianceDeviceSNMPv3TrapDestinations(self.__connection)

    @property
    def appliance_device_snmp_v3_users(self):
        """
        Gets the ApplianceDeviceSNMPv3Users API client.

        Returns:
            ApplianceDeviceSNMPv3Users:
        """
        return ApplianceDeviceSNMPv3Users(self.__connection)

    @property
    def appliance_node_information(self):
        """
        Gets the ApplianceNodeInformation API client.

        Returns:
            ApplianceNodeInformation:
        """
        return ApplianceNodeInformation(self.__connection)

    @property
    def appliance_health_status(self):
        """
        Gets the ApplianceHealthStatus API client.

        Returns:
            ApplianceHealthStatus:
        """
        return ApplianceHealthStatus(self.__connection)

    @property
    def ha_nodes(self):
        """
        Gets the HANodes API client.

        Returns:
            HANodes:
        """
        return HANodes(self.__connection)

    @property
    def appliance_time_and_locale_configuration(self):
        """
        Gets the ApplianceTimeAndLocaleConfiguration API client.

        Returns:
            ApplianceTimeAndLocaleConfiguration:
        """
        return ApplianceTimeAndLocaleConfiguration(self.__connection)

    @property
    def versions(self):
        """
        Gets the Version API client.

        Returns:
            Version:
        """
        if not self.__versions:
            self.__versions = Versions(self.__connection)
        return self.__versions

    @property
    def backups(self):
        """
        Gets the Backup API client.

        Returns:
            Backups:
        """
        if not self.__backups:
            self.__backups = Backups(self.__connection)
        return self.__backups

    @property
    def login_details(self):
        """
        Gets the login details

        Returns:
        List of login details
        """
        if not self.__login_details:
            self.__login_details = LoginDetails(self.__connection)
        return self.__login_details

    @property
    def licenses(self):
        """
        Gets all the licenses
        Returns:
        List of licenses
        """
        if not self.__licenses:
            self.__licenses = Licenses(self.__connection)
        return self.__licenses

    @property
    def hypervisor_managers(self):
        """
        Gets the Hypervisor Managers API client.

        Returns:
            HypervisorManagers
        """
        return HypervisorManagers(self.__connection)

    @property
    def certificates_server(self):
        """
        Gets the Certificates Server API client.

        Returns:
            Server Certificate:
        """
        return CertificatesServer(self.__connection)

    @property
    def hypervisor_cluster_profiles(self):
        """
        Gets the Hypervisor Cluster Profiles API client.

        Returns:
            Hypervisor Cluster Profiles:
        """
        return HypervisorClusterProfiles(self.__connection)

    @property
    def appliance_configuration_timeconfig(self):
        """
        Gets the ApplianceConfigurationTimeconfig API client.

        Returns:
            ApplianceConfigurationTimeconfig:
        """
        return ApplianceConfigurationTimeconfig(self.__connection)

    @property
    def appliance_ssh_access(self):
        """
        Gets the ApplianceSshAccess API client.

        Returns:
            ApplianceSshAccess:
        """
        return ApplianceSshAccess(self.__connection)
