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

import click
from click.core import Context, Option
from termcolor import colored

from tizero import __AUTHOR__, __EMAIL__, __TITLE__, __VERSION__
from tizero.utils.util import get_system_info


def red(text: str):
    return colored(text, "red")


def print_version(
    ctx: Context,
    param: Option,
    value: bool,
) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.secho(f"{__TITLE__.upper()} version: {red(__VERSION__)}")
    click.secho(f"Developed by {__AUTHOR__}, Email: {red(__EMAIL__)}")
    ctx.exit()


def print_system_info(
    ctx: Context,
    param: Option,
    value: bool,
) -> None:
    if not value or ctx.resilient_parsing:
        return
    info_dict = get_system_info()
    for key, value in info_dict.items():
        click.secho(f"- {key}: {red(value)}")
    ctx.exit()


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show package's version information.",
)
@click.option(
    "--system_info",
    is_flag=True,
    callback=print_system_info,
    expose_value=False,
    is_eager=True,
    help="Show system information.",
)
@click.option(
    "--tool",
    prompt="Choose a tool to use",
    type=click.Choice(
        [
            "dump2video",
        ]
    ),
    help="tool name",
)
@click.option(
    "--input",
    prompt="Please enter input file path or directory",
    type=str,
    help="input file path or directory",
)
@click.option(
    "--output",
    prompt="Please enter output file path or directory",
    type=str,
    help="output file path or directory",
)
@click.option(
    "--episode_length",
    type=int,
    default=None,
    help="episode length",
)
@click.option(
    "--render_type",
    type=click.Choice(
        [
            "2d",
            "3d",
        ]
    ),
    default="2d",
    help="render type",
)
def run(tool: str, input: str, output: str, episode_length: int, render_type: str):
    if tool == "dump2video":
        from tizero.cli.dump2video import dump2video

        dump2video(
            input=input,
            output=output,
            episode_length=episode_length,
            render_type=render_type,
        )
    else:
        raise NotImplementedError
