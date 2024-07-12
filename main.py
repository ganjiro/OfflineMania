import OfflineMania
import gymnasium as gym
import argparse

def main(game_file, dataset_path, dataset_name):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OfflineMania with specified parameters.")
    parser.add_argument('--game_file', type=str, default='Game/Windows/OfflineMania.exe', help='Path to the game file.')
    parser.add_argument('--dataset_path', type=str, default='OfflineMania/Datasets',
                        help='Path to the dataset directory.')
    parser.add_argument('--dataset_name', type=str, default='mixLarge', help='Name of the dataset to load.')

    args = parser.parse_args()

    main(args.game_file, args.dataset_path, args.dataset_name)
