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

import json
import os

CUR_MODULE_DIR = os.path.dirname(__file__)
DEFAULT_EXAMPLE_CONFIG_FILE = os.path.join(CUR_MODULE_DIR, 'config.json')


def try_load_from_file(config, file_name=None):
    if not file_name:
        file_name = DEFAULT_EXAMPLE_CONFIG_FILE

    if not os.path.isfile(file_name):
        return config

    with open(file_name) as json_data:
        return json.load(json_data)
