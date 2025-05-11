import numpy as np
from gym import spaces
def _get_obs(last_actions, info):
    congestion, delay = info['congestion'], info['delay']
    return np.concatenate(([congestion], last_actions, [delay]), dtype=np.float32)



action_space = spaces.MultiDiscrete([3] * 3)
info = {'congestion': 3, 'delay': 1}

print(_get_obs(action_space.sample(), info))