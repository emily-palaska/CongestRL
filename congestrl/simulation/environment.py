import numpy as np
import gym
from gym import spaces
from congestrl.simulation.network import CongestNetwork
from congestrl.policy.rewards import linear_reward

class CongestControlEnv(gym.Env):
    def __init__(self, r=10, u=50, dens=0.1, limit=10000, step_time=5, alpha=0.1, beta=1.0, reward=linear_reward):
        super(CongestControlEnv, self).__init__()
        # Metadata
        self.num_routers, self.num_users = r, u
        self.connection_density, self.congestion_limit = dens, limit
        self.step_time, self.alpha, self.beta = step_time, alpha, beta
        self.reward_func = reward

        # Initialization
        self.network = CongestNetwork(num_users=u, num_routers=r,
                                      connection_density=dens)
        self._initialize_metadata()
        self._initialize_spaces()

        # Placeholders
        self.last_action = [0] * self.num_routers
        self.congestions = [0] * 25
        self.delays = {router_id: 0 for router_id in range(self.num_routers)}

    def _initialize_metadata(self):
        self.metadata = {
            'num_routers': self.num_routers,
            'num_users': self.num_users,
            'step_time': self.step_time,
            'alpha': self.alpha,
            'beta': self.beta,
            'reward_func': self.reward_func.__name__,
            'congestion_limit': self.congestion_limit,
            'connection_density': self.connection_density
        }

    def _initialize_spaces(self):
        # Action: increase/decrease of send rate for each router
        low_obs = np.array([-1000] * self.num_routers)
        high_obs = np.array([1000] * self.num_routers)
        self.action_space = gym.spaces.Box(low=low_obs, high=high_obs, dtype=np.int16)

        # Observations: congestion samples and average delay per router
        low_obs = np.array([0.0] * (25 + self.num_routers))
        high_obs = np.array([np.inf] * (25 + self.num_routers))
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)


    def reset(self, seed=None, options=None):
        self.network.reset()
        self.last_action = [0] * self.num_routers
        self.congestions = [0] * 25
        self.delays = {router_id: 0 for router_id in range(self.num_routers)}
        return self._get_obs(), self._get_info()

    def stop(self,):
        self.network.stop()

    def _get_obs(self,):
        delays_list = [v for _,v in self.delays.items()]
        return np.concatenate((self.congestions, delays_list), dtype=np.float32)

    def _get_info(self):
        return {
            'last_action': self.last_action,
            'congestions': self.congestions,
            'delays': self.delays,
            'send_rates': self.network.get_send_rates()
        }

    def step(self, action):
        self.last_action = action

        for router, offset in zip(self.network.routers, action):
            new_send_rate = max(0, min(router.max_send_rate, router.send_rate + offset))
            router.send_rate = int(new_send_rate)

        self.network.start(run_time=self.step_time)

        self.congestions, self.delays = self.network.get_congestions(), self.network.get_delays()
        reward = self.reward_func(congestions=self.congestions, delays=self.delays,
                                  congestion_limit=self.congestion_limit, alpha=self.alpha, beta=self.beta)
        return self._get_obs(), reward, self._get_info()