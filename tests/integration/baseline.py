from congestrl.simulation.environment import CongestionControlEnv
from congestrl.policy.utils import random_policy
from congestrl.core.results import ResultManager
from policy.rewards import linear_reward

def run_simulation(env, policy=random_policy, episodes=1, steps=1, verbose=True):
    filename= 'linear' if env.reward_func == linear_reward else ''
    filename += '_random' if policy == random_policy else ''
    filename += f'_e{episodes}_s{steps}.json'
    manager = ResultManager(filename= filename)

    for e in range(episodes):
        if verbose: print('\rResetting simulation', end='')
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
    net_env = CongestionControlEnv(step_time=5)
    run_simulation(net_env)