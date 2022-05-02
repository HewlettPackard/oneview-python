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

from hpeOneView.resources.resource import ResourceClient


class MetricStreaming(object):
    """
    Metrics API client.

    Metrics can be relayed from OneView for managed resources at a specified interval. The following steps can be
    followed to enable the metric relay in OneView:

        * Get the list of resource types and metrics which can be configured for live streaming
        * Configure the live metric stream in OneView
        * Receive the stream of metric on MSMB

    The list below describes the structure of message relayed to MSMB:
        startTime (str):
            The starting time of the metric collection.
        sampleIntervalInSeconds (int):
            Interval between samples.
        numberOfSamples (int):
            Number of samples in the list for each metric type.
        resourceType (str):
            Identifies the resource type.
        resourceDataList (list):
            Metric sample list.
        uri (str):
            Canonical URI of the resource.
        category (str):
            Identifies the category of resource. The supported devices are server-hardware, enclosures, and
            power-devices.
        created (timestamp):
            Date and time when the resource was created.
        modified (timestamp):
            Date and time when the resource was last modified.
        eTag (str):
            Entity tag/version ID of the resource, the same value that is returned in the ETag header on a GET of the
            resource.
        type (str):
            Uniquely identifies the type of the JSON object.

    """
    URI = '/rest/metrics'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_capability(self):
        """
        Fetches the list of resource types and supported metrics that OneView is capable of relaying.

        Returns:
            list: List of resource types and supported metrics.
        """
        return self._client.get(self.URI + "/capability")

    def get_configuration(self):
        """
        Fetches the current configuration for which metrics are being relayed.

        Returns:
            list: List of objects which contain frequency, sample interval, and source type for each resource-type.

        """
        return self._client.get(self.URI + "/configuration")

    def update_configuration(self, configuration):
        """
        Updates the metrics configuration with the new values. Overwrites the existing configuration.

        Args:
            configuration (dict):
                Dictionary with a list of objects which contain frequency, sample interval, and source type for each
                resource-type.

        Returns:
            dict: The current configuration for which metrics are being relayed.

        """
        return self._client.update(configuration, uri=self.URI + "/configuration")
