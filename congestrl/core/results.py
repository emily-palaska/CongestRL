import json, os
import numpy as np

class ResultManager:
    def __init__(self, filename='results.json', metadata=None, autosave=True,
                 path=r'D:\Σχολή\8ο εξάμηνο\Υπολογιστική Νοημοσύνη - Βαθιά Ενισχυτική Μάθηση\2025\CongestRL\results'):
        self.filename = filename
        self.full_path = os.path.join(path, filename)
        self.autosave = autosave
        self.results = {} if metadata is None else {'metadata': metadata}
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
        last_action, congestions, delays, send_rates = info['last_action'], info['congestions'], info['delays'], info['send_rates']
        if isinstance(last_action, np.ndarray): last_action = last_action.tolist()

        if self.current_episode is None:
            self.current_episode = {
                'last_actions': [last_action],
                'congestions': [congestions],
                'delays': [delays],
                'rewards': [reward],
                'send_rates': [send_rates]
        }
        else:
            self.current_episode['last_actions'].append(last_action)
            self.current_episode['congestions'].append(congestions)
            self.current_episode['delays'].append(delays)
            self.current_episode['rewards'].append(reward)
            self.current_episode['send_rates'].append(send_rates)

    def append_episode(self):
        if self.current_episode is None:
            print('No episode to append')
            return

        n = len(self.results)
        self.results[f'episode {n}'] = self.current_episode
        if self.autosave: self.save()
        self.current_episode = None

    def get_data(self, key='congestion'):
        assert key in self.results.keys(), f'Key {key} not found in {self.filename} json file'
        [ep.get(key, 0) for ep in self.results.values()]
