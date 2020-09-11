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
from hpeOneView.resources.activity.alerts import Alerts
from hpeOneView.resources.resource import ResourceClient


class AlertsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host, 800)
        self._client = Alerts(self.connection)

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
        self._client.get('35323930-4936-4450-5531-303153474820')
        mock_get.assert_called_once_with('35323930-4936-4450-5531-303153474820')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('alertState', 'Active')
        mock_get_by.assert_called_once_with('alertState', 'Active')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_fail_when_no_uri_is_provided(self, mock_update):
        resource = {
            'alertState': 'Cleared',
            'assignedToUser': 'Paul',
            'alertUrgency': 'None',
            'notes': 'Problem fixed',
            'eTag': '2014-03-28T04:40:06.831Z'
        }
        self.assertRaises(ValueError, self._client.update, resource)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values_by_resource_uri(self, mock_update):
        resource = {
            'uri': '/rest/alerts/26',
            'alertState': 'Cleared',
            'assignedToUser': 'Paul',
            'alertUrgency': 'None',
            'notes': 'Problem fixed',
            'eTag': '2014-03-28T04:40:06.831Z'
        }
        self._client.update(resource.copy(), '/rest/alerts/26')
        resource_test = resource.copy()
        del resource_test["uri"]
        mock_update.assert_called_once_with(resource=resource_test, timeout=-1, uri='/rest/alerts/26')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values_by_uri_param(self, mock_update):
        resource = {
            'alertState': 'Cleared',
            'assignedToUser': 'Paul',
            'alertUrgency': 'None',
            'notes': 'Problem fixed',
            'eTag': '2014-03-28T04:40:06.831Z'
        }
        self._client.update(resource, '/rest/alerts/26')
        mock_update.assert_called_once_with(resource=resource.copy(), timeout=-1, uri='/rest/alerts/26')

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id_alert = '35323930-4936-4450-5531-303153474820'
        self._client.delete(id_alert)
        mock_delete.assert_called_once_with(id_alert)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_alert_change_log_called_once_by_id(self, mock_delete):
        id_alert = '20'
        self._client.delete_alert_change_log(id_alert)
        mock_delete.assert_called_once_with({'uri': '/rest/alerts/AlertChangeLog/20'})

    @mock.patch.object(ResourceClient, 'delete_all')
    def test_delete_all_called_once(self, mock_delete):
        self._client.delete_all('name="name"')
        mock_delete.assert_called_once_with(filter='name="name"', timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_alert_change_log_called_once_by_uri(self, mock_delete):
        uri = '/rest/alerts/AlertChangeLog/20'
        self._client.delete_alert_change_log(uri)
        mock_delete.assert_called_once_with(
            {'uri': uri})
