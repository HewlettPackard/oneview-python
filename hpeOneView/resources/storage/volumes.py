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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


from hpeOneView.resources.resource import Resource

INVALID_VOLUME_URI = "When no snapshot uri is provided, volume id or valume uri is required."


class VolumeSnapshots(Resource):
    """
    Volume snapshots API client.

    """
    DEFAULT_VALUES = {
        '200': {"type": "Snapshot"},
        '300': {"type": "Snapshot"},
        '500': {}
    }

    def __init__(self, connection, data=None, volume_uri=None, snapshot_id=None):
        self.URI = "{}/snapshots/{}".format(volume_uri, snapshot_id or '')
        super(VolumeSnapshots, self).__init__(connection, data)

    def create(self, data=None, timeout=-1, custom_headers=None, force=False):
        """Makes a POST request to create a resource when a request body is required.

        Args:
            data: Additional fields can be passed to create the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers: Allows set specific HTTP headers.
        Returns:
            Created resource.
        """
        super(VolumeSnapshots, self).create(data, timeout=timeout, custom_headers=custom_headers, force=force)
        return self.get_by_name(data["name"])

    def delete(self, force=False, timeout=-1):
        """
        Deletes a snapshot from OneView and the storage system.

        Args:
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Details of associated volume.

        """
        headers = {'If-Match': '*'}
        super(VolumeSnapshots, self).delete(force=force, timeout=timeout,
                                            custom_headers=headers)


class Volumes(Resource):
    """
    Volumes API client.

    """
    URI = '/rest/storage-volumes'

    def __init__(self, connection, data=None):
        super(Volumes, self).__init__(connection, data)
        self._snapshots = None

    def __get_snapshot_object(self):
        if self.data and not self._snapshots:
            self._snapshots = VolumeSnapshots(self._connection,
                                              volume_uri=self.data["uri"])

    def add_from_existing(self, resource, timeout=-1):
        """
        Adds a volume that already exists in the Storage system

        Args:
            resource (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Added resource.
        """
        uri = self.URI + "/from-existing"
        return self._helper.create(resource, uri=uri, timeout=timeout)

    def create_from_snapshot(self, data, timeout=-1):
        """
        Creates a new volume on the storage system from a snapshot of a volume.
        A volume template must also be specified when creating a volume from a snapshot.

        The global setting "StorageVolumeTemplateRequired" controls whether or
        not root volume templates can be used to provision volumes.
        The value of this setting defaults to "false".
        If the value is set to "true", then only templates with an "isRoot" value of "false"
        can be used to provision a volume.

        Args:
            data (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created data.
        """
        uri = self.URI + "/from-snapshot"
        return self._helper.create(data, uri=uri, timeout=timeout)

    def delete(self, force=False, export_only=None, suppress_device_updates=None, timeout=-1):
        """
        Deletes a managed volume.

        Args:
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            export_only:
                Valid prior to API500. By default, volumes will be deleted from OneView, and storage system.
                To delete the volume from OneView only, you must set its value to True.
                Setting its value to False has the same behavior as the default behavior.
            suppress_device_updates:
                Valid API500 onwards. By default, volumes will be deleted from OneView, and storage system.
                To delete the volume from OneView only, you must set its value to True.
                Setting its value to False has the same behavior as the default behavior.

        Returns:
            bool: Indicates if the volume was successfully deleted.
        """
        custom_headers = {'If-Match': '*'}
        uri = self.data["uri"]
        if suppress_device_updates:
            uri += '?suppressDeviceUpdates=true'
        if export_only:
            custom_headers['exportOnly'] = True
        return self._helper.delete(uri, force=force, timeout=timeout, custom_headers=custom_headers)

    def get_snapshots(self, start=0, count=-1, filter='', sort=''):
        """
        Gets all snapshots of a volume. Returns a list of snapshots based on optional sorting and filtering, and
        constrained by start and count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of snapshots.
        """
        self.__get_snapshot_object()
        return self._snapshots.get_all(start, count, filter=filter, sort=sort)

    def create_snapshot(self, snapshot, timeout=-1):
        """
        Creates a snapshot for the specified volume.

        Args:
            snapshot (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Storage volume.
        """
        self.__get_snapshot_object()
        return self._snapshots.create(snapshot, timeout=timeout)

    def get_snapshot_by_name(self, name):
        """
        Gets snapshot by name.

        Args:
            name: Snapshot name

        Returns:
            object: VolumeSnapshots
        """
        self.__get_snapshot_object()
        return self._snapshots.get_by_name(name)

    def get_snapshot_by_uri(self, uri):
        """
        Gets snapshot by uri.

        Args:
            uri: Snapshot uri

        Returns:
            object: VolumeSnapshots
        """
        self.__get_snapshot_object()
        return self._snapshots.get_by_uri(uri)

    def get_snapshot_by(self, field, value):
        """
        Gets all snapshots that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: Snapshots
        """
        self.__get_snapshot_object()
        return self._snapshots.get_by(field, value)

    def get_extra_managed_storage_volume_paths(self, start=0, count=-1, filter='', sort=''):
        """
        Gets the list of extra managed storage volume paths.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of extra managed storage volume paths.
        """
        uri = self.URI + '/repair?alertFixType=ExtraManagedStorageVolumePaths'
        return self._helper.get_all(start, count, filter=filter, sort=sort, uri=uri)

    def repair(self, timeout=-1):
        """
        Removes extra presentations from a specified volume on the storage system.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Storage volume.
        """
        data = {
            "type": "ExtraManagedStorageVolumePaths",
            "resourceUri": self.data["uri"]
        }
        custom_headers = {'Accept-Language': 'en_US'}
        uri = self.URI + '/repair'
        return self._helper.create(data, uri=uri, timeout=timeout, custom_headers=custom_headers)

    def get_attachable_volumes(self, start=0, count=-1, filter='', query='', sort='', scope_uris='', connections=''):
        """
        Gets the volumes that are connected on the specified networks based on the storage system port's expected
        network connectivity.

        A volume is attachable if it satisfies either of the following conditions:
            * The volume is shareable.
            * The volume not shareable and not attached.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            query:
                A general query string to narrow the list of resources returned. The default
                is no query; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            connections:
                A list of dicts specifics the connections used by the attachable volumes. Needs network uri, initiatoer
                name and optional proxy name
            scope_uris:
                A list specifics the list of scope uris used by the attachable volumed.

        Returns:
            list: A list of attachable volumes that the appliance manages.
        """
        uri = self.URI + '/attachable-volumes'
        if connections:
            uri += str('?' + 'connections=' + connections.__str__())
            uri = uri.replace(" ", "")
        return self._helper.get_all(start, count, filter=filter, query=query, sort=sort, uri=uri, scope_uris=scope_uris)
