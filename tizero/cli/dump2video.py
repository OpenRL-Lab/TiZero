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


def dump2video(input: str, output: str, episode_length: int, render_type: str) -> None:
    from tizero.utils import script_helpers

    if render_type == "2d":
        print("saving as 2d video")
        script_helpers.ScriptHelpers().dump_to_video(
            dump_file=input, directory=output, episode_length=episode_length
        )
    elif render_type == "3d":
        print("saving as 3d video")
        script_helpers.ScriptHelpers().replay(
            dump=input,
            fps=10,
            directory=output,
            episode_length=episode_length,
            render_type=render_type,
        )
    else:
        raise ValueError("render_type must be 2d or 3d, but got {}".format(render_type))
