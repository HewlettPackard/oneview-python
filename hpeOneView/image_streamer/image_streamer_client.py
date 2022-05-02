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
"""
This module implements a common client for HPE Image Streamer REST API.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


from hpeOneView.connection import connection
from hpeOneView.image_streamer.resources.golden_images import GoldenImages
from hpeOneView.image_streamer.resources.plan_scripts import PlanScripts
from hpeOneView.image_streamer.resources.build_plans import BuildPlans
from hpeOneView.image_streamer.resources.os_volumes import OsVolumes
from hpeOneView.image_streamer.resources.deployment_plans import DeploymentPlans
from hpeOneView.image_streamer.resources.artifact_bundles import ArtifactBundles
from hpeOneView.image_streamer.resources.deployment_groups import DeploymentGroups


class ImageStreamerClient(object):
    def __init__(self, ip, session_id, api_version, sslBundle=False):
        self.__connection = connection(ip, api_version, sslBundle)
        self.__connection.set_session_id(session_id)
        self.__golden_images = None
        self.__plan_scripts = None
        self.__build_plans = None
        self.__os_volumes = None
        self.__deployment_plans = None
        self.__artifact_bundles = None
        self.__deployment_groups = None

    @property
    def connection(self):
        """
        Gets the underlying HPE Image Streamer connection used by the ImageStreamerClient.

        Returns:
            connection:
        """
        return self.__connection

    @property
    def golden_images(self):
        """
        Gets the Golden Images API client.

        Returns:
            GoldenImages:
        """
        if not self.__golden_images:
            self.__golden_images = GoldenImages(self.__connection)
        return self.__golden_images

    @property
    def plan_scripts(self):
        """
        Gets the Plan Scripts API client.

        Returns:
            PlanScripts:
        """
        if not self.__plan_scripts:
            self.__plan_scripts = PlanScripts(self.__connection)
        return self.__plan_scripts

    @property
    def build_plans(self):
        """
        Gets the Build Plans API client.

        Returns:
            BuildPlans:
        """
        if not self.__build_plans:
            self.__build_plans = BuildPlans(self.__connection)
        return self.__build_plans

    @property
    def os_volumes(self):
        """
        Gets the OS Volumes API client.

        Returns:
            OsVolumes:
        """
        if not self.__os_volumes:
            self.__os_volumes = OsVolumes(self.__connection)
        return self.__os_volumes

    @property
    def deployment_plans(self):
        """
        Gets the Deployment Plans API client.

        Returns:
            DeploymentPlans:
        """
        return DeploymentPlans(self.__connection)

    @property
    def artifact_bundles(self):
        """
        Gets the Artifact Bundles API client.

        Returns:
            ArtifactBundles:
        """
        return ArtifactBundles(self.__connection)

    @property
    def deployment_groups(self):
        """
        Gets the Deployment Groups API client.

        Returns:
            DeploymentGroups:
        """
        if not self.__deployment_groups:
            self.__deployment_groups = DeploymentGroups(self.__connection)
        return self.__deployment_groups
