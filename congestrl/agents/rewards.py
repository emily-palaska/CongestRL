

def linear_reward(congestion, congestion_limit, delay, alpha, beta):
    reward = -alpha * delay
    if congestion < 0.6 * congestion_limit:
        reward += beta
    elif congestion < congestion_limit:
        reward += 4 * beta - 5 * beta / congestion_limit * congestion
    else:
        reward -= 4 * beta
    return reward