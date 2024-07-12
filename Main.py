import OfflineMania
import gymnasium as gym

if __name__ == "__main__":

    game_file = 'Game/Windows/OfflineMania.exe'  # 'Game/Linux/OfflineMania.x86_64'
    dataset_path = 'OfflineMania/Datasets'
    dataset_name = 'mixLarge'

    env = gym.make('OfflineMania-v0', game_files=game_file, no_graphics=True, time_scale=20)

    offline_dataset = env.unwrapped.get_dataset(dataset_path, dataset_name)

    state, _ = env.reset()

    done = False
    total_reward = 0

    while not done:
        state, reward, truncated, terminated, _ = env.step(env.action_space.sample())
        done = terminated or truncated

        total_reward += reward

    env.close()
    print("Total reward:", total_reward)
