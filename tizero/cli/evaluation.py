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
from typing import Dict, List, Optional

import numpy as np
from openrl.arena import make_arena
from openrl.arena.agents.jidi_agent import JiDiAgent
from openrl.envs.PettingZoo.registration import register
from openrl.envs.wrappers.pettingzoo_wrappers import RecordWinner

from tizero.football_env.football_pettingzoo import FootballAECEnv

register("GFootball/11_vs_11_jidi_eval", FootballAECEnv)


def fix_dispatch_func(
    np_random: np.random.Generator,
    players: List[str],
    agent_names: List[str],
) -> Dict[str, str]:
    assert len(players) == len(
        agent_names
    ), "The number of players must be equal to the number of agents."
    assert len(players) == 2, "The number of players must be equal to 2."
    return dict(zip(players, agent_names))


def evaluation(
    left_agent: str,
    right_agent: str,
    total_game: int,
    game_length: int,
    parallel: Optional[bool] = True,
    max_game_onetime: int = 2,
    seed: int = 0,
):
    env_wrappers = [RecordWinner]

    arena = make_arena("GFootball/11_vs_11_jidi_eval", env_wrappers=env_wrappers)
    player_num = 11
    left_agent = JiDiAgent(left_agent, player_num=player_num)
    right_agent = JiDiAgent(right_agent, player_num=player_num)

    arena.reset(
        agents={"left_agent": left_agent, "right_agent": right_agent},
        total_games=total_game,
        max_game_onetime=max_game_onetime,
        seed=seed,
        dispatch_func=fix_dispatch_func,
    )
    parallel = True
    result = arena.run(parallel=parallel)
    arena.close()
    print(result)
    return result
