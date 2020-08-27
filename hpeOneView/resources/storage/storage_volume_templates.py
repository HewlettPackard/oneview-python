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


class StorageVolumeTemplates(Resource):
    """
    Storage Volume Templates API client.

    """
    URI = '/rest/storage-volume-templates'

    DEFAULT_VALUES = {
        '200': {"type": "StorageVolumeTemplateV3"},
        '300': {"type": "StorageVolumeTemplateV3"}
    }

    def __init__(self, connection, data=None):
        super(StorageVolumeTemplates, self).__init__(connection, data)

    def get_connectable_volume_templates(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets the storage volume templates that are available on the specified networks based on the storage system
        port's expected network connectivity. If there are no storage volume templates that meet the specified
        connectivity criteria, an empty collection will be returned.

        Returns:
            list: Storage volume templates.
        """
        uri = self.URI + "/connectable-volume-templates"

        get_uri = self._helper.build_query_uri(start=start, count=count, filter=filter,
                                               query=query, sort=sort, uri=uri)
        return self._helper.do_get(get_uri)

    def get_reachable_volume_templates(self, start=0, count=-1, filter='', query='', sort='',
                                       networks=None, scope_uris='', private_allowed_only=False):
        """
        Gets the storage templates that are connected on the specified networks based on the storage system
        port's expected network connectivity.

        Returns:
            list: Storage volume templates.
        """
        uri = self.URI + "/reachable-volume-templates"

        uri += "?networks={}&privateAllowedOnly={}".format(networks, private_allowed_only)

        get_uri = self._helper.build_query_uri(start=start, count=count, filter=filter,
                                               query=query, sort=sort, uri=uri, scope_uris=scope_uris)
        return self._helper.do_get(get_uri)

    def get_compatible_systems(self):
        """
        Retrieves a collection of all storage systems that is applicable to this storage volume template.

        Returns:
            list: Storage systems.
        """
        uri = "{}/compatible-systems".format(self.data["uri"])
        return self._helper.do_get(uri)

    def delete(self, force=False, timeout=-1):
        """
        Deletes the specified storage volume template.

        Args:
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        custom_headers = {'Accept-Language': 'en_US', 'If-Match': '*'}
        uri = self.data['uri']

        return self._helper.delete(uri, force=force, timeout=timeout, custom_headers=custom_headers)
