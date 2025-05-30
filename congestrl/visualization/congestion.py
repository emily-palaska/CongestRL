import matplotlib.pyplot as plt
import numpy as np
import json

def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def plot_congestion_mean(files: list, labels: list):
    plt.figure()

    for i, data in enumerate(files):
        current_means = []
        for key, value in data.items():
            if key.startswith('episode'):
                last_actions = np.array(value['congestions'])
                current_means.append(np.mean(last_actions))
        plt.plot(current_means, label=labels[i])

    plt.legend()
    plt.xlabel('Episode')
    plt.ylabel('Mean Congestions')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    #plt.savefig('../../results/plots/3_mean_last_actions.png')
    plt.close()

def congestion_heatmap(data, label, episode_num: int):
    plt.figure()
    congestions = data[f'episode {episode_num}']['congestions']
    plt.imshow(congestions, aspect='auto')
    plt.colorbar()
    plt.title(label)
    plt.savefig(f'../../results/plots/2_congestion_heatmap_{episode_num}.png')
    plt.close()

def plot_congestion_episodes(files: list, labels: list, episodes: list):
    colors = ('crimson', 'teal', 'mediumblue', 'indigo')
    fig, axs = plt.subplots(1, 3, figsize=(15, 4), sharey=True, constrained_layout=True)

    for i, data in enumerate(files):
        congestions = []
        for j, episode in enumerate(episodes):
            congestions = data[f'episode {episode}']['congestions']
            congestions = [sum(c) / len(c) for c in congestions]
            axs[i].plot(congestions, label=f'Episode {episode}', color=colors[j])
        congestion_limit = data['metadata']['congestion_limit']
        axs[i].plot([congestion_limit]*len(congestions), linestyle='--', label=f'Congestion Limit', color='maroon')
        axs[i].set_xticks([])
        axs[i].legend()
        axs[i].set_title(labels[i])

    plt.savefig('../../results/plots/7_congestion_mean.png')
    #plt.show()

    plt.close()

def main():
    filenames1 = ['../../results/0526_1934_baseline_e10_s200.json',
                 '../../results/0515_1849_dqn_e10_s200.json',
                 '../../results/0517_1836_ppo_e10_s200.json']
    files1 = [load_json_data(file) for file in filenames1]
    labels1 = ['Baseline', 'DQN', 'PPO']

    filenames2 = ['../../results/0526_1949_dqn_e10_s200.json',
                 '../../results/0518_1907_dqn_e10_s200.json',
                 '../../results/0518_1909_dqn_e10_s200.json']
    files2 = [load_json_data(file) for file in filenames2]
    labels2 = ['10k DQN (exp)', '8k DQN (exp)', '6k DQN (exp)']

    filenames3 = ['../../results/0516_1822_dqn_e10_s200.json',
                 '../../results/0526_1940_dqn_e10_s200.json',
                 '../../results/0518_1908_dqn_e10_s200.json']
    files3 = [load_json_data(file) for file in filenames3]
    labels3 = ['α = 0.1', 'α = 0.5', 'α = 1.0']

    plot_congestion_episodes(files3, labels3, [1, 5, 10])

if __name__ == '__main__':
    main()