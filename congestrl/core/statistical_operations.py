import random
from typing import Callable, Optional
import numpy as np

def random_balanced_partition(u : int, r : int):
    """Randomly partitions users into balanced groups (with at most ±1 size difference)."""
    user_ids = list(range(u))
    random.shuffle(user_ids)

    base_size, remainder = divmod(u, r)
    sublist_sizes = [base_size + 1] * remainder + [base_size] * (r - remainder)

    return {
        r_id: sorted(
            user_ids[sum(sublist_sizes[:r_id]):sum(sublist_sizes[:r_id + 1])]
        ) for r_id in range(r)
    }

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