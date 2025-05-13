from congestrl.core.graphs import shortest_path_policy
from congestrl.core.statistics import probabilistic_redirect
import random, time
from colorama import Fore
import numpy as np

def create_packets(router_id, local_users, num_routers, graph, send_rate=0.01):
    packets = []
    for user_id in range(local_users):
        source_node = router_id
        if (dest_node := probabilistic_redirect(
            source_id=router_id,
            num_nodes=num_routers,
            activation_rate=send_rate
        )) is None: continue

        if best_path := shortest_path_policy(graph, source_node, dest_node):
            packets.append({
                "source_node": source_node,
                "destination_node": dest_node,
                "path": best_path,
                "weight": random.randint(1, 10),
                "created": time.time()
            })
        else:
            print(Fore.BLUE + f"Router {source_node} no path to Router {dest_node}")
    return packets

def calculate_delay(created, received, active_periods):
    on_air = round(received - created, 2)
    if not active_periods: return on_air

    start_idx, end_idx = None, None
    for i, (start, end) in enumerate(active_periods):
        if start <= created <= end: start_idx = i
        if start <= received <= end: end_idx = i

    if start_idx is None and end_idx is None:
        return on_air # Both timestamps on last active period

    if start_idx is None:
        start_idx = 0 # Fallback in case active_periods overflows

    if end_idx is None: # Received timestamp on last active period
        end_idx = len(active_periods) - 1
    assert end_idx >= start_idx, f"{end_idx} < {start_idx}"

    frozen = 0.0
    if start_idx is not None and end_idx is not None and end_idx > start_idx:
        for i in range(start_idx + 1, end_idx + 1):
            prev_end = active_periods[i - 1][1]
            curr_start = active_periods[i][0]
            frozen += max(0, curr_start - prev_end)
    return round(on_air - frozen, 2)

def demultiplex_packets(router_id, packets, active_periods):
    routed_packets = {router_id: []}
    if not packets: return routed_packets

    for packet in packets:
        if packet["destination_node"] == router_id:
            created, received = packet['created'], time.time()
            delay_time = calculate_delay(created, received, active_periods)
            routed_packets[router_id].append(delay_time)
            continue

        path = packet["path"]
        current_index = path.index(router_id)
        next_router_id = path[current_index + 1]

        try: routed_packets[next_router_id].append(packet)
        except KeyError: routed_packets[next_router_id] = [packet]
    return routed_packets

def decide_destination(user_id, num_users, send_rate=0.1 , dist=np.random.normal):
    number = dist(0, 1)
    if send_rate > number > - send_rate:
        destination = random.randint(0, num_users - 1)
        if destination != user_id: return destination
    return None