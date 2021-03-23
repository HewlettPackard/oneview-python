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

import unittest

import mock

from hpeOneView.connection import connection
from hpeOneView.resources.search.labels import Labels
from hpeOneView.resources.resource import Resource, ResourceHelper


class LabelsTest(unittest.TestCase):

    RESOURCE_LABEL = dict(
        uri="/rest/labels/resources/rest/resource/uri",
        resourceUri="/rest/resource/uri",
        type="ResourceLabels",
        category="the-resource-category",
        created="2014-03-31T02:08:27.884Z",
        modified="2014-03-31T02:08:27.884Z",
        eTag=None,
        labels=[
            dict(name="new label", uri=None),
            dict(name="old label", uri="/rest/labels/3")
        ]
    )

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._labels = Labels(self.connection)
        self.uri = "/rest/labels/2"
        self._labels.data = {"uri": self.uri}

    @mock.patch.object(Resource, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self._labels.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter, sort)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_called_once(self, mock_get):
        label_uri = "/rest/labels/2"
        self._labels.get_by_uri(label_uri)
        mock_get.assert_called_once_with(label_uri)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_resource(self, mock_get):
        resource_uri = "/rest/enclosures/09SGH100X6J1"
        self._labels.get_by_resource(resource_uri)
        expected_uri = '/rest/labels/resources/' + resource_uri
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            resourceUri="/rest/enclosures/09SGH100X6J1",
            labels=["labelSample2", "enclosureDemo"]
        )
        self._labels.create(resource, timeout=30)
        expected_uri = '/rest/labels/resources'
        mock_create.assert_called_once_with(resource, timeout=30, uri=expected_uri)

    @mock.patch.object(Resource, 'update')
    def test_update_called_once(self, mock_update):
        self._labels.update(resource=self.RESOURCE_LABEL)
        mock_update.assert_called_once_with(resource=self.RESOURCE_LABEL)

    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._labels.delete(resource=self.RESOURCE_LABEL)
        mock_delete.assert_called_once_with(resource=self.RESOURCE_LABEL)
