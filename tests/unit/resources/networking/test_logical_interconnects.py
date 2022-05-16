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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpeOneView.resources.resource import ResourcePatchMixin, ResourceHelper


class LogicalInterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._logical_interconnect = LogicalInterconnects(self.connection)
        self.uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._logical_interconnect.data = {
            "uri": self.uri,
            "telemetryConfiguration": {"uri": "{}/telemetry-configurations/445cea80-280a-4794-b703-c53e8394a485".format(self.uri)}}

        self.telemetry_config = {
            "sampleCount": 12,
            "enableTelemetry": True,
            "sampleInterval": 300
        }
        self.tc_default_values = self._logical_interconnect.SETTINGS_TELEMETRY_CONFIG_DEFAULT_VALUES

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        sort = 'name:ascending'

        self._logical_interconnect.get_all(2, 500, sort)

        mock_get_all.assert_called_once_with(2, 500, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._logical_interconnect.get_all()
        mock_get_all.assert_called_once_with(0, -1, sort='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_return_logical_interconnect_when_exists(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "Logical Interconnect 1", "uri": "/path/to/logical/interconnect/1"},
            {"name": "Logical Interconnect 2", "uri": "/path/to/logical/interconnect/2"}
        ]
        logical_interconnect = self._logical_interconnect.get_by_name("Logical Interconnect 1")

        self.assertEqual(logical_interconnect.data,
                         {"name": "Logical Interconnect 1", "uri": "/path/to/logical/interconnect/1"})

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_return_null_when_logical_interconnect_not_exist(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "Logical Interconnect 1", "uri": "/path/to/logical/interconnect/1"},
            {"name": "Logical Interconnect 2", "uri": "/path/to/logical/interconnect/2"}
        ]
        logical_interconnect = self._logical_interconnect.get_by_name("another name")

        self.assertIsNone(logical_interconnect)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_compliance(self, mock_update):
        uri_rest_call = '{}/compliance'.format(self.uri)

        self._logical_interconnect.update_compliance()

        mock_update.assert_called_once_with(None, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_ethernet_settings(self, mock_update):
        uri_rest_call = '{}/ethernetSettings'.format(self.uri)
        configuration = {"enableNetworkLoopProtection": True}
        configuration_rest_call = configuration.copy()

        self._logical_interconnect.update_ethernet_settings(configuration)

        mock_update.assert_called_once_with(configuration_rest_call, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_ethernet_settings_with_force(self, mock_update):
        self._logical_interconnect.update_ethernet_settings({}, force=True)

        mock_update.assert_called_once_with(mock.ANY, uri=mock.ANY, force=True, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_internal_networks(self, mock_update):
        uri_rest_call = '{}/internalNetworks'.format(self.uri)
        network_uri_list = ['/rest/ethernet-networks/123s4s', '/rest/ethernet-networks/335d']

        self._logical_interconnect.update_internal_networks(network_uri_list)

        mock_update.assert_called_once_with(network_uri_list, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_internal_networks_with_force(self, mock_update):
        self._logical_interconnect.update_internal_networks([], force=True)

        mock_update.assert_called_once_with(mock.ANY, uri=mock.ANY, force=True, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_internal_vlans(self, mock_get_collection):
        uri_rest_call = '{}/internalVlans'.format(self.uri)

        self._logical_interconnect.get_internal_vlans()

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_settings(self, mock_update):
        uri_rest_call = '{}/settings'.format(self.uri)
        settings = {
            "type": "type",
            "ethernetSettings": {
                "macRefreshInterval": "5"
            }
        }
        settings_rest_call = settings.copy()
        settings_rest_call["type"] = "type"
        settings_rest_call["ethernetSettings"]["type"] = "EthernetInterconnectSettingsV4"
        self._logical_interconnect.update_settings(settings)

        mock_update.assert_called_once_with(settings_rest_call, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_settings_with_force(self, mock_update):
        self._logical_interconnect.update_settings({}, force=True)

        mock_update.assert_called_once_with({},
                                            uri="/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/settings",
                                            force=True, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_settings_with_default_values(self, mock_update):
        settings = {
            "ethernetSettings": {
                "macRefreshInterval": "5"
            }
        }
        settings_with_default_values = {
            "ethernetSettings": {
                "type": "EthernetInterconnectSettingsV4",
                "macRefreshInterval": "5"
            }
        }
        self._logical_interconnect.update_settings(settings)

        mock_update.assert_called_once_with(settings_with_default_values,
                                            uri="/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/settings",
                                            force=False,
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_configuration(self, mock_update):
        uri_rest_call = '{}/configuration'.format(self.uri)

        self._logical_interconnect.update_configuration()

        mock_update.assert_called_once_with(None, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_snmp_configuration_by_uri(self, mock_get):
        uri_rest_call = '{}/snmp-configuration'.format(self.uri)

        self._logical_interconnect.get_snmp_configuration()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_snmp_configuration(self, mock_update):
        uri_rest_call = '{}/snmp-configuration'.format(self.uri)
        configuration = {
            "readCommunity": "public",
            "enabled": True,
            "systemContact": "",
            "snmpAccess": [
                "10.0.0.0/24"
            ],
            "trapDestinations": [{
                "enetTrapCategories": [
                    "PortStatus"
                ],
                "vcmTrapCategories": [
                    "Legacy"
                ],
                "trapSeverities": [
                    "Normal",
                    "Info",
                    "Warning"
                ],
                "communityString": "public",
                "fcTrapCategories": [
                    "PortStatus"
                ],
                "trapDestination": "dest",
                "trapFormat": "SNMPv1"
            }],
        }
        port_monitor_rest_call = configuration.copy()

        self._logical_interconnect.update_snmp_configuration(configuration)

        port_monitor_rest_call['type'] = 'snmp-configuration'

        mock_update.assert_called_once_with(port_monitor_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_unassigned_uplink_ports(self, mock_get_collection):
        uri_rest_call = '{}/unassignedUplinkPortsForPortMonitor'.format(self.uri)

        self._logical_interconnect.get_unassigned_uplink_ports()

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_unassigned_ports(self, mock_get_collection):
        uri_rest_call = '{}/unassignedPortsForPortMonitor'.format(self.uri)

        self._logical_interconnect.get_unassigned_ports()

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_port_monitor_by_uri(self, mock_get):
        uri_rest_call = '{}/port-monitor'.format(self.uri)

        self._logical_interconnect.get_port_monitor()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_port_monitor_by_uri(self, mock_update):
        uri_rest_call = '{}/port-monitor'.format(self.uri)
        monitor_data = {
            "analyzerPort": {
                "portUri": "/rest/interconnects/76ad8f4b-b01b-d2ac31295c19/ports/76ad8f4b-6f13:X1",
                "portMonitorConfigInfo": "AnalyzerPort"
            },
            "enablePortMonitor": True,

            "monitoredPorts": [{
                "portUri": "/rest/interconnects/76ad8f4b-b01b-d2ac31295c19/ports/76ad8f4b-6f13:X1",
                "portMonitorConfigInfo": "MonitoredBoth"
            }]
        }
        port_monitor_rest_call = monitor_data.copy()
        port_monitor_rest_call['type'] = 'port-monitor'
        self._logical_interconnect.update_port_monitor(monitor_data)

        mock_update.assert_called_once_with(port_monitor_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_telemetry_configuration(self, mock_get):
        uri_telemetry_configuration = self._logical_interconnect.data["telemetryConfiguration"]["uri"]

        self._logical_interconnect.get_telemetry_configuration()

        mock_get.assert_called_once_with(uri_telemetry_configuration)

    @mock.patch.object(ResourceHelper, 'build_uri')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware(self, mock_get, mock_build_uri):
        mock_build_uri.return_value = self.uri

        expected_uri = "{}/firmware".format(self.uri)

        self._logical_interconnect.get_firmware()
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'build_uri')
    @mock.patch.object(ResourceHelper, 'update')
    def test_install_firmware(self, mock_update, mock_build_uri):
        fake_firmware = dict(
            command="Update",
            sppUri="/rest/firmware-drivers/Service_0Pack_0for_0ProLiant"
        )

        mock_build_uri.return_value = self.uri

        expected_uri = "{}/firmware".format(self.uri)

        self._logical_interconnect.install_firmware(fake_firmware)
        mock_update.assert_called_once_with(fake_firmware, expected_uri)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_forwarding_information_base(self, mock_get_collection):
        filter = 'name=TestName'
        self._logical_interconnect.get_forwarding_information_base(filter)

        expected_uri = '{}/forwarding-information-base'.format(self.uri)
        mock_get_collection.assert_called_once_with(expected_uri, filter=filter)

    @mock.patch.object(ResourceHelper, 'get_collection')
    def test_get_forwarding_information_base_when_no_filtering(self, mock_get_collection):
        self._logical_interconnect.get_forwarding_information_base()

        mock_get_collection.assert_called_once_with("{}/forwarding-information-base".format(self.uri), filter='')

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_create_interconnect_called_once_when_uri_provided(self, mock_create_with_zero_body):
        self._logical_interconnect.create_forwarding_information_base()

        expected_uri = '{}/forwarding-information-base'.format(self.uri)
        mock_create_with_zero_body.assert_called_once_with(expected_uri,
                                                           None, -1, None)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_qos_aggregated_configuration(self, mock_get):
        self._logical_interconnect.get_qos_aggregated_configuration()

        expected_uri = '{}/qos-aggregated-configuration'.format(self.uri)
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_qos_aggregated_configuration(self, mock_update):
        qos_configuration = {"type": "qos-aggregated-configuration"}
        qos_configuration_rest_call = qos_configuration.copy()

        self._logical_interconnect.update_qos_aggregated_configuration(qos_configuration)

        expected_uri = '{}/qos-aggregated-configuration'.format(self.uri)
        mock_update.assert_called_once_with(qos_configuration_rest_call, uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_ethernet_settings(self, mock_get):
        self._logical_interconnect.get_ethernet_settings()

        expected_uri = '{}/ethernetSettings'.format(self.uri)
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_telemetry_configuration(self, mock_update):
        self._logical_interconnect.update_telemetry_configurations(configuration=self.telemetry_config)

        mock_update.assert_called_once_with(self.telemetry_config,
                                            uri=self._logical_interconnect.data["telemetryConfiguration"]["uri"], timeout=-1)

    @mock.patch.object(ResourcePatchMixin, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._logical_interconnect.patch('replace', '/scopeUris',
                                         ['rest/fake/scope123'], 1)
        mock_patch.assert_called_once_with('replace', '/scopeUris',
                                           ['rest/fake/scope123'], 1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_igmp_settings(self, mock_update):
        configuration = {"igmpIdleTimeoutInterval": 200}
        configuration_rest_call = configuration.copy()

        self._logical_interconnect.update_igmp_settings(configuration)

        mock_update.assert_called_once_with(configuration_rest_call, uri='{}/igmpSettings'.format(self.uri), force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_igmp_settings(self, mock_get):
        self._logical_interconnect.get_igmp_settings()

        expected_uri = '{}/igmpSettings'.format(self.uri)
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_bulk_inconsistency_validate(self, mock_post):
        resource = {
            "logicalInterconnectUris": [
                "/rest/logical-interconnects/d0432852-28a7-4060-ba49-57ca973ef6c2"
            ]
        }
        expected_uri = '/rest/logical-interconnects/bulk-inconsistency-validation'

        self._logical_interconnect.bulk_inconsistency_validate(resource)

        mock_post.assert_called_once_with(expected_uri, resource, -1, None)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_port_flap_settings(self, mock_update):
        configuration = {"portFlapThresholdPerInterval": 3}
        configuration_rest_call = configuration.copy()

        self._logical_interconnect.update_port_flap_settings(configuration)

        mock_update.assert_called_once_with(configuration_rest_call, uri='{}/portFlapSettings'.format(self.uri), force=False, timeout=-1)
