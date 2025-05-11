import numpy as np
from congestrl.environment.environment import CongestionControlEnv
from congestrl.policy.utils import random_policy
from congestrl.core.results import ResultManager

def run_simulation(env, policy=random_policy, episodes=10, steps=10, verbose=True):
    manager = ResultManager()

    for e in range(episodes):
        if verbose: print('Resetting environment', end='')
        obs, info = env.reset()
        manager.append_step(info=info)

        for step in range(steps):
            action = policy(env.action_space)
            obs, reward, info = env.step(action)

            if verbose: print(f"\rStep {step + 1}", end='')
            manager.append_step(reward=reward, info=info)

        manager.append_episode()
        if verbose: print(f'\rEpisode {e} completed')

    manager.save()
    if verbose: print(f'Results saved in {manager.full_path}')
    env.stop()

if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    net_env = CongestionControlEnv()
    run_simulation(net_env)