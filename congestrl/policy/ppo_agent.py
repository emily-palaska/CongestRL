import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal

class Actor(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=128):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )
        self.mean_head = nn.Linear(hidden_size, action_size)
        self.log_std = nn.Parameter(torch.zeros(action_size))

    def forward(self, x):
        x = self.fc(x)
        mean = self.mean_head(x)
        std = self.log_std.exp().expand_as(mean)
        return Normal(mean, std)

class Critic(nn.Module):
    def __init__(self, state_size, hidden_size=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)

class PPOAgent:
    def __init__(self, state_size, action_space, clip_epsilon=0.2, lr=3e-4, gamma=0.99, batch_size=64, update_steps=10):
        self.metadata = {
            'state_size': state_size,
            'action_size': action_space.shape[0],
            'clip_epsilon': clip_epsilon,
            'lr': lr,
            'gamma': gamma,
            'update_steps': update_steps,
            'batch_size': batch_size,
        }

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.action_low = torch.tensor(action_space.low, dtype=torch.float32).to(self.device)
        self.action_high = torch.tensor(action_space.high, dtype=torch.float32).to(self.device)
        self.actor = Actor(state_size, self.metadata['action_size']).to(self.device)
        self.critic = Critic(state_size).to(self.device)
        self.optimizer = optim.Adam(list(self.actor.parameters()) + list(self.critic.parameters()), lr=lr)
        self.trajectory = []

    def get_action(self, state):
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        dist = self.actor(state_tensor)
        action = dist.sample()
        action_clipped = torch.clamp(action, self.action_low, self.action_high)
        log_prob = dist.log_prob(action).sum(dim=-1)
        return action_clipped.squeeze(0).cpu().numpy(), log_prob.item()

    def remember(self, state, action, reward, next_state, log_prob):
        self.trajectory.append((state, action, reward, next_state, log_prob))

    def compute_returns(self, rewards, next_states):
        returns = []
        G = 0
        with torch.no_grad():
            for r, ns in zip(reversed(rewards), reversed(next_states)):
                v_next = self.critic(torch.FloatTensor(ns).to(self.device)).item()
                G = r + self.metadata['gamma'] * G
                returns.insert(0, G)
        return torch.FloatTensor(returns).to(self.device)

    def update(self):
        states, actions, rewards, next_states, old_log_probs = zip(*self.trajectory)
        self.trajectory.clear()

        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.FloatTensor(np.array(actions)).to(self.device)
        old_log_probs = torch.FloatTensor(old_log_probs).to(self.device)
        returns = self.compute_returns(rewards, next_states)
        cl_eps = self.metadata['clip_epsilon']

        for _ in range(self.metadata['update_steps']):
            values = self.critic(states)
            advantages = returns - values.detach()

            dist = self.actor(states)
            log_probs = dist.log_prob(actions).sum(dim=-1)
            ratios = torch.exp(log_probs - old_log_probs)

            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - cl_eps, 1 + cl_eps) * advantages

            actor_loss = -torch.min(surr1, surr2).mean()
            critic_loss = nn.MSELoss()(values, returns)
            loss = actor_loss + critic_loss

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
