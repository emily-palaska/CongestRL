from math import exp

def linear_reward(congestions: list, delays: list,  congestion_limit: int, alpha=1.0, beta=1.0):
    reward = -alpha * sum(delays) / len(delays) if delays else 0

    for c in congestions:
        if c < 0.6 * congestion_limit:
            reward += beta
        elif c < congestion_limit:
            reward += 4 * beta - 5 * beta / congestion_limit * c
        else:
            reward -= 4 * beta
    return reward

def quadratic_reward(congestions: list, delays: list,  congestion_limit: int, alpha=1.0, beta=1.0):
    reward = -alpha * (sum(delays) / len(delays))**2 if delays else 0

    k = 1e-2/congestion_limit
    l = -(2*beta + 0.64*k * congestion_limit**2) / (0.4 * congestion_limit)
    m = 4*beta + 0.6*k * congestion_limit**2

    for c in congestions:
        if c < 0.6 * congestion_limit:
            reward += beta
        elif c < congestion_limit:
            reward += k * c**2 + l*c + m
        else:
            reward -= 4 * beta
    return reward

def exponential_reward(congestions: list, delays: list,  congestion_limit: int, alpha=1.0, beta=1.0):
    reward = -alpha +  alpha * exp(-sum(delays) / len(delays)) if delays else 0

    for c in congestions:
        if c < 0.6 * congestion_limit:
            reward += beta
        elif c < congestion_limit:
            reward += 4 * beta - 5 * beta / congestion_limit * c
        else:
            reward -= 4 * beta
    return reward