from congestrl.environment.network import NetworkTopologyEnv

def main():
    env = NetworkTopologyEnv(num_users=50, num_routers=10, connection_density=0.1)
    observation, info = env.reset()

    for _ in range(1000):
        action = env.action_space.sample()  # Replace with your agent's action
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            observation, info = env.reset()

    env.close()

if __name__ == '__main__':
    main()