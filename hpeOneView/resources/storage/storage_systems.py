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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpeOneView.resources.resource import Resource


class StorageSystems(Resource):
    """
    Storage Systems API client.

    """
    URI = '/rest/storage-systems'

    def __init__(self, connection, data=None):
        super(StorageSystems, self).__init__(connection, data)

    def add(self, resource, timeout=-1):
        """
        Adds a storage system for management by the appliance. The storage system resource created will be in a
        Connected state and will not yet be available for further operations. Users are required to perform a PUT API
        on the storage system resource to complete the management of the storage system resource. An asynchronous task
        will be created as a result of this API call to discover available domains, target ports, and storage pools.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created storage system.
        """
        return self.create(resource, timeout=timeout)

    def get_host_types(self):
        """
        Gets the list of supported host types.

        Returns:
            list: Host types.
        """
        uri = self.URI + "/host-types"
        return self._helper.do_get(uri)

    def get_storage_pools(self):
        """
        Gets a list of Storage pools. Returns a list of storage pools belonging to the storage system referred by the
        Path property {ID} parameter or URI.

        Returns:
            dict: Host types.
        """
        uri = "{}/storage-pools".format(self.data["uri"])
        return self._helper.do_get(uri)

    def remove(self, force=False, timeout=-1):
        """
        Removes the storage system from OneView.

        Args:
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Details of associated resource.
        """
        headers = {'If-Match': '*'}
        return self.delete(force=force, timeout=timeout, custom_headers=headers)

    def get_managed_ports(self, port_id_or_uri=''):
        """
        Gets all ports or a specific managed target port for the specified storage system.

        Args:
            port_id_or_uri: Can be either the port id or the port uri.

        Returns:
            dict: Managed ports.
        """
        if port_id_or_uri:
            uri = self._helper.build_uri(port_id_or_uri)
            if "/managedPorts" not in uri:
                uri = "{}/managedPorts/{}".format(self.data["uri"], port_id_or_uri)

        else:
            uri = "{}/managedPorts".format(self.data["uri"])

        return self._helper.get_collection(uri)

    def get_by_ip_hostname(self, ip_hostname):
        """
        Retrieve a storage system by its IP.

        Works only with API version <= 300.

        Args:
            ip_hostname: Storage system IP or hostname.

        Returns:
            dict
        """
        resources = self.get_all()

        resources_filtered = [x for x in resources if x['credentials']['ip_hostname'] == ip_hostname]

        if resources_filtered:
            return self.new(self._connection, resources_filtered[0])
        else:
            return None

    def get_by_hostname(self, hostname):
        """
        Retrieve a storage system by its hostname.

        Works only in API500 onwards.

        Args:
            hostname: Storage system hostname.

        Returns:
            dict
        """
        resources = self.get_all()

        resources_filtered = [x for x in resources if x['hostname'] == hostname]

        if resources_filtered:
            return self.new(self._connection, resources_filtered[0])
        else:
            return None

    def get_reachable_ports(self, start=0, count=-1, filter='', query='', sort='', networks=[]):
        """
        Gets the storage ports that are connected on the specified networks
        based on the storage system port's expected network connectivity.

        Returns:
            list: Reachable Storage Port List.
        """
        uri = "{}/reachable-ports".format(self.data["uri"])

        if networks:
            elements = "\'"
            for n in networks:
                elements += n + ','
            elements = elements[:-1] + "\'"
            uri = uri + "?networks=" + elements

        return self._helper.do_get(self._helper.build_query_uri(start=start, count=count, filter=filter, query=query,
                                                                sort=sort, uri=uri))

    def get_templates(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets a list of volume templates. Returns a list of storage templates belonging to the storage system.

        Returns:
            list: Storage Template List.
        """
        uri = "{}/templates".format(self.data["uri"])
        return self._helper.do_get(self._helper.build_query_uri(start=start, count=count, filter=filter,
                                                                query=query, sort=sort, uri=uri))
