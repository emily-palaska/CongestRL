from congestrl.policy.dqn_agent import DQNAgent
from congestrl.simulation.environment import CongestionControlEnv
from congestrl.core.results import ResultManager
from datetime import datetime

def run_dqn(env, episodes=10, steps=200):
    state_size = env.observation_space.shape[0]
    agent = DQNAgent(state_size, env.action_space, batch_size=8)
    print(f'Initialized DQNAgent with state size {agent.metadata['state_size']} and action size {agent.metadata['action_size']}')

    timestamp = datetime.now().strftime("%m%d_%H%M")
    filename = f'{timestamp}_dqn_e{episodes}_s{steps}.json'
    manager = ResultManager(filename=filename, metadata=agent.metadata | env.metadata)

    for e in range(episodes):
        state, info = env.reset()
        manager.append_step(info=info)
        for step in range(steps):
            print(f"\rStep {step + 1}", end='')
            action = agent.get_action(state)
            next_state, reward, info = env.step(action)

            agent.remember(state, action, reward, next_state)
            agent.replay()

            manager.append_step(reward=reward, info=info)
            state = next_state

        manager.append_episode()
        print(f"\rEpisode {e+1} complete")

    manager.save()
    print(f'Results saved in {manager.full_path}')
    env.stop()

if __name__ == "__main__":
    demo_env = CongestionControlEnv(num_routers=10, num_users=50, step_time=5, congestion_limit=8000)
    run_dqn(demo_env)
