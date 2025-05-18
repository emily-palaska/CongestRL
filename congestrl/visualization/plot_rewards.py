import numpy as np
import matplotlib.pyplot as plt

from congestrl.policy.rewards import linear_reward, quadratic_reward, exponential_reward

def plot_parametric_sweep(reward_function=linear_reward, congestion_limit=1000, alpha=1.0, beta=1.0):
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

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].plot(delays, rewards_per_delay, label=f'no congestion data', color='red')
    axs[0].set_title(f'Congestion Limit: {congestion_limit}')
    axs[0].set_xlabel('Delay')
    axs[0].set_ylabel('Reward')
    axs[0].legend(fontsize=8)

    axs[1].plot(congestions, rewards_per_congestion, label=f'no delay data', color='green')
    axs[1].set_title(f'Congestion Limit: {congestion_limit}')
    axs[1].set_xlabel('Congestion')
    axs[1].set_ylabel('Reward')
    axs[1].legend(fontsize=8)

    fig.suptitle(f'Parametric Sweep of {reward_function.__name__} w/ α = {alpha}, β = {beta}', fontsize=16)
    plt.tight_layout()
    plt.show()


plot_parametric_sweep(reward_function=exponential_reward)