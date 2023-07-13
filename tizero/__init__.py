#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 The OpenRL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""""""


__TITLE__ = "tizero"
__VERSION__ = "v0.0.3"
__DESCRIPTION__ = "Toolkit and Agents for Google Research Football"
__AUTHOR__ = "OpenRL Contributors"
__EMAIL__ = "huangshiyu@4paradigm.com"
__version__ = __VERSION__

import platform

python_version_list = list(map(int, platform.python_version_tuple()))
assert python_version_list >= [
    3,
    8,
    0,
], (
    "tizero requires Python 3.8 or newer, but your Python is"
    f" {platform.python_version()}"
)
