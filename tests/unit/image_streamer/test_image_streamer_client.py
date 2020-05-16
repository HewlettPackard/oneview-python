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

from hpOneView.image_streamer.image_streamer_client import ImageStreamerClient
from hpOneView.image_streamer.resources.plan_scripts import PlanScripts
from hpOneView.image_streamer.resources.golden_images import GoldenImages
from hpOneView.image_streamer.resources.build_plans import BuildPlans
from hpOneView.image_streamer.resources.os_volumes import OsVolumes
from hpOneView.image_streamer.resources.deployment_plans import DeploymentPlans
from hpOneView.image_streamer.resources.artifact_bundles import ArtifactBundles
from hpOneView.image_streamer.resources.deployment_groups import DeploymentGroups


class ImageStreamerClientTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.session_id = 'LTU1NzIzMDMxMjIxcsgLtu5d6Q_oydNqaO2oWuZz5Xj7L7cc'
        self._client = ImageStreamerClient(self.host, self.session_id, 300)

    def test_connection_has_right_host(self):
        self.assertEqual(self._client.connection.get_host(), self.host)

    def test_connection_has_right_session_id(self):
        self.assertEqual(self._client.connection.get_session_id(), self.session_id)

    def test_connection_has_session(self):
        self.assertEqual(self._client.connection.get_session(), True)

    def test_golden_images_has_right_type(self):
        self.assertIsInstance(self._client.golden_images, GoldenImages)

    def test_golden_images_lazy_loading(self):
        resource = self._client.golden_images
        self.assertEqual(resource, self._client.golden_images)

    def test_plan_scripts_has_right_type(self):
        self.assertIsInstance(self._client.plan_scripts, PlanScripts)

    def test_plan_scripts_lazy_loading(self):
        resource = self._client.plan_scripts
        self.assertEqual(resource, self._client.plan_scripts)

    def test_build_plans_has_right_type(self):
        self.assertIsInstance(self._client.build_plans, BuildPlans)

    def test_build_plans_lazy_loading(self):
        resource = self._client.build_plans
        self.assertEqual(resource, self._client.build_plans)

    def test_os_volumes_has_right_type(self):
        self.assertIsInstance(self._client.os_volumes, OsVolumes)

    def test_os_volumes_lazy_loading(self):
        resource = self._client.os_volumes
        self.assertEqual(resource, self._client.os_volumes)

    def test_deployment_plans_has_right_type(self):
        self.assertIsInstance(self._client.deployment_plans, DeploymentPlans)

    def test_deployment_plans_client(self):
        resource = self._client.deployment_plans
        self.assertNotEqual(resource, self._client.deployment_plans)

    def test_artifact_bundles_has_right_type(self):
        self.assertIsInstance(self._client.artifact_bundles, ArtifactBundles)

    def test_artifact_bundles_client(self):
        resource = self._client.artifact_bundles
        self.assertNotEqual(resource, self._client.artifact_bundles)

    def test_deployment_groups_has_right_type(self):
        self.assertIsInstance(self._client.deployment_groups, DeploymentGroups)

    def test_deployment_groups_lazy_loading(self):
        resource = self._client.deployment_groups
        self.assertEqual(resource, self._client.deployment_groups)
