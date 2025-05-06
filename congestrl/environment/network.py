import gymnasium as gym
from gymnasium import spaces
import numpy as np
from congestrl.environment.routing import Router
import time
from colorama import Fore
from congestrl.core import ensure_connectivity, create_random_graph

class NetworkTopologyEnv(gym.Env):
    """Custom Network Topology Environment that follows gym interface."""

    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 4}

    def __init__(self, num_users=10, num_routers=10, connection_density=0.5, render_mode=None):
        super(NetworkTopologyEnv, self).__init__()

        # Arguments
        self.num_users = num_users
        self.num_routers = num_routers
        self.connection_density = connection_density
        self.render_mode = render_mode

        # Define action and observation spaces
        # Example: Action could be adjusting weights on edges
        self.action_space = spaces.Box(
            low=0.1, high=10.0, shape=(num_routers, num_routers), dtype=np.float32
        )

        # Observation could be current weights and congestion times
        self.observation_space = spaces.Dict({
            "weights": spaces.Box(low=0.1, high=10.0, shape=(num_routers, num_routers), dtype=np.float32),
            "congestion": spaces.Box(low=0, high=100, shape=(num_routers,), dtype=np.float32),
            "packets": spaces.Box(low=0, high=np.inf, shape=(num_routers, 2), dtype=np.float32)  # [created, received]
        })

        # Placeholders
        self.routers = []
        self.weights_runtime = []
        self.current_step = 0
        self.max_steps = 100  # or whatever makes sense for your simulation

        # Initialize network
        self._initialize_network()

    def _initialize_network(self):
        self.graph = ensure_connectivity(
            create_random_graph(num_nodes=self.num_routers,
                                connection_density=self.connection_density)
        )
        self._initialize_routers()

    def _initialize_routers(self):
        self.routers = [Router(router_id=router_id,
                               num_routers=self.num_routers,
                               num_users=self.num_users,
                               graph=self.graph)
                        for router_id in range(self.num_routers)]
        self._update_neighbor_routers()

    def _update_neighbor_routers(self):
        for i in range(self.num_routers):
            neighbor_routers = {
                self.routers[n].router_id: self.routers[n]
                for n in self.graph.neighbors(i)
            }
            self.routers[i].neighbor_routers = neighbor_routers

    def step(self, action):
        """
        Run one timestep of the environment's dynamics.

        Args:
            action: The action to take (adjusting weights in this case)

        Returns:
            observation, reward, terminated, truncated, info
        """
        # Apply the action (e.g., adjust weights)
        self._apply_action(action)

        # Let the simulation run for a bit
        time.sleep(0.1)  # Adjust as needed

        # Get the current state
        observation = self._get_obs()

        # Calculate reward
        reward = self._calculate_reward()

        # Check if episode is done
        self.current_step += 1
        terminated = self.current_step >= self.max_steps
        truncated = False  # You can implement early termination if needed

        # Additional info
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, truncated, info

    def _apply_action(self, action):
        """Apply the agent's action to the environment."""
        # Example: Update edge weights based on action
        for i in range(self.num_routers):
            for j in range(self.num_routers):
                if self.graph.has_edge(i, j):
                    self.graph[i][j]['weight'] = action[i, j]

    def _get_obs(self):
        """Get current observation."""
        # Create weight matrix
        weight_matrix = np.zeros((self.num_routers, self.num_routers))
        for i, j in self.graph.edges():
            weight_matrix[i, j] = self.graph[i][j]['weight']
            weight_matrix[j, i] = self.graph[i][j]['weight']  # if undirected

        # Get congestion and packet stats
        congestion = np.array([router.congestion_times[-1] if router.congestion_times else 0
                               for router in self.routers])
        packets = np.array([[router.packets_created, router.packets_received]
                            for router in self.routers])

        return {
            "weights": weight_matrix,
            "congestion": congestion,
            "packets": packets
        }

    def _calculate_reward(self):
        """Calculate reward based on current state."""
        # Example: Reward for minimizing total weight and congestion
        total_weight = sum(data['weight'] for _, _, data in self.graph.edges(data=True))
        total_congestion = sum(router.congestion_times[-1] if router.congestion_times else 0
                               for router in self.routers)

        # You'll need to design a proper reward function for your specific goals
        reward = - (0.7 * total_weight + 0.3 * total_congestion)
        return reward

    def _get_info(self):
        """Get additional info for debugging."""
        return {
            "total_weight": sum(data['weight'] for _, _, data in self.graph.edges(data=True)),
            "total_congestion": sum(router.congestion_times[-1] if router.congestion_times else 0
                                    for router in self.routers),
            "step": self.current_step
        }

    def reset(self, seed=None, options=None):
        """Reset the environment to initial state."""
        super().reset(seed=seed)

        # Stop any running threads
        for router in self.routers:
            if hasattr(router, 'stop'):
                router.stop()

        # Reinitialize
        self._initialize_network()
        self.current_step = 0
        self.weights_runtime = []

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def render(self):
        """Render the environment."""
        if self.render_mode == "human":
            total_weight = sum(data['weight'] for _, _, data in self.graph.edges(data=True))
            print(Fore.CYAN + f"Step {self.current_step}: Total Graph weight: {total_weight}")

    def close(self):
        """Clean up resources."""
        for router in self.routers:
            router.stop()