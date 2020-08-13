# -*- coding: utf-8 -*-
###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
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
from hpeOneView.resources.resource import ResourceClient
from hpeOneView.resources.facilities.power_devices import PowerDevices


class PowerDevicesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._power_devices = PowerDevices(self.connection)

    @mock.patch.object(ResourceClient, 'get_utilization')
    def test_get_utilization_with_all_args(self, mock_get):
        self._power_devices.get_utilization(
            '35323930-4936-4450-5531-303153474820',
            fields='PeakPower,AveragePower',
            filter='startDate=2016-05-30T03:29:42.361Z,endDate=2016-05-31T03:29:42.361Z',
            refresh=True, view='day')

        mock_get.assert_called_once_with('35323930-4936-4450-5531-303153474820',
                                         'PeakPower,AveragePower',
                                         'startDate=2016-05-30T03:29:42.361Z,endDate=2016-05-31T03:29:42.361Z',
                                         True,
                                         'day')

    @mock.patch.object(ResourceClient, 'get_utilization')
    def test_get_utilization_with_defaults(self, mock_get):
        self._power_devices.get_utilization('35323930-4936-4450-5531-303153474820')

        mock_get.assert_called_once_with('35323930-4936-4450-5531-303153474820', None, None, False, None)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._power_devices.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query='')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._power_devices.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        rack_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._power_devices.get(rack_id)
        mock_get.assert_called_once_with(rack_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        rack_uri = "/rest/racks/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._power_devices.get(rack_uri)
        mock_get.assert_called_once_with(rack_uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._power_devices.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        rack = {
            "name": "MyRack"
        }
        self._power_devices.add(rack)
        mock_create.assert_called_once_with(rack, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        rack = {
            "name": "MyRack"
        }
        self._power_devices.add(rack, 70)
        mock_create.assert_called_once_with(rack, timeout=70)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, update):
        rack = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "uuid": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "depth": 20,
            "height": 30,
            "width": 20
        }
        self._power_devices.update(rack)
        update.assert_called_once_with(rack.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        rack = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "uuid": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "depth": 20,
            "height": 30,
            "width": 20
        }
        self._power_devices.update(rack, 70)
        mock_update.assert_called_once_with(rack.copy(), timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.remove(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.remove(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_ipdu_called_once_with_defaults(self, mock_create):
        self._power_devices.add_ipdu({'name': 'name'})

        mock_create.assert_called_once_with({'name': 'name'}, timeout=-1, uri='/rest/power-devices/discover')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_power_state_called_once_with_defaults(self, mock_get):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.get_power_state(id)

        mock_get.assert_called_once_with('/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32/powerState')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_uid_state_called_once_with_defaults(self, mock_get):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.get_uid_state(id)

        mock_get.assert_called_once_with('/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32/uidState')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_power_state_called_once_with_defaults(self, mock_update):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.update_power_state(id, {"powerState": "Off"})

        mock_update.assert_called_once_with({'powerState': 'Off'},
                                            '/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32/powerState')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_refresh_state_called_once_with_defaults(self, mock_update):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.update_refresh_state(id, {"refreshState": "RefreshPending"})

        mock_update.assert_called_once_with({'refreshState': 'RefreshPending'},
                                            uri='/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32/refreshState')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_uid_state_called_once_with_defaults(self, mock_update):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._power_devices.update_uid_state(id, {"uidState": "Off"})

        mock_update.assert_called_once_with({'uidState': 'Off'},
                                            '/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32/uidState')

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_synchronous_called_once_with_defaults(self, mock_delete):
        self._power_devices.remove_synchronous({'uri': '/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32'})

        mock_delete.assert_called_once_with(
            {'uri': '/rest/power-devices/ad28cf21-8b15-4f92-bdcf-51cb2042db32/synchronous'},
            force=False,
            timeout=-1)
