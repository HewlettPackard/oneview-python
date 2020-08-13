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

from hpeOneView.connection import connection
from hpeOneView.resources.data_services.metric_streaming import MetricStreaming
from hpeOneView.resources.resource import ResourceClient


class MetricStreamingTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._metrics = MetricStreaming(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_capability_called_once(self, mock_get):
        self._metrics.get_capability()
        mock_get.assert_called_once_with("/rest/metrics/capability")

    @mock.patch.object(ResourceClient, 'get')
    def test_get_configuration_called_once(self, mock_get):
        self._metrics.get_configuration()
        mock_get.assert_called_once_with("/rest/metrics/configuration")

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        configuration = {
            "sourceTypeList": [
                {
                    "sourceType": "/rest/power-devices",
                    "sampleIntervalInSeconds": "300",
                    "frequencyOfRelayInSeconds": "3600"
                }
            ]
        }
        configuration_rest_call = configuration.copy()
        mock_update.return_value = configuration

        self._metrics.update_configuration(configuration)
        mock_update.assert_called_once_with(configuration_rest_call, uri="/rest/metrics/configuration")
