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
from hpeOneView.resources.resource import Resource, ResourcePatchMixin, ResourceHelper
from hpeOneView.resources.settings.scopes import Scopes
from hpeOneView.resources.search.index_resources import IndexResources


class ScopesTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        self.oneview_connection = connection(self.DEFAULT_HOST, 800)
        self.resource = Scopes(self.oneview_connection)
        self.indexresource = IndexResources(self.oneview_connection)
        self.resource.data = {'uri': 'uri1'}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get_all):
        sort = 'name:ascending'
        query = 'name eq "TestName"'
        view = 'expand'
        filter = 'name:'

        self.resource.get_all(2, 500, filter, sort, query, view)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query=query, view=view)

    @mock.patch.object(Resource, 'update')
    def test_update_called_once(self, mock_update):
        data = {
            'name': 'Name of the Scope',
            'uri': 'a_uri'
        }
        data_rest_call = data.copy()

        self.resource.update(data, 60)

        headers = {'If-Match': '*'}
        mock_update.assert_called_once_with(data_rest_call, timeout=60,
                                            custom_headers=headers)

    @mock.patch.object(Resource, 'update')
    def test_update_should_verify_if_match_etag_when_provided(self, mock_update):
        data = {'eTag': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}

        self.resource.update(data, -1)

        headers = {'If-Match': '2016-11-03T18:41:10.751Z/2016-11-03T18:41:10.751Z'}
        mock_update.assert_called_once_with(mock.ANY, timeout=mock.ANY, custom_headers=headers)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.resource.delete(timeout=-1)

        mock_delete.assert_called_once_with(timeout=-1, custom_headers={'If-Match': '*'})

    @mock.patch.object(Resource, 'get_by_uri')
    @mock.patch.object(IndexResources, 'get_all')
    def test_get_with_uri_called_once(self, mock_get_resources, mock_get):
        uri = '/rest/scopes/3518be0e-17c1-4189-8f81-83f3724f6155'
        mock_get_resources.return_value = [{'uri': 'uri1'}, {'uri': 'uri2'}]
        fake_obj = mock.Mock()
        fake_obj.data = {'uri': 'uri1'}
        mock_get.return_value = fake_obj
        result = self.resource.get_by_uri(uri).data
        mock_get.assert_called_once_with(uri)
        self.assertEqual(result['addedResourceUris'], ['uri1', 'uri2'])

    @mock.patch.object(Resource, 'get_by_name')
    @mock.patch.object(IndexResources, 'get_all')
    def test_get_by_name_called_once(self, mock_get_resources, mock_get_name):
        mock_get_resources.return_value = [{'uri': 'uri1'}, {'uri': 'uri2'}]
        fake_obj = mock.Mock()
        fake_obj.data = {'uri': 'uri1'}
        mock_get_name.return_value = fake_obj
        result = self.resource.get_by_name('test').data
        mock_get_name.assert_called_once_with('test')
        self.assertEqual(result['addedResourceUris'], ['uri1', 'uri2'])

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_update_resource_assignments_called_once(self, mock_patch_request):
        uri = '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2'

        information = {
            "addedResourceUris": ["/rest/ethernet-networks/e801b73f-b4e8-4b32-b042-36f5bac2d60f"],
            "removedResourceUris": ["/rest/ethernet-networks/390bc9f9-cdd5-4c70-b38f-cf04e64f5c72"]
        }
        self.resource.update_resource_assignments(uri, information, timeout=-1)

        mock_patch_request.assert_called_once_with(
            '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2/resource-assignments',
            information.copy(),
            timeout=-1)
