from congestrl.simulation.environment import CongestionControlEnv
from congestrl.policy.agents import random_policy
from congestrl.core.results import ResultManager
from datetime import datetime

def run_simulation(env, policy=random_policy, episodes=10, steps=20):
    timestamp = datetime.now().strftime("%m%d_%H%M")
    filename = f'{timestamp}_baseline_e{episodes}_s{steps}.json'
    manager = ResultManager(filename= filename, metadata = {'policy': policy.__name__, **env.metadata})

    for e in range(episodes):
        print('\rResetting simulation', end='')
        obs, info = env.reset()
        manager.append_step(info=info)

        for step in range(steps):
            action = policy(env.action_space)
            obs, reward, info = env.step(action)

            print(f"\rStep {step + 1}", end='')
            manager.append_step(reward=reward, info=info)

        manager.append_episode()
        print(f'\rEpisode {e} completed')

    manager.save()
    print(f'Results saved in {manager.full_path}')
    env.stop()

if __name__ == "__main__":
    net_env = CongestionControlEnv(num_routers=100, num_users=100,step_time=5)
    run_simulation(net_env)