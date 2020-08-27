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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpeOneView.resources.resource import Resource, ResourceFileHandlerMixin, extract_id_from_uri


class ArtifactBundles(ResourceFileHandlerMixin, Resource):

    URI = '/rest/artifact-bundles'
    BACKUPS_PATH = '/rest/artifact-bundles/backups'
    BACKUP_ARCHIVE_PATH = '/rest/artifact-bundles/backups/archive'
    DOWNLOAD_PATH = '/rest/artifact-bundles/download'

    def __init__(self, connection, data=None):
        super(ArtifactBundles, self).__init__(connection, data)
        self.__default_values = {
            'type': 'ArtifactsBundle'
        }

    def get_all_backups(self):
        """
        Get all Backups for Artifact Bundle.

        Returns:
            list: A list of Backups for Artifacts Bundle.
        """
        return self._helper.get_collection(uri=self.BACKUPS_PATH)

    def get_backup(self, uri):
        """
        Get the details for the backup from an Artifact Bundle.

        Args:
            uri: URI of the Artifact Bundle.

        Returns:
            Dict: Backup for an Artifacts Bundle.
        """
        uri = self.BACKUPS_PATH + '/' + extract_id_from_uri(uri)
        return super(ArtifactBundles, self).get_by_uri(uri)

    def download_archive(self, path, uri=None):
        """
        Downloads backup archive for the Artifact Bundle.

        Args:
            path(str): Destination file path.
            uri: URI of the Artifact Bundle.

        Returns:
            bool: Successfully downloaded.
        """
        if not uri:
            uri = self.data['uri']

        download_uri = self.BACKUP_ARCHIVE_PATH + '/' + extract_id_from_uri(uri)
        return super(ArtifactBundles, self).download(download_uri, path)

    def download(self, path, uri=None):
        """
        Download the Artifact Bundle.

        Args:
            uri: URI of the Artifact Bundle.
            path(str): Destination file path.

        Returns:
            bool: Successfully downloaded.
        """
        if not uri:
            uri = self.data['uri']

        download_uri = self.DOWNLOAD_PATH + '/' + extract_id_from_uri(uri)
        return super(ArtifactBundles, self).download(download_uri, path)

    def create_backup(self, resource, timeout=-1):
        """
        Creates a backup bundle with all the artifacts present on the appliance. At any given point only one backup
        bundle will exist on the appliance.

        Args:
            resource (dict): Deployment Group to create the backup.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            dict: A Deployment Group associated with the Artifact Bundle backup.
        """
        return super(ArtifactBundles, self).create(resource, uri=self.BACKUPS_PATH, timeout=timeout)

    def upload_bundle_from_file(self, file_path):
        """
        Restore an Artifact Bundle from a backup file.

        Args:
            file_path (str): The File Path to restore the Artifact Bundle.

        Returns:
            dict: Artifact bundle.
        """
        return super(ArtifactBundles, self).upload(file_path)

    def upload_backup_bundle_from_file(self, file_path, deployment_group_uri):
        """
        Restore an Artifact Bundle from a backup file.

        Args:
            file_path (str): The File Path to restore the Artifact Bundle.
            deployment_group_uri: URI of the Deployment Groups.

        Returns:
            dict: Deployment group.
        """
        uri = self.BACKUP_ARCHIVE_PATH + "?deploymentGrpUri=" + deployment_group_uri
        return super(ArtifactBundles, self).upload(file_path, uri)

    def extract(self, resource=None, uri=None, timeout=-1):
        """
        Extracts the existing bundle on the appliance and creates all the artifacts.

        Args:
            resource (dict): Artifact Bundle to extract.
            uri: URI of artifact bundle
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            dict: The Artifact Bundle.
        """
        if not uri:
            uri = self.data['uri']

        extract_uri = "{}?extract=true&forceImport=true".format(uri)
        return self._helper.update(resource, extract_uri, timeout=timeout, custom_headers={"Content-Type": "text/plain;charset=UTF-8"})

    def extract_backup(self, resource, uri=None, timeout=-1):
        """
        Extracts the existing backup bundle on the appliance and creates all the artifacts.

        Args:
            resource (dict): Deployment Group to extract.
            uri: URI of artifact backup
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            dict: A Deployment Group associated with the Artifact Bundle backup.
        """
        if not uri:
            uri = self.data['uri']

        extract_uri = self.BACKUPS_PATH + '/' + extract_id_from_uri(uri)
        return self._helper.update(resource, extract_uri, timeout=timeout)

    def stop_artifact_creation(self, task_uri, uri=None):
        """
        Stops creation of the selected Artifact Bundle.

        Args:
            task_uri: Task URI associated with the Artifact Bundle.
            uri: URI of the Artifact Bundle.

        Returns:
            string:
        """
        if not uri:
            uri = self.data['uri']

        data = {
            "taskUri": task_uri
        }

        stop_uri = "{}/stopArtifactCreate".format(uri)
        return self._helper.update(data, uri=stop_uri)
