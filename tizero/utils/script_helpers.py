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


"""Set of functions used by command line scripts."""

from __future__ import absolute_import, division, print_function

import copy
import os
import shutil
import tempfile
import time
from pathlib import Path

import six.moves.cPickle
from gfootball.env import football_action_set, observation_processor
from tqdm import tqdm

from tizero.football_env.core import config, football_env


class ScriptHelpers(object):
    """Set of methods used by command line scripts."""

    def __init__(self):
        pass

    def __modify_trace(self, replay, fps):
        """Adopt replay to the new framerate and add additional steps at the end."""
        trace = []
        min_fps = replay[0]["debug"]["config"]["physics_steps_per_frame"]
        assert (
            fps % min_fps == 0
        ), "Trace has to be rendered in framerate being multiple of {}".format(min_fps)
        assert fps <= 100, "Framerate of up to 100 is supported"
        empty_steps = int(fps / min_fps) - 1
        for f in replay:
            trace.append(f)
            idle_step = copy.deepcopy(f)
            idle_step["debug"]["action"] = [football_action_set.action_idle] * len(
                f["debug"]["action"]
            )
            for _ in range(empty_steps):
                trace.append(idle_step)
        # Add some empty steps at the end, so that we can record videos.
        for _ in range(10):
            trace.append(idle_step)
        return trace

    def __build_players(self, dump_file, spec):
        players = []
        for player in spec:
            players.extend(
                ["replay:path={},left_players=1".format(dump_file)]
                * config.count_left_players(player)
            )
            players.extend(
                ["replay:path={},right_players=1".format(dump_file)]
                * config.count_right_players(player)
            )
        return players

    def load_dump(self, dump_file):
        dump = []
        with open(dump_file, "rb") as in_fd:
            while True:
                try:
                    step = six.moves.cPickle.load(in_fd)
                except EOFError:
                    return dump
                dump.append(step)

    def dump_to_txt(self, dump_file, output, include_debug):
        with open(output, "w") as out_fd:
            dump = self.load_dump(dump_file)
        if not include_debug:
            for s in dump:
                if "debug" in s:
                    del s["debug"]
        with open(output, "w") as f:
            f.write(str(dump))

    def dump_to_video(self, dump_file, directory=None, episode_length=None):
        dump_path = Path(dump_file)
        file_name = dump_path.stem
        print(file_name)

        save_dir = Path(directory)
        if not save_dir.exists():
            save_dir.mkdir()

        if directory:
            tmp_dir = tempfile.mkdtemp(dir=directory)
        else:
            tmp_dir = tempfile.mkdtemp()

        dump = self.load_dump(dump_file)
        cfg = config.Config(dump[0]["debug"]["config"])
        cfg["dump_full_episodes"] = True
        cfg["write_video"] = True
        cfg["display_game_stats"] = True
        # if directory:
        cfg["tracesdir"] = tmp_dir
        processor = observation_processor.ObservationProcessor(cfg)
        processor.write_dump("episode_done")
        if episode_length is None:
            for frame in tqdm(dump):
                processor.update(frame)
        else:
            episode_length = min(episode_length, len(dump))
            for step in tqdm(range(episode_length)):
                processor.update(dump[step])

        del processor
        processor = None

        avi_files = []
        try_time = 0
        while len(avi_files) == 0:
            if try_time > 10:
                print("can not find .avi file in {}".format(tmp_dir))
                break
            avi_files = list(Path(tmp_dir).glob("**/*.avi"))
            try_time += 1
            time.sleep(0.5)
        avi_file = avi_files[0]
        # print('source avi file:',avi_file)
        save_avi_path = save_dir / "{}.avi".format(file_name)
        print("save video to {}".format(save_avi_path.resolve()))

        try_time = 0
        while try_time < 10:
            try:
                try_time += 1
                shutil.copy(avi_file, save_avi_path)
            except:
                time.sleep(0.2)

        shutil.rmtree(tmp_dir)

    def replay(
        self,
        dump,
        fps=10,
        config_update={},
        directory=None,
        render=True,
        episode_length=None,
        render_type="3d",
    ):
        replay = self.load_dump(dump)
        trace = self.__modify_trace(replay, fps)
        fd, temp_path = tempfile.mkstemp(suffix=".dump")
        with open(temp_path, "wb") as f:
            for step in trace:
                six.moves.cPickle.dump(step, f)
        assert (
            replay[0]["debug"]["frame_cnt"] == 0
        ), "Trace does not start from the beginning of the episode, can not replay"

        cfg = config.Config(replay[0]["debug"]["config"])

        # print("game_engine_random_seed",cfg['game_engine_random_seed'])

        cfg["players"] = self.__build_players(temp_path, cfg["players"])
        config_update["physics_steps_per_frame"] = int(100 / fps)
        config_update["real_time"] = False
        if directory:
            config_update["tracesdir"] = directory
        config_update["write_video"] = True
        # my edition
        # config_update['display_game_stats'] = False
        # config_update['video_quality_level'] = 2
        cfg.update(config_update)
        env = football_env.FootballEnv(cfg)
        if render and render_type == "3d":
            env.render()
        env.reset()
        done = False
        try:
            step = 0
            if episode_length is None:
                while not done:
                    _, _, done, _ = env.step([])
                    step += 1
            else:
                for _ in tqdm(range(episode_length)):
                    _, _, done, _ = env.step([])

        except KeyboardInterrupt:
            env.write_dump("shutdown")
            exit(1)
        os.close(fd)
