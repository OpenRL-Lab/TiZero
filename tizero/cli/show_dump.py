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
from pathlib import Path

from tizero.utils.visualize_tools.tools.tracer import MatchTracer
from tizero.utils.visualize_tools.visualizer import Visualizer


def show_dump(dump_file):
    assert Path(dump_file).exists()

    tracer = MatchTracer.load_from_official_trace(dump_file)
    visualizer = Visualizer(tracer, disable_RGB=False)
    visualizer.run()
