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
from hpeOneView.resources.facilities.racks import Racks
from hpeOneView.resources.resource import ResourceClient


class RacksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._racks = Racks(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._racks.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query='')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._racks.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        rack_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._racks.get(rack_id)
        mock_get.assert_called_once_with(rack_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        rack_uri = "/rest/racks/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._racks.get(rack_uri)
        mock_get.assert_called_once_with(rack_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_device_topology_called_once_when_rack_uri_provided(self, mock_get):
        rack_uri = "/rest/racks/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        rack_device_topology_uri = "/rest/racks/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/deviceTopology"
        self._racks.get_device_topology(rack_uri)
        mock_get.assert_called_once_with(rack_device_topology_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_device_topology_called_once_when_rack_id_provided(self, mock_get):
        rack_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        rack_device_topology_uri = "/rest/racks/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/deviceTopology"
        self._racks.get_device_topology(rack_id)
        mock_get.assert_called_once_with(rack_device_topology_uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._racks.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        rack = {
            "name": "MyRack"
        }
        self._racks.add(rack)
        mock_create.assert_called_once_with(rack, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        rack = {
            "name": "MyRack"
        }
        self._racks.add(rack, 70)
        mock_create.assert_called_once_with(rack, timeout=70)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, update):
        rack = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "uuid": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "MyRack",
            "depth": 20,
            "height": 30,
            "width": 20
        }
        self._racks.update(rack)
        update.assert_called_once_with(rack, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        rack = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "uuid": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "MyRack",
            "depth": 20,
            "height": 30,
            "width": 20
        }
        self._racks.update(rack, 70)
        mock_update.assert_called_once_with(rack, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._racks.remove(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._racks.remove(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)
