from congestrl.policy.dqn_agent import DQNAgent
from congestrl.simulation.environment import CongestControlEnv
from congestrl.core.results import ResultManager
from datetime import datetime

episodes, steps = 10, 200
r, u = 10, 50
step_time = 5
congestion_limit = 8000
batch = 8

env = CongestControlEnv(r, u, limit=congestion_limit, step_time=step_time)
state_size = env.observation_space.shape[0]
agent = DQNAgent(state_size, env.action_space, batch_size=batch)

timestamp = datetime.now().strftime("%m%d_%H%M")
filename = f'{timestamp}_dqn_e{episodes}_s{steps}.json'
manager = ResultManager(path='../../results/' ,filename=filename, metadata={**agent.metadata, **env.metadata})

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
