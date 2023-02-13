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

""""""
import numpy as np

class RandomAgent():
    def __init__(self):
        pass
    def get_action(self,raw_obs):
        return np.eye(19)[np.random.choice(19, 1)].tolist()

agent = RandomAgent()

def my_controller(obs_list, action_space_list, is_act_continuous=False):
    del obs_list['controlled_player_index']
    return agent.get_action(obs_list)

def jidi_controller(obs_list = None):
    if obs_list is None:
        return
    re = my_controller(obs_list,None)
    assert isinstance(re,list)
    assert isinstance(re[0],list)
    return re