#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2022 The TARTRL Authors.
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

import numpy as np
from tmarl.envs.football import football_env

""""""
# Actions.
IDLE = 0
LEFT = 1
TOP_LEFT = 2
TOP = 3
TOP_RIGHT = 4
RIGHT = 5
BOTTOM_RIGHT = 6
BOTTOM = 7
BOTTOM_LEFT = 8
LONG_PASS = 9
HIGH_PASS = 10
SHORT_PASS = 11
SHOT = 12
SPRINT = 13
RELEASE_DIRECTION = 14
RELEASE_SPRINT = 15
SLIDING = 16
DRIBBLE = 17
RELEASE_DRIBBLE = 18
STICKY_LEFT = 0
STICKY_TOP_LEFT = 1
STICKY_TOP = 2
STICKY_TOP_RIGHT = 3
STICKY_RIGHT = 4
STICKY_BOTTOM_RIGHT = 5
STICKY_BOTTOM = 6
STICKY_BOTTOM_LEFT = 7


RIGHT_ACTIONS = [TOP_RIGHT, RIGHT, BOTTOM_RIGHT, TOP, BOTTOM]
LEFT_ACTIONS = [TOP_LEFT, LEFT, BOTTOM_LEFT, TOP, BOTTOM]
BOTTOM_ACTIONS = [BOTTOM_LEFT, BOTTOM, BOTTOM_RIGHT, LEFT, RIGHT]
TOP_ACTIONS = [TOP_LEFT, TOP, TOP_RIGHT, LEFT, RIGHT]
ALL_DIRECTION_ACTIONS = [
    LEFT,
    TOP_LEFT,
    TOP,
    TOP_RIGHT,
    RIGHT,
    BOTTOM_RIGHT,
    BOTTOM,
    BOTTOM_LEFT,
]
ALL_DIRECTION_VECS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
]


def get_direction_action(
    available_action,
    sticky_actions,
    forbidden_action,
    target_action,
    active_direction,
    need_sprint,
):
    available_action[forbidden_action] = 0
    available_action[RELEASE_DIRECTION] = 0
    available_action[target_action] = 1
    target_direction = ALL_DIRECTION_VECS[target_action[0] - 1]
    target_direction = np.array(target_direction) / np.linalg.norm(
        np.array(target_direction)
    )
    if np.linalg.norm(active_direction) != 0:
        active_direction = active_direction / np.linalg.norm(active_direction)
        if np.dot(target_direction, active_direction) < 2**0.5 / 2:
            available_action[SPRINT] = 0
        elif need_sprint:
            if sticky_actions[8] == 0:
                available_action = np.zeros(19)
                available_action[SPRINT] = 1
            else:
                available_action[RELEASE_SPRINT] = 0
    else:
        available_action[SPRINT] = 0
    # if np.sum(sticky_actions[[act-1 for act in forbidden_action]]) > 0:
    #     available_action = np.zeros(19)
    #     available_action[RELEASE_DIRECTION] = 1
    return available_action


def test_scenario():
    if_visual = True
    env = football_env.create_environment(
        env_name="11_vs_11_jidi",
        stacked=False,
        logdir=(
            "/home/linfanqi/play_football/play_football/tmarl/envs/football/scenarios"
        ),
        representation="raw",
        rewards="scoring",
        write_goal_dumps=False,
        write_full_episode_dumps=True,
        render=if_visual,
        write_video=if_visual,
        dump_frequency=1,
        number_of_left_players_agent_controls=10,
        number_of_right_players_agent_controls=10,
        other_config_options={},
    )
    print("before reset")
    env.reset()
    raw_o, r, d, info = env.step([0] * 20)
    # for i in range(53):
    #     raw_o, r, d, info = env.step([7] * 20)
    # for xx in raw_o[0]['left_team']:
    #     print(xx)
    # for i in range(50):
    #     raw_o, r, d, info = env.step([3] * 20)
    # env.reset()
    for i in range(200):
        obs = raw_o[0]
        active_position = obs["left_team"][obs["active"]]
        sticky_actions = obs["sticky_actions"][:10]
        active_direction = obs["left_team_direction"][obs["active"]]
        relative_ball_position = obs["ball"][:2] - active_position
        all_directions_vecs = [
            np.array(v) / np.linalg.norm(np.array(v)) for v in ALL_DIRECTION_VECS
        ]
        best_direction = np.argmax(
            [np.dot(relative_ball_position, v) for v in all_directions_vecs]
        )
        target_direction = ALL_DIRECTION_ACTIONS[best_direction]
        if i > 10 and i < 40:
            target_direction = SPRINT
        raw_o, r, d, info = env.step([target_direction] + [0] * 19)

    # forbidden_actions = ALL_DIRECTION_ACTIONS.copy()
    # forbidden_actions.remove(target_direction)
    # available_action = get_direction_action(available_action, sticky_actions, forbidden_actions, [target_direction], active_direction, True)


if __name__ == "__main__":
    test_scenario()

# min_x = 100
#     max_x = -100
#     min_y = 100
#     max_y = -100
#     min_ball_direction_x = 100
#     max_ball_direction_x = -100
#     min_ball_direction_y = 100
#     max_ball_direction_y = -100
#     min_ball_direction_z = 100
#     max_ball_direction_z = -100

#     min_ball_rotation_x = 100
#     max_ball_rotation_x = -100
#     min_ball_rotation_y = 100
#     max_ball_rotation_y = -100
#     min_ball_rotation_z = 100
#     max_ball_rotation_z = -100

#     for j in range(2):
#         for i in range(3001):
#             random_action = np.random.randint(19, size=20)
#             raw_o, r, d, info = env.step(random_action)
#             for obs in raw_o[0]['left_team_direction']:
#                 if obs[0] < min_x:
#                     min_x = obs[0]
#                 if obs[0] > max_x:
#                     max_x = obs[0]
#                 if obs[1] < min_y:
#                     min_y = obs[1]
#                 if obs[1] > max_y:
#                     max_y = obs[1]
#             for obs in raw_o[0]['right_team_direction']:
#                 if obs[0] < min_x:
#                     min_x = obs[0]
#                 if obs[0] > max_x:
#                     max_x = obs[0]
#                 if obs[1] < min_y:
#                     min_y = obs[1]
#                 if obs[1] > max_y:
#                     max_y = obs[1]
#             if  raw_o[0]['ball_direction'][0] < min_ball_direction_x:
#                 min_ball_direction_x = raw_o[0]['ball_direction'][0]
#             if  raw_o[0]['ball_direction'][0] > max_ball_direction_x:
#                 max_ball_direction_x = raw_o[0]['ball_direction'][0]
#             if  raw_o[0]['ball_direction'][1] < min_ball_direction_y:
#                 min_ball_direction_y = raw_o[0]['ball_direction'][1]
#             if  raw_o[0]['ball_direction'][1] > max_ball_direction_y:
#                 max_ball_direction_y = raw_o[0]['ball_direction'][1]
#             if  raw_o[0]['ball_direction'][2] < min_ball_direction_z:
#                 min_ball_direction_z = raw_o[0]['ball_direction'][2]
#             if  raw_o[0]['ball_direction'][2] > max_ball_direction_z:
#                 max_ball_direction_z = raw_o[0]['ball_direction'][2]

#             if  raw_o[0]['ball_rotation'][0] < min_ball_rotation_x:
#                 min_ball_rotation_x = raw_o[0]['ball_rotation'][0]
#             if  raw_o[0]['ball_rotation'][0] > max_ball_rotation_x:
#                 max_ball_rotation_x = raw_o[0]['ball_rotation'][0]
#             if  raw_o[0]['ball_rotation'][1] < min_ball_rotation_y:
#                 min_ball_rotation_y = raw_o[0]['ball_rotation'][1]
#             if  raw_o[0]['ball_rotation'][1] > max_ball_rotation_y:
#                 max_ball_rotation_y = raw_o[0]['ball_rotation'][1]
#             if  raw_o[0]['ball_rotation'][2] < min_ball_rotation_z:
#                 min_ball_rotation_z = raw_o[0]['ball_rotation'][2]
#             if  raw_o[0]['ball_rotation'][2] > max_ball_rotation_z:
#                 max_ball_rotation_z = raw_o[0]['ball_rotation'][2]

# print(min_x, max_x, min_y, max_y)
#     print(min_ball_direction_x, max_ball_direction_x, min_ball_direction_y, max_ball_direction_y, min_ball_direction_z, max_ball_direction_z)
#     print(min_ball_rotation_x, max_ball_rotation_x, min_ball_rotation_y, max_ball_rotation_y, min_ball_rotation_z, max_ball_rotation_z)
