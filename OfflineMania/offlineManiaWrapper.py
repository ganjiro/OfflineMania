import os

import h5py
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import ActionTuple
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import numpy as np
import time
import gymnasium as gym
from gymnasium import spaces

dataset_list = ["basic", "basicSmall", "expert", "medium", "mixLarge", "mixSmall"]

class UnityEnv(gym.Env):
    def __init__(self, game_files, no_graphics=True, worker_id=0, seed=int(time.time()), time_scale=100,
                 log_folder=None):

        self.no_graphics = no_graphics

        self.configuration_channel = EngineConfigurationChannel()
        self.unity_env = UnityEnvironment(game_files, no_graphics=no_graphics, seed=seed, worker_id=int(worker_id),
                                          side_channels=[self.configuration_channel],
                                          log_folder=log_folder
                                          )
        self.behavior_name = 'CarDriver?team=0'
        self.unity_env.reset()
        self.configuration_channel.set_configuration_parameters(time_scale=time_scale, quality_level=0)

        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(33,), dtype=np.float32)

        self.current_timestep = 0

        self.ep = 0

    def reset(self, seed=None, options=None):

        self.current_timestep = 0

        decision_steps = None
        self.unity_env.reset()

        while decision_steps is None or len(decision_steps.obs[0]) <= 0:
            self.unity_env.step()
            decision_steps, terminal_steps = self.unity_env.get_steps(self.behavior_name)

        state = np.concatenate(decision_steps.obs, axis=-1)[0]
        self.ep += 1
        return state, {}

    def step(self, actions):

        actions = np.asarray(actions)
        actions = np.reshape(actions, [1, self.action_space.shape[0]])

        actionsAT = ActionTuple()
        actionsAT.add_continuous(actions)

        self.unity_env.set_actions(self.behavior_name, actionsAT)
        self.unity_env.step()
        decision_steps, terminal_steps = self.unity_env.get_steps(self.behavior_name)
        done = False
        if (len(terminal_steps.interrupted) > 0):
            state = np.concatenate(decision_steps.obs, axis=-1)[0]

            reward = terminal_steps.reward[0]
        else:
            state = np.concatenate(decision_steps.obs, axis=-1)[0]

            reward = decision_steps.reward[0]

        self.current_timestep += 1
        if self.current_timestep == 2000:
            done = True

        return state, reward, False, done, {}

    def close(self):
        self.unity_env.close()

    def get_dataset(self, path, name):

        if name not in dataset_list:
            raise NotImplementedError

        if name == 'mixLarge':
            # split because of the Github size limit
            file_1 = os.path.join(path, f'{name}_1.h5')
            file_2 = os.path.join(path, f'{name}_2.h5')

            with h5py.File(file_1, 'r') as file1:
                data_dict_1 = {key: np.array(file1[key]) for key in file1.keys()}

            with h5py.File(file_2, 'r') as file2:
                data_dict_2 = {key: np.array(file2[key]) for key in file2.keys()}

            loaded_data_dict = {key: np.concatenate((data_dict_1[key], data_dict_2[key]), axis=0) for key in
                                data_dict_1.keys()}

        else:
            with h5py.File(f'{os.path.join(path, name)}.h5', 'r') as file:
                loaded_data_dict = {key: np.array(file[key]) for key in file.keys()}

        return loaded_data_dict
