from congestrl.core.graph import shortest_path_policy
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

def demultiplex_packets(router_id, packets):
    routed_packets = {router_id: []}
    if not packets: return routed_packets

    for packet in packets:
        if packet["destination_node"] == router_id:
            delay_time = round(time.time() - packet["created"], 2)
            routed_packets[router_id].append(delay_time)
            #print(Fore.GREEN + f"\nRouter {router_id} received packet with path {packet["path"]}.")
            continue

        # todo change the path dynamically
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