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
from hpeOneView.resources.servers.migratable_vc_domains import MigratableVcDomains
from hpeOneView.resources.resource import ResourceClient


class MigratableVcDomainsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.vcmigrationmanager = MigratableVcDomains(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_test_compatibility(self, mock_create):
        timeoutValue = 26

        migrationInformation = MigratableVcDomains. \
            make_migration_information('192.168.9.32', 'Administrator', 'password', 'Administrator', 'password',
                                       enclosureGroupUri='/rest/enclosure-groups/uri')

        self.vcmigrationmanager.test_compatibility(migrationInformation, timeout=timeoutValue)

        mock_create.assert_called_once_with(migrationInformation, timeout=timeoutValue)

    @mock.patch.object(ResourceClient, 'create')
    def test_test_compatibility_default(self, mock_create):

        migrationInformation = MigratableVcDomains. \
            make_migration_information('192.168.9.32', 'Administrator', 'password', 'Administrator', 'password',
                                       enclosureGroupUri='/rest/enclosure-groups/uri')

        self.vcmigrationmanager.test_compatibility(migrationInformation)

        mock_create.assert_called_once_with(migrationInformation, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_migration_report(self, mock_get):
        uri = '/rest/migratable-vc-domains/uri'

        self.vcmigrationmanager.get_migration_report(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_migrate_with_full_uri(self, mock_update):
        migrationInformation = {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }
        uriValue = '/rest/migratable-vc-domains/uri'
        timeoutValue = 26

        self.vcmigrationmanager.migrate(uriValue, timeout=timeoutValue)

        mock_update.assert_called_once_with(migrationInformation, uri=uriValue, timeout=timeoutValue)

    @mock.patch.object(ResourceClient, 'update')
    def test_migrate_with_id(self, mock_update):
        migrationInformation = {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }
        id = 'uri'
        uriValue = '/rest/migratable-vc-domains/' + id
        timeoutValue = 26

        self.vcmigrationmanager.migrate(id, timeout=timeoutValue)

        mock_update.assert_called_once_with(migrationInformation, uri=uriValue, timeout=timeoutValue)

    @mock.patch.object(ResourceClient, 'update')
    def test_migrate_default(self, mock_update):
        migrationInformation = {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }
        uriValue = '/rest/migratable-vc-domains/uri'

        self.vcmigrationmanager.migrate(uriValue)

        mock_update.assert_called_once_with(migrationInformation, uri=uriValue, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete(self, mock_delete):
        timeoutValue = 26
        uriValue = '/rest/migratable-vc-domains/uri'

        self.vcmigrationmanager.delete(uriValue, timeout=timeoutValue)

        mock_delete.assert_called_once_with(uriValue, timeout=timeoutValue)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_default(self, mock_delete):
        uriValue = '/rest/migratable-vc-domains/uri'

        self.vcmigrationmanager.delete(uriValue)

        mock_delete.assert_called_once_with(uriValue, timeout=-1)
