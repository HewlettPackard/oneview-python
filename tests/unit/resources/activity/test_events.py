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

from hpOneView.connection import connection
from hpOneView.resources.activity.events import Events
from hpOneView.resources.resource import ResourceClient


class EventsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = Events(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get):
        self._client.get_all(filter="name='name'",
                             sort='name:ascending',
                             view='day')
        mock_get.assert_called_once_with(count=-1,
                                         filter="name='name'",
                                         query='', sort='name:ascending', start=0, view='day')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_specific(self, mock_get):
        self._client.get('/rest/events/fake_uri')
        mock_get.assert_called_once_with('/rest/events/fake_uri')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('eventTypeID', 'hp.justATest')
        mock_get_by.assert_called_once_with('eventTypeID', 'hp.justATest')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            "description": "This is a very simple test event",
            "serviceEventSource": True,
            "serviceEventDetails": {
                "caseId": "1234",
                "primaryContact": "contactDetails",
                "remoteSupportState": "Submitted"
            },
            "severity": "OK",
            "healthCategory": "PROCESSOR",
            "eventTypeID": "hp.justATest",
            "rxTime": "2012-05-14T20:23:56.688Z",
            "urgency": "None",
            "eventDetails":
            [{"eventItemName": "ipv4Address",
                "eventItemValue": "198.51.100.5",
                "isThisVarbindData": False,
                "varBindOrderIndex": -1}]
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._client.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30,
                                            default_values=self._client.DEFAULT_VALUES)
