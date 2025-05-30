import matplotlib.pyplot as plt
import json

import numpy as np


def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def plot_delay_mean(files: list, labels: list):
    colors = ('crimson', 'teal', 'mediumblue', 'indigo')
    plt.figure(figsize=(8, 6))
    for i, data in enumerate(files):
        means, stds = [], []
        for key, value in data.items():
            if key.startswith('episode'):
                delays = value['delays']
                delays = np.array([list(d.values()) for d in delays])
                means.append(np.mean(delays))
                stds.append(np.std(delays))
        plt.errorbar(list(range(len(means))), means, yerr=stds, fmt='-o',
                     capsize=5, label=labels[i], color=colors[i], alpha=0.9)

    plt.legend()
    plt.xlabel('Episode')
    plt.ylabel('Mean Delay')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('../../results/plots/4_mean_delays.png')
    #plt.show()
    plt.close()

def plot_delay_heatmap(files, labels, episode_num: int):
    assert len(files) == len(labels) == 3
    fig, axs = plt.subplots(1, 3, figsize=(15, 4), sharey=True, constrained_layout=True)

    mappable = None
    for i, data in enumerate(files):
        delays = data[f'episode {episode_num}']['delays']
        delays = [list(d.values()) for d in delays]
        mappable = axs[i].imshow(delays, aspect='auto', cmap='gist_ncar')
        axs[i].set_title(labels[i])

    plt.colorbar(mappable, label='Delay')
    plt.suptitle(f'Episode (episode {episode_num})')
    plt.show()
    plt.close()

def main():
    filenames = ['../../results/0516_1822_dqn_e10_s200.json',
                 '../../results/0526_1940_dqn_e10_s200.json',
                 '../../results/0518_1908_dqn_e10_s200.json']
    files = [load_json_data(file) for file in filenames]
    labels = ['α = 0.1', 'α = 0.5', 'α = 1.0']

    filenames2 = ['../../results/0526_1949_dqn_e10_s200.json',
                  '../../results/0518_1907_dqn_e10_s200.json',
                  '../../results/0518_1909_dqn_e10_s200.json']
    files2 = [load_json_data(file) for file in filenames2]
    labels2 = ['10k DQN (exp)', '8k DQN (exp)', '6k DQN (exp)']

    filenames4 = [
        '../../results/0517_1836_ppo_e10_s200.json',
        '../../results/0517_1724_ppo_e10_s200.json',
        '../../results/0529_1933_ppo_e10_s200.json',
    ]
    files4 = [load_json_data(file) for file in filenames4]
    labels4 = ['10k PPO', '8k PPO', '6k PPO']

    plot_delay_mean(files4, labels4)

if __name__ == '__main__':
    main()
