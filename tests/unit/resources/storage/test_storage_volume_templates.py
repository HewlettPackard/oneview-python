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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpOneView.resources.resource import ResourceHelper


class StorageVolumeTemplatesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._storage_volume_templates = StorageVolumeTemplates(self.connection)
        self._storage_volume_templates.data = {'uri': '/rest/storage-volume-templates/ad28cf21-8b15-4f92-bdcf-51cb2042db32'}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_volume_templates.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(count=500, filter='name=TestName',
                                             sort='name:ascending', start=2)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_volume_templates.get_all()
        mock_get_all.assert_called_once_with(count=-1, filter='', sort='', start=0)

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_create_called_once(self, mock_create):
        storage_volume_template = {
            "name": "FusionTemplateExample",
            "provisioning": {
                "shareable": True,
                "provisionType": "Thin",
                "capacity": "235834383322",
                "storagePoolUri": "/rest/storage-pools/{id}"
            },
            "stateReason": "None",
            "storageSystemUri": "/rest/storage-systems/{id}",
            "snapshotPoolUri": "/rest/storage-pools/{id}"
        }
        self._storage_volume_templates.create(storage_volume_template, timeout=70)
        mock_create.assert_called_once_with('/rest/storage-volume-templates',
                                            storage_volume_template, 70, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._storage_volume_templates.delete(force=True, timeout=50)
        mock_delete.assert_called_once_with(self._storage_volume_templates.data["uri"],
                                            custom_headers={u'If-Match': u'*', u'Accept-Language': u'en_US'},
                                            force=True, timeout=50)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self._storage_volume_templates.delete()
        mock_delete.assert_called_once_with(self._storage_volume_templates.data["uri"],
                                            custom_headers={u'If-Match': u'*', u'Accept-Language': u'en_US'},
                                            force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_connectable_volume_templates_called_once(self, mock_get):
        uri = '/rest/storage-volume-templates/connectable-volume-templates?start=0&count=-1'
        self._storage_volume_templates.get_connectable_volume_templates()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_reachable_volume_templates_called_once(self, mock_get):
        uri = '/rest/storage-volume-templates/reachable-volume-templates?networks=/rest/fake&privateAllowedOnly=False&start=0&count=-1'
        self._storage_volume_templates.get_reachable_volume_templates(networks='/rest/fake')
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_compatible_systems_called_once(self, mock_get):
        uri = '{}/compatible-systems'.format(self._storage_volume_templates.data["uri"])
        self._storage_volume_templates.get_compatible_systems()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_put')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_update_called_once(self, mock_get, mock_update):
        storage_volume_template = {
            "type": "StorageVolumeTemplateV3",
            "provisioning": {
                "shareable": True,
                "provisionType": "Thin",
                "capacity": "235834383322",
                "storagePoolUri": "/rest/storage-pools/{id}"
            },
            "name": "FusionTemplateExample",
        }
        return_value = storage_volume_template.copy()
        return_value["uri"] = self._storage_volume_templates.data["uri"]

        mock_get.return_value = return_value
        mock_update.return_value = return_value
        self._storage_volume_templates.update(storage_volume_template, 70)
        mock_update.assert_called_once_with(self._storage_volume_templates.data["uri"],
                                            return_value, 70, None)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_all):
        self._storage_volume_templates.get_by("name", "test name")
        mock_get_all.assert_called_once_with(count=-1, filter='"name=\'test name\'"', sort='', start=0)
