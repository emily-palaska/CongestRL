import json, os

class ResultManager:
    def __init__(self, filename='results.json', path=r'D:\Σχολή\8ο εξάμηνο\Υπολογιστική Νοημοσύνη - Βαθιά Ενισχυτική Μάθηση\2025\CongestRL\results'):
        self.filename = filename
        self.full_path = os.path.join(path, filename)
        self.results = {}
        self.current_episode = None

    def __len__(self):
        return len(self.results)

    def load(self):
        if os.path.exists(self.full_path):
            with open(self.full_path, 'r') as f:
                self.results = json.load(f)
        else:
            raise FileNotFoundError(f"No result file found at: {self.full_path}")

    def save(self):
        with open(self.full_path, 'w') as f:
            json.dump(self.results, f, indent=4)

    def append_step(self, info=None, reward=None):
        if self.current_episode is None:
            self.current_episode = {
                'congestions': [info['congestion']],
                'delays': [info['delay']],
                'rewards': [reward]
        }
        else:
            self.current_episode['congestions'].append(info['congestion'])
            self.current_episode['delays'].append(info['delay'])
            self.current_episode['rewards'].append(reward)

    def append_episode(self):
        if self.current_episode is None:
            print('No episode to append')
            return

        n = len(self.results)
        self.results[n] = self.current_episode
        self.current_episode = None

    def get_data(self, key='congestion'):
        assert key in self.results.keys(), f'Key {key} not found in {self.filename} json file'
        [ep.get(key, 0) for ep in self.results.values()]
