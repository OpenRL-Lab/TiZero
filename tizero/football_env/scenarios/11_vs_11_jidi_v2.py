# coding=utf-8
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from . import *


def build_scenario(builder):
    # jidi比赛用的11_vs_11_stochastic，但是11_vs_11_kaggle的right_team_difficulty=0.6，会导致左右双方能力不一致
    # 所以这里把right_team_difficulty改成了1.0
    # 另外，这个scenario每次环境reset后会切换双方球员位置。这个scenario有半场！
    builder.config().game_duration = 3000

    builder.config().second_half = 1500

    builder.config().left_team_difficulty = 1.0
    builder.config().right_team_difficulty = 1.0

    builder.config().deterministic = False
    if builder.EpisodeNumber() % 2 == 0:
        first_team = Team.e_Left
        second_team = Team.e_Right
    else:
        first_team = Team.e_Right
        second_team = Team.e_Left
    builder.SetTeam(first_team)
    builder.AddPlayer(-1.000000, 0.000000, e_PlayerRole_GK, controllable=True)
    builder.AddPlayer(0.000000, 0.020000, e_PlayerRole_RM)
    builder.AddPlayer(0.000000, -0.020000, e_PlayerRole_CF)
    builder.AddPlayer(-0.422000, -0.19576, e_PlayerRole_LB)
    builder.AddPlayer(-0.500000, -0.06356, e_PlayerRole_CB)
    builder.AddPlayer(-0.500000, 0.063559, e_PlayerRole_CB)
    builder.AddPlayer(-0.422000, 0.195760, e_PlayerRole_RB)
    builder.AddPlayer(-0.184212, -0.10568, e_PlayerRole_CM)
    builder.AddPlayer(-0.267574, 0.000000, e_PlayerRole_CM)
    builder.AddPlayer(-0.184212, 0.105680, e_PlayerRole_CM)
    builder.AddPlayer(-0.010000, -0.21610, e_PlayerRole_LM)
    builder.SetTeam(second_team)
    builder.AddPlayer(-1.000000, 0.000000, e_PlayerRole_GK, controllable=True)
    builder.AddPlayer(-0.050000, 0.000000, e_PlayerRole_RM)
    builder.AddPlayer(-0.010000, 0.216102, e_PlayerRole_CF)
    builder.AddPlayer(-0.422000, -0.19576, e_PlayerRole_LB)
    builder.AddPlayer(-0.500000, -0.06356, e_PlayerRole_CB)
    builder.AddPlayer(-0.500000, 0.063559, e_PlayerRole_CB)
    builder.AddPlayer(-0.422000, 0.195760, e_PlayerRole_RB)
    builder.AddPlayer(-0.184212, -0.10568, e_PlayerRole_CM)
    builder.AddPlayer(-0.267574, 0.000000, e_PlayerRole_CM)
    builder.AddPlayer(-0.184212, 0.105680, e_PlayerRole_CM)
    builder.AddPlayer(-0.010000, -0.21610, e_PlayerRole_LM)
