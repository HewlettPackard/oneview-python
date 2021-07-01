# -*- coding: utf-8 -*-
###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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


from setuptools import find_packages
from setuptools import setup

setup(name='hpeOneView',
      version='6.2.0',
      description='HPE OneView Python Library',
      url='https://github.com/HewlettPackard/oneview-python',
      download_url="https://github.com/HewlettPackard/oneview-python/tarball/v6.2.0",
      author='Hewlett Packard Enterprise Development LP',
      author_email='oneview-pythonsdk@hpe.com',
      license='Apache',
      packages=find_packages(exclude=['examples*', 'tests*']),
      keywords=['oneview', 'hpe'],
      long_description_content_type="text/markdown",
      install_requires=['future>=0.15.2'])
