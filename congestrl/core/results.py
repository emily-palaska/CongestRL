import json
import matplotlib.pyplot as plt
import os

class ResultManager:
    def __init__(self, filename='results.json', path=r'D:\emily\CongestRL\results'):
        self.full_path = os.path.join(path, filename)
        self.results = {}
        self.current_episode = None

    def load(self):
        if os.path.exists(self.full_path):
            with open(self.full_path, 'r') as f:
                self.results = json.load(f)
        else:
            raise FileNotFoundError(f"No result file found at: {self.full_path}")

    def save(self):
        with open(self.full_path, 'w') as f:
            json.dump(self.results, f, indent=4)

    def plot(self, plot_path):
        if not self.results:
            print("No results to plot.")
            return

        rewards = [ep.get('reward', 0) for ep in self.results.values()]
        plt.figure(figsize=(10, 5))
        plt.plot(rewards, marker='o')
        plt.title("Episode Rewards")
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.grid(True)
        plt.savefig(plot_path)
        plt.close()

    def append_step(self, info=None, reward=None):
        if self.current_episode is None:
            self.current_episode = {
                'infos': [info],
                'rewards': [reward]
        }
        else:
            self.current_episode['infos'].append(info)
            self.current_episode['rewards'].append(reward)

    def append_episode(self):
        if self.current_episode is None:
            print('No episode to append')
            return

        n = len(self.results)
        self.results[n] = self.current_episode
        self.current_episode = None
