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


@click.group(invoke_without_command=True)
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
@click.pass_context
def run(ctx):
    if ctx.invoked_subcommand is None:
        pass
    else:
        pass


@run.command()
@click.option(
    "--left_agent",
    type=str,
    help="left agent path",
)
@click.option(
    "--right_agent",
    type=str,
    help="right agent path",
)
@click.option(
    "--total_game",
    type=int,
    default=1,
    help="total games to run",
)
@click.option(
    "--game_length",
    type=int,
    default=3000,
    help="max length of one game",
)
def eval(left_agent: str, right_agent: str, total_game: int, game_length: int):
    from tizero.cli.evaluation import evaluation

    evaluation(
        left_agent=left_agent,
        right_agent=right_agent,
        total_game=total_game,
        game_length=game_length,
    )


@run.command()
@click.argument("input")
@click.argument("output")
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
def dump2video(input: str, output: str, episode_length: int, render_type: str):
    from tizero.cli.dump2video import dump2video

    dump2video(
        input=input,
        output=output,
        episode_length=episode_length,
        render_type=render_type,
    )


@run.command()
@click.argument("input")
def show(input: str):
    from tizero.cli.show_dump import show_dump

    show_dump(
        dump_file=input,
    )


@run.command()
@click.argument("input")
def keypoint(input: str):
    from tizero.cli.show_keypoint import show_keypoint

    show_keypoint(
        dump_file=input,
    )
