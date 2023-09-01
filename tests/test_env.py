import numpy as np


def raw_env():
    from tizero.football_env.football_jidi_eval import FootballJiDiEnv

    env = FootballJiDiEnv("11_vs_11_jidi_eval")
    env.reset()

    single_action = np.zeros(20)
    single_action[-1] = 1
    action = [single_action] * 22
    raw_o, reward, dones, infos = env.step(action)


def pettingzoo_env():
    from tizero.football_env.football_pettingzoo import FootballAECEnv

    env = FootballAECEnv(id="11_vs_11_jidi_eval")
    env.reset()
    step = 0
    for player_name in env.agent_iter():
        # if step > 20:
        #     break
        observation, reward, termination, truncation, info = env.last()
        if termination or truncation:
            break
        action = env.sample_action(player_name)

        env.step(action)
        step += 1

    print("Total steps: {}".format(step))


if __name__ == "__main__":
    pettingzoo_env()
