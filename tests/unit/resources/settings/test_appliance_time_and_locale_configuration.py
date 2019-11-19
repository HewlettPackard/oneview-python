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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.settings.appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfiguration
from hpOneView.resources.resource import ResourceClient


class ApplianceTimeAndLocaleConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._time_and_locale = ApplianceTimeAndLocaleConfiguration(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._time_and_locale.get()
        mock_get.assert_called_once_with('/rest/appliance/configuration/time-locale')

    @mock.patch.object(ResourceClient, 'create')
    def test_update_called_once(self, mock_create):
        resource = {
            'dateTime': '2020-02-27T7:55:00.000Z',
            'locale': 'en_US.UTF-8',
            'localeDisplayName': 'English (United States)',
            'ntpServers': ['127.0.0.1'],
            'timezone': 'UTC',
            'uri': None
        }
        self._time_and_locale.update(resource)
        mock_create.assert_called_once_with(resource, timeout=-1, default_values=self._time_and_locale.DEFAULT_VALUES)
