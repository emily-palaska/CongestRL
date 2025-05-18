def linear_reward(congestions: list, delays: list,  congestion_limit: int, alpha=1.0, beta=1.0):
    reward = -alpha * sum(delays) / len(delays)

    for c in congestions:
        if c < 0.6 * congestion_limit:
            reward += beta
        elif c < congestion_limit:
            reward += 4 * beta - 5 * beta / congestion_limit * c
        else:
            reward -= 4 * beta
    return reward