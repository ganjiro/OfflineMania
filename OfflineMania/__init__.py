import gymnasium as gym
from OfflineMania.OfflineManiaWrapper import UnityEnv

gym.envs.registration.register(
    id='OfflineMania-v0',
    entry_point=UnityEnv,
)
