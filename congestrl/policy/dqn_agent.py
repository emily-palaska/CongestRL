import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from congestrl.policy.agents import random_policy

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=128):
        super(QNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size)
        )

    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self, state_size, action_space, batch_size=64,
                 lr=1e-3, gamma=0.99, epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.995):
        self.metadata = {
            'state_size': state_size,
            'action_size': action_space.shape[0],
            'epsilon_start': epsilon,
            'epsilon_min': epsilon_min,
            'epsilon_decay': epsilon_decay,
            'gamma': gamma,
            'lr': lr,
            'batch_size': batch_size
        }

        self.action_space = action_space
        self.epsilon = epsilon
        self.memory = deque(maxlen=10000)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.q_network = QNetwork(state_size, action_space.shape[0]).to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return random_policy(self.action_space)
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.q_network(state_tensor)
        return q_values.squeeze(0).cpu().tolist()

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def replay(self):
        if len(self.memory) < self.metadata['batch_size']:
            return

        batch = random.sample(self.memory, self.metadata['batch_size'])
        states, actions, rewards, next_states = zip(*batch)

        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.FloatTensor(np.array(actions)).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)

        current_q_values = self.q_network(states)  # Shape: [batch_size, action_size]

        # Since actions are continuous, we need to compute the Q-value for the taken action
        # We'll use the dot product between the Q-values and the action vector
        current_q = (current_q_values * actions).sum(dim=1)  # Shape: [batch_size]

        # Get Q values for next states
        with torch.no_grad():
            next_q_values = self.q_network(next_states)  # Shape: [batch_size, action_size]
            # For DQN, we take the max over possible actions
            next_q = next_q_values.max(dim=1)[0]  # Shape: [batch_size]
        target_q = rewards + self.metadata['gamma'] * next_q

        self.optimizer.zero_grad()
        loss = self.loss_fn(current_q, target_q)
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(
            self.metadata['epsilon_min'],
            self.epsilon * self.metadata['epsilon_decay']
        )

