import copy
from typing import Dict, Optional

import numpy as np
from ray.rllib.env.multi_agent_env import MultiAgentEnv

from tizero import football_env


class FootballJiDiEnv(MultiAgentEnv):
    """An example of a wrapper for GFootball to make it compatible with rllib."""

    def __init__(
        self,
        scenario_name: str,
        cfg: Dict = {},
        rank: int = 0,
        log_dir=None,
        isEval=True,
        seed: int = 0,
        write_video=False,
        need_render=False,
    ):
        # football本身运行太慢，在debug的时候，通过fake_step来进行加速，返回虚拟的observation
        # deterministic = True时，设置game_engine_random_seed无效，环境会自动设置game_engine_random_seed=42
        # deterministic = False时，如果没有设置game_engine_random_seed，环境会使用随机seed初始化。
        # 想要我们自己设置seed，需要把deterministic设为False，然后设置一下game_engine_random_seed！
        assert seed is not None, "you must set a seed when setup the environment"
        self.fake_step = False
        if self.fake_step:
            self.fake_raw, self.fake_r, self.fake_d, self.fake_info = (
                None,
                None,
                None,
                None,
            )

        # self.left_agent_num = cfg.left_agent_num if cfg else 11
        self.left_agent_num = cfg.pop("left_agent_num", 11)
        # self.right_agent_num = cfg.right_agent_num if cfg else 11
        self.right_agent_num = cfg.pop("right_agent_num", 11)

        self.max_episode_length = cfg.pop("max_episode_length", 3001)

        self.isEval = isEval
        self.rank = rank

        # create env

        video_quality_level = 0

        if write_video:
            print("evaluation environment will write video!")
            video_quality_level = 0  # 最低画质，全场游戏大概85M
            # video_quality_level = 1 # 中等画质，全场游戏大概330M
            # video_quality_level = 2 # 最高画质，全场游戏大概5G

        representation = "raw"  # simple115, simple115v2,extracted

        self.env = football_env.create_environment(
            env_name=scenario_name,
            stacked=False,
            logdir=log_dir,
            representation=representation,
            rewards="scoring",
            write_goal_dumps=False,
            write_full_episode_dumps=need_render,
            render=write_video,
            write_video=write_video,
            dump_frequency=1 if need_render else 0,
            number_of_left_players_agent_controls=self.left_agent_num,
            number_of_right_players_agent_controls=self.right_agent_num,
            other_config_options={
                "action_set": "v2",
                "video_quality_level": video_quality_level,
                "game_engine_random_seed": seed,
            },
        )

        self.cur_step = 0
        self.total_step = 0

    def reset(self):
        raw_obs = self.env.reset()
        self.cur_step = 0
        return self.add_control_index(raw_obs), [
            {} for i in range(self.left_agent_num + self.right_agent_num)
        ]

    def add_control_index(self, raw_obs):
        for i, o in enumerate(raw_obs):
            if "controlled_player_index" not in o:
                o["controlled_player_index"] = i % 11
        return raw_obs

    def step(self, actions):
        self.cur_step += 1
        self.total_step += 1
        actions = np.array(actions)

        if len(actions.shape) != 1:
            actions = np.argmax(actions, axis=-1)

        if self.fake_step:
            if self.fake_raw is None:
                raw_o, r, d, info = self.env.step(actions.astype("int32"))
                self.fake_raw, self.fake_r, self.fake_d, self.fake_info = (
                    raw_o,
                    r,
                    d,
                    info,
                )
            raw_o, r, d, info = self.fake_raw, self.fake_r, self.fake_d, self.fake_info
        else:
            raw_o, r, d, info = self.env.step(actions.astype("int32"))
        info["enemy_designated"] = raw_o[-1]["designated"]
        dones = []
        infos = []

        for i in range(self.left_agent_num + self.right_agent_num):
            if (
                hasattr(self, "max_episode_length")
                and self.cur_step >= self.max_episode_length
            ):
                dones.append(True)
            else:
                dones.append(d)
            reward = r[i] if self.left_agent_num > 1 else r
            info["goal"] = reward
            infos.append(copy.deepcopy(info))

        return self.add_control_index(raw_o), r, dones, infos

    def seed(self, seed=None):
        if seed is None:
            np.random.seed(1)
        else:
            np.random.seed(seed)

    def close(self):
        self.env.close()
