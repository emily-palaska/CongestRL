import numpy as np
import gym
from gym import spaces
from congestrl.simulation.network import CongestNetwork
from congestrl.policy.rewards import linear_reward

class CongestionControlEnv(gym.Env):
    def __init__(self, num_routers=10, num_users=50, connection_density=0.1, congestion_limit=10000,
                 step_time=5, alpha=0.1, beta=1.0, reward_func=linear_reward):
        super(CongestionControlEnv, self).__init__()
        self.num_routers, self.num_users = num_routers, num_users
        self.congestion_limit = congestion_limit
        self.step_time, self.alpha, self.beta = step_time, alpha, beta
        self.reward_func = reward_func
        self.network = CongestNetwork(num_users=num_users, num_routers=num_routers, connection_density=connection_density)

        # Action: each router decides to {0: decrease, 1: maintain, 2: increase} traffic
        self.action_space = spaces.MultiDiscrete([3] * self.num_routers)

        # Observations: global congestion, last action taken by each router, and average delay
        low_obs = np.array([0.0] + [0] * self.num_routers + [0.0])
        high_obs = np.array([np.inf] + [2] * self.num_routers + [np.inf])
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)

        self.last_actions = [1] * self.num_routers  # Start with 'maintain'
        self.current_step = 0

    def reset(self, seed=None, options=None):
        self.network.reset()
        self.last_actions = [1] * self.num_routers
        self.current_step = 0
        info =  {'congestion': 0, 'delay': 0.0}
        return self._get_obs(info), info

    def stop(self, verbose=True):
        self.network.stop(verbose=verbose)

    def _get_obs(self, info):
        congestion, delay = info['congestion'], info['delay']
        return np.concatenate(([congestion], self.last_actions, [delay]), dtype=np.float32)

    def step(self, actions):
        assert len(actions) == self.num_routers, f"Given {len(actions)} actions but expected {self.num_routers}"
        self.last_actions = actions

        for router, action in zip(self.network.routers, actions):
            if action == 0:
                router.send_rate = max(0, router.send_rate - 10)
            elif action == 2:
                router.local_users = min(router.max_send_rate, router.send_rate + 10)

        self.network.start(run_time=self.step_time)

        info = self.network.get_info()
        obs = self._get_obs(info)
        reward = self.reward_func(congestion=info['congestion'], delay=info['delay'],
                                  congestion_limit=self.congestion_limit, alpha=self.alpha, beta=self.beta)
        self.current_step += 1
        return obs, reward, info