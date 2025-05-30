import numpy as np
import matplotlib.pyplot as plt

from congestrl.policy.rewards import linear_reward, quadratic_reward, exponential_reward

def plot_parametric_sweep(reward_function=exponential_reward, congestion_limit=1000, alpha=1.0, beta=1.0):
    delays = np.linspace(0, 10, 200)
    rewards_per_delay = [
        reward_function([], [d], congestion_limit=congestion_limit, alpha=alpha, beta=beta)
            for d in delays
    ]
    congestions = np.linspace(0, 1.5 * congestion_limit, 2 * congestion_limit)
    rewards_per_congestion = [
        reward_function([c], [], congestion_limit=congestion_limit, alpha=alpha, beta=beta)
            for c in congestions
    ]

    fig, axs = plt.subplots(1, 2)
    axs[0].plot(delays, rewards_per_delay, color='slateblue')
    axs[0].set_title(f'Delay Sweep')
    axs[0].set_xlabel('Delay')
    axs[0].set_ylabel('Reward')

    axs[1].plot(congestions, rewards_per_congestion, color='orchid')
    axs[1].set_title(f'Congestion Sweep')
    axs[1].set_xlabel('Congestion')
    axs[1].set_ylabel('Reward')

    fig.suptitle(f'{reward_function.__name__}\nα = {alpha}, β = {beta}, congestion limit: {congestion_limit}', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'../../results/plots/{reward_function.__name__}.png')
    plt.close()

if __name__ == '__main__':
    plot_parametric_sweep()