import matplotlib.pyplot as plt
import numpy as np
import json


def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def plot_mean_last_action(files: list, labels: list):
    plt.figure()
    colors = ['crimson', 'teal', 'mediumblue', 'indigo']
    for i, data in enumerate(files):
        current_means = []
        for key, value in data.items():
            if key.startswith('episode'):
                last_actions = np.array(value['last_actions'])
                current_means.append(np.mean(last_actions))
        plt.plot(current_means, label=labels[i], color=colors[i])

    plt.legend()
    plt.xlabel('Episode')
    #plt.yticks([])
    plt.ylabel('Mean last actions')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('../../results/plots/8_mean_last_actions.png')
    plt.close()


def plot_send_rates(files: list, labels: list, episode_num: int):
    assert len(files) == len(labels) == 4

    fig, axs = plt.subplots(1, 4, figsize=(16, 4), sharey=True, constrained_layout=True)
    mappables = []

    for i, data in enumerate(files):
        send_rates = data[f'episode {episode_num}']['send_rates']
        send_rates = [list(s.values()) for s in send_rates]
        send_rates = [[row[i] for row in send_rates] for i in range(len(send_rates[0]))]
        mappable = axs[i].imshow(send_rates, aspect='auto', cmap='gist_ncar')
        mappables.append(mappable)

        axs[i].set_title(labels[i])
        axs[i].set_xlabel('Step Progression')
        if i == 0:
            axs[i].set_ylabel('Routers')

    plt.suptitle(f'Episode {episode_num}')
    fig.colorbar(mappables[2], ax=axs, label='Send Rate', orientation='vertical')

    plt.savefig(f'../../results/plots/3_send_rates_heatmap_{episode_num}.png')
    plt.close()

def main():
    filenames = ['../../results/0515_1849_dqn_e10_s200.json',
                 '../../results/0516_1822_dqn_e10_s200.json',
                 '../../results/0517_1255_dqn_e10_s200.json',
                 '../../results/0526_1934_baseline_e10_s200.json',]
    files = [load_json_data(file) for file in filenames]
    labels = ['10k DQN', '8k DQN', '6k DQN', '10k Baseline']

    filenames2 = ['../../results/0526_1949_dqn_e10_s200.json',
                  '../../results/0518_1907_dqn_e10_s200.json',
                  '../../results/0518_1909_dqn_e10_s200.json',
                  '../../results/0526_1934_baseline_e10_s200.json']
    files2 = [load_json_data(file) for file in filenames2]
    labels2 = ['10k DQN (exp)', '8k DQN (exp)', '6k DQN (exp)', '10k Baseline']

    #plot_mean_last_action(files2, labels2)
    plot_send_rates(files, labels, 1)
    plot_send_rates(files, labels, 9)


if __name__ == '__main__':
    main()