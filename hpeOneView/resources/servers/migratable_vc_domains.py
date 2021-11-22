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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from hpeOneView.resources.resource import ResourceClient

from future import standard_library

standard_library.install_aliases()



class MigratableVcDomains(object):
    """
    The migratable VC domains resource provides methods for migrating Virtual Connect (VC)
    enclosures into the appliance. The operations are testing compatibility of a VC
    managed enclosure, retrieving a compatibility report, deleting a
    compatibility report and migrating a VC managed enclosure into the appliance.

    """

    URI = '/rest/migratable-vc-domains'

    def __init__(self, connection):
        self._connection = connection
        self._client = ResourceClient(connection, self.URI)

    @staticmethod
    def make_migration_information(oa_ip_address, oa_username, oa_password, vcm_username,\
            vcm_password, ilo_license_type='OneView', enclosure_group_uri=None):
        return {
            'credentials': {
                'oaIpAddress': oa_ip_address,
                'oaUsername': oa_username,
                'oaPassword': oa_password,
                'vcmUsername': vcm_username,
                'vcmPassword': vcm_password,
                'type': 'EnclosureCredentials'
            },
            'iloLicenseType': ilo_license_type,
            'enclosureGroupUri': enclosure_group_uri,
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }

    def test_compatibility(self, migration_information, timeout=-1):
        """
        Creates a migration report for an enclosure with a Virtual Connect domain.

        Args:
           migrationInformation: A dict specifying the enclosure, OA username, OA password,
           VCM username, and VCM password among other things.  Use make_migration_information
           to easily create this dict.
           timeout: Timeout in seconds.  Waits for task completion by default.  The timeout does
           not abort the task in OneView; just stops waiting for its completion.

        Returns: dict: a migration report.
        """

        return self._client.create(migration_information, timeout=timeout)

    def get_migration_report(self, id_or_uri):
        """
        Returns a migration report that has previously been generated.

        Args:
            id_or_uri: ID or URI of the migration report.

        Returns: dict: a migration report.
        """

        return self._client.get(id_or_uri)

    def migrate(self, id_or_uri, timeout=-1):
        """
        Initiates a migration of an enclosure specified by the ID or URI of a migration report.

        Args:
            id_or_uri: ID or URI of the migration report.
            timeout: Timeout in seconds.  Waits for task completion by default.  The timeout does
            not abort the task in OneView; just stops waiting for its completion.

        Returns: dict: a migration report.
        """

        # create the special payload to tell the VC Migration Manager to migrate the VC domain
        migration_information = {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }

        # call build_uri manually since .update(...) doesn't do it and the URI is not to be
        # included in the body when requesting a migration
        complete_uri = self._client.build_uri(id_or_uri)

        return self._client.update(migration_information, uri=complete_uri, timeout=timeout)

    def delete(self, id_or_uri, timeout=-1):
        """
        Deletes a migration report.

        Args:
            id_or_uri: ID or URI of the migration report.
            timeout: Timeout in seconds.  Waits for task completion by default.  The timeout does
            not abort the task in OneView; just stops waiting for its completion.

        Returns: bool: Indicates if the migration report was successfully deleted.
        """

        return self._client.delete(id_or_uri, timeout=timeout)
