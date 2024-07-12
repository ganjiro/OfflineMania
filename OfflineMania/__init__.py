import gymnasium as gym
from OfflineMania.offlineManiaWrapper import UnityEnv

gym.envs.registration.register(
    id='OfflineMania-v0',
    entry_point=UnityEnv,
)
