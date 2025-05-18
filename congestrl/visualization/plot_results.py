import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def plot_reward_distribution(data):
    episodes = []
    reward_means = []
    reward_stds = []

    for key in data.keys():
        if key.startswith('episode'):
            episode_num = int(key.split()[1])
            rewards = data[key]['rewards']
            if rewards:  # Only process if there are rewards
                episodes.append(episode_num)
                reward_means.append(np.mean(rewards[1:]))
                reward_stds.append(np.std(rewards[1:]))

    plt.figure(figsize=(12, 8))
    plt.errorbar(episodes, reward_means, yerr=reward_stds, fmt='-o',
                 capsize=5, label='Mean ± Std Dev')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Reward Distribution Across Episodes')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_congestion_over_time(data):
    plt.figure(figsize=(12, 8))

    for key in data.keys():
        if key.startswith('episode'):
            congestions = data[key]['congestions']
            if congestions:  # Only process if there are congestion data
                congestions = [sum(c) / len(c) for c in congestions]
                episode_num = int(key.split()[1])
                plt.plot(congestions, label=f'Episode {episode_num}')

    plt.xlabel('Time Step')
    plt.ylabel('Congestion')
    plt.title('Congestion Over Time for Each Episode')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_delay_heatmap(data):
    # Collect all delays for each router across episodes
    router_delays = defaultdict(list)

    for key in data.keys():
        if key.startswith('episode'):
            delays = data[key]['delays']
            if delays:  # Only process if there are delays
                for time_step in delays:
                    for router, delay in time_step.items():
                        router_delays[int(router)].append(delay)

    # Prepare data for heatmap
    routers = sorted(router_delays.keys())
    delay_matrix = []
    for router in routers:
        delay_matrix.append(router_delays[router])

    plt.figure(figsize=(12, 8))
    plt.imshow(delay_matrix, aspect='auto', cmap='hot_r')
    plt.colorbar(label='Delay')
    plt.xlabel('Time Step')
    plt.ylabel('Router ID')
    plt.title('Delay Heatmap Across All Routers')
    plt.yticks(range(len(routers)), routers)
    plt.tight_layout()
    plt.show()


def main():
    filename = '../../results/0517_0900_baseline_e10_s20.json'
    data = load_json_data(filename)

    plot_reward_distribution(data)
    plot_congestion_over_time(data)
    plot_delay_heatmap(data)


if __name__ == '__main__':
    main()