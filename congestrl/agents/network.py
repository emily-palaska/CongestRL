import numpy as np
import gym
from gym import spaces
from topology import NetworkTopology

class CongestionControlEnv(gym.Env):
    def __init__(self, num_routers=10, num_users=50, connection_density=0.1, congestion_limit=200):
        super(CongestionControlEnv, self).__init__()
        self.num_routers = num_routers
        self.num_users = num_users
        self.congestion_limit = congestion_limit

        # Initialize network
        self.network = NetworkTopology(num_users=num_users, num_routers=num_routers, connection_density=connection_density)

        # Action: each router decides to {0: decrease, 1: maintain, 2: increase} traffic
        self.action_space = spaces.MultiDiscrete([3] * self.num_routers)

        # Observation: global congestion, last action taken by each router, and total packets sent
        low_obs = np.array([0.0] + [0] * self.num_routers + [0])
        high_obs = np.array([np.inf] + [2] * self.num_routers + [np.inf])
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)

        self.last_actions = [1] * self.num_routers  # Start with 'maintain'
        self.total_packets = 0
        self.current_step = 0

    def reset(self):
        self.network.reset()
        self.last_actions = [1] * self.num_routers
        self.total_packets = 0
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        total_weight = sum(data['weight'] for _, _, data in self.network.graph.edges(data=True))
        return np.array([total_weight] + self.last_actions + [self.total_packets], dtype=np.float32)

    def step(self, actions):
        assert len(actions) == self.num_routers
        self.last_actions = actions

        # Modify router behavior here (you can scale packet creation, e.g., via a parameter in Router)
        for router, action in zip(self.network.routers, actions):
            # simulate effect of action (basic example: scale user count)
            if action == 0:
                router.local_users = max(1, int(router.local_users * 0.8))
            elif action == 2:
                router.local_users = int(router.local_users * 1.2)

        self.network.start(run_time=1)  # simulate 1 second
        self.network.stop()

        total_weight = sum(data['weight'] for _, _, data in self.network.graph.edges(data=True))
        delay = sum(len(router.delay_times) for router in self.network.routers)
        self.total_packets += sum(router.packets_created for router in self.network.routers)

        reward = -1.0 * delay
        if total_weight > self.congestion_limit:
            reward -= 50  # heavy penalty for violating congestion

        self.current_step += 1
        done = self.current_step >= 100  # Or some other condition
        obs = self._get_obs()
        info = {'total_weight': total_weight, 'delay': delay}

        return obs, reward, done, info
