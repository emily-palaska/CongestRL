import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def plot_reward_errorbar(files: list, labels: list):
    assert len(files) == len(labels)
    colors = ('crimson', 'teal', 'mediumblue', 'indigo')
    plt.figure()
    for i, data in enumerate(files):
        episodes, reward_means, reward_stds = [], [], []

        for key in data.keys():
            if key.startswith('episode'):
                episode_num = int(key.split()[1])
                rewards = data[key]['rewards']
                if rewards:  # Only process if there are rewards
                    episodes.append(episode_num)
                    reward_means.append(np.mean(rewards[1:]))
                    reward_stds.append(np.std(rewards[1:]))
        plt.errorbar(episodes, reward_means, yerr=reward_stds, fmt='-o',
                     capsize=5, label=labels[i], color=colors[i])

    plt.xlabel('Episodes')
    plt.title('Reward Error Bar - 8k DQN')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    #plt.savefig('../../results/plots/2_reward_distribution.png')
    plt.show()
    plt.close()


def main():
    filenames = ['../../results/0516_1822_dqn_e10_s200.json',
                 '../../results/0526_1940_dqn_e10_s200.json',
                 '../../results/0518_1908_dqn_e10_s200.json']
    data = [load_json_data(file) for file in filenames]
    labels = ['α = 0.1', 'α = 0.5', 'α = 1.0']

    plot_reward_errorbar(data, labels)
    #plot_congestion_comparison(data, labels, 1)
    #plot_congestion_comparison(data, labels, 5)
    #plot_congestion_comparison(data, labels, 10)
    #plot_delay_heatmap(data)


if __name__ == '__main__':
    main()