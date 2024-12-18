import os
import sys

sys.path.append(os.getcwd())
import gymnasium as gym

from cyberattacksim.utils.env_utils import create_env

gym.logger.set_level(40)


def make_env(env_id):
    # return NormalizedEnv(create_env(env_id))
    return create_env(env_id=env_id)


class NormalizedEnv(gym.Wrapper):

    def __init__(self, env):
        gym.Wrapper.__init__(self, env)
        self._max_episode_steps = 100

        self.scale = env.action_space.shape
        self.action_space.high /= self.scale
        self.action_space.low /= self.scale

    def step(self, action):
        return self.env.step(action * self.scale)
