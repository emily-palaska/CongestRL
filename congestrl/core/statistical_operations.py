import random
from typing import Callable, Optional
import numpy as np

def distributed_partition(u : int, r : int, idx: int):
    if idx < 0 or idx >= r: raise ValueError("Index must be between 0 and r-1")
    base, remainder = u // r, u % r
    return base + 1 if idx < remainder else base

def probabilistic_redirect(
        source_id: int,
        num_nodes: int,
        activation_rate: float = 0.1,
        distribution: Callable = np.random.normal,
        distribution_args: tuple = (0, 1),
        allow_self_redirect: bool = False
) -> Optional[int]:
    sample = distribution(*distribution_args)
    if -activation_rate < sample < activation_rate:
        destination = random.randint(0, num_nodes - 1)
        if allow_self_redirect or destination != source_id:
            return destination

    return None