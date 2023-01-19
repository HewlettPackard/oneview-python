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

from unittest import TestCase

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.servers.server_hardware import ServerHardware
from hpeOneView.resources.resource import (ResourceHelper,
                                           ResourceUtilizationMixin,
                                           ResourcePatchMixin)


class ServerHardwareTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._server_hardware = ServerHardware(self.connection)
        self.uri = "/rest/server-hardware/1224242424"
        self._server_hardware.data = {"uri": self.uri}

    @mock.patch.object(ResourceUtilizationMixin, 'get_utilization')
    def test_get_utilization_with_all_args(self, mock_get_utilization):
        self._server_hardware.get_utilization(fields='AmbientTemperature,AveragePower,PeakPower',
                                              filter='startDate=2016-05-30T03:29:42.361Z',
                                              refresh=True, view='day')

        mock_get_utilization.assert_called_once_with(fields='AmbientTemperature,AveragePower,PeakPower',
                                                     filter='startDate=2016-05-30T03:29:42.361Z',
                                                     refresh=True, view='day')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_utilization_with_defaults(self, mock_get):
        self._server_hardware.get_utilization()

        mock_get.assert_called_once_with("{}/utilization".format(self.uri))

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._server_hardware.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._server_hardware.get_all()

        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='')

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once(self, mock_create):
        information = {
            "licensingIntent": "OneView",
            "configurationState": "Managed"
        }
        mock_create.return_value = {}

        self._server_hardware.add(information)
        mock_create.assert_called_once_with(information.copy(), None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_multiple_servers_called_once(self, mock_create):
        information = {
            "licensingIntent": "OneView",
            "configurationState": "Managed"
        }
        mock_create.return_value = {}

        self._server_hardware.add_multiple_servers(information)
        mock_create.assert_called_once_with(information.copy(),
                                            '/rest/server-hardware/discovery',
                                            -1, None, False)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._server_hardware.remove(force=False)

        mock_delete.assert_called_once_with(self.uri, force=False,
                                            custom_headers=None, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        self._server_hardware.remove(force=True)

        mock_delete.assert_called_once_with(self.uri, force=True,
                                            custom_headers=None,
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_bios(self, mock_get):
        uri_rest_call = '{}/bios'.format(self.uri)

        self._server_hardware.get_bios()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_environmental_configuration(self, mock_get):
        uri_rest_call = '{}/environmentalConfiguration'.format(self.uri)

        self._server_hardware.get_environmental_configuration()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_environmental_configuration(self, mock_update):
        uri_rest_call = '{}/environmentalConfiguration'.format(self.uri)
        configuration = {"calibratedMaxPower": 2500}
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_environmental_configuration(
            configuration, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_ilo_sso_url(self, mock_get):
        uri_rest_call = '{}/iloSsoUrl'.format(self.uri)

        self._server_hardware.get_ilo_sso_url()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_ilo_sso_url_with_ip(self, mock_get):
        uri_rest_call = '{}/iloSsoUrl?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_ilo_sso_url(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_java_remote_console(self, mock_get):
        uri_rest_call = '{}/javaRemoteConsoleUrl'.format(self.uri)

        self._server_hardware.get_java_remote_console_url()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_java_remote_console_with_ip(self, mock_get):
        uri_rest_call = '{}/javaRemoteConsoleUrl?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_java_remote_console_url(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_refresh_state(self, mock_update):
        uri_rest_call = '{}/refreshState'.format(self.uri)
        configuration = {"refreshState": "RefreshPending"}
        configuration_rest_call = configuration.copy()

        self._server_hardware.refresh_state(
            configuration, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_power_state(self, mock_update):
        uri_rest_call = '{}/powerState'.format(self.uri)
        configuration = {
            "powerState": "Off",
            "powerControl": "MomentaryPress"
        }
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_power_state(configuration)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_remote_console_url(self, mock_get):
        uri_rest_call = '{}/remoteConsoleUrl'.format(self.uri)

        self._server_hardware.get_remote_console_url()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_remote_console_url_with_ip(self, mock_get):
        uri_rest_call = '{}/remoteConsoleUrl?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_remote_console_url(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_remote_console_url_with_consoleType(self, mock_get):
        uri_rest_call = '{}/remoteConsoleUrl?consoleType=.Net IRC'.format(self.uri)

        self._server_hardware.get_remote_console_url(consoleType='.Net IRC')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_put')
    def test_update_mp_firware_version_called_once(self, mock_get):
        self._server_hardware.update_mp_firware_version()
        uri = "{}/mpFirmwareVersion".format(self.uri)
        mock_get.assert_called_once_with(uri, None, -1, None)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_firmwares_with_defaults(self, mock_get):
        self._server_hardware.get_all_firmwares()

        mock_get.assert_called_once_with(0, -1, '', '', '', '', '',
                                         '/rest/server-hardware/*/firmware')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_firmwares_with_all_arguments(self, mock_get):
        self._server_hardware.get_all_firmwares("name='name'", 2, 5, 'query', 'sort')

        mock_get.assert_called_once_with(2, 5, "name='name'",
                                         'query', 'sort',
                                         '', '', '/rest/server-hardware/*/firmware')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware_by_id(self, mock_get):
        self._server_hardware.get_firmware()

        mock_get.assert_called_once_with('{}/firmware'.format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware_by_uri(self, mock_get):
        self._server_hardware.get_firmware()

        mock_get.assert_called_once_with('{}/firmware'.format(self.uri))

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_called_once(self, mock_patch):
        self._server_hardware.patch('replace', '/uidState', 'On')

        mock_patch.assert_called_once_with(self.uri,
                                           body=[{'op': 'replace',
                                                  'path': '/uidState',
                                                  'value': 'On'}],
                                           custom_headers=None,
                                           timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_physical_server_hardware(self, mock_get):
        uri_rest_call = '{}/physicalServerHardware'.format(self.uri)

        self._server_hardware.get_physical_server_hardware()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_local_storage(self, mock_get):
        uri_rest_call = '{}/localStorageV2'.format(self.uri)

        self._server_hardware.get_local_storage()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_local_storage_with_ip(self, mock_get):
        uri_rest_call = '{}/localStorageV2?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_local_storage(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_check_firmware_compliance(self, mock_post):
        self._server_hardware.check_firmware_compliance(configuration={"firmwareBaselineId": "abcd-1234-defg",
                                                                       "serverUUID": "1234567-8901"})

        mock_post.assert_called_once_with('/rest/server-hardware/firmware-compliance', {"firmwareBaselineId": "abcd-1234-defg",
                                                          "serverUUID": "1234567-8901"}, timeout=-1, custom_headers=None )

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_perform_firmware_update_called_once(self, mock_patch):
        uri_rest_call= '{}/firmware/settings'.format(self.uri)
        self._server_hardware.perform_firmware_update([
                    { "op": "replace", "value": {"baselineUri":"/rest/firmware-drivers/sdsdfsdf",
                      "firmwareInstallType":"FirmwareOnlyOfflineMode", "installationPolicy":"LowerThanBaseline"}
                    }])

        mock_patch.assert_called_once_with(uri_rest_call,
                                           [{ "op": "replace", "value": {"baselineUri":"/rest/firmware-drivers/sdsdfsdf",
                                              "firmwareInstallType":"FirmwareOnlyOfflineMode", "installationPolicy":"LowerThanBaseline"}
                                           }],
                                           custom_headers=None,
                                           timeout=-1)
