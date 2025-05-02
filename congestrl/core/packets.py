from congestrl.core.graph_operations import shortest_path_policy
from congestrl.core.statistical_operations import probabilistic_redirect
import random
from colorama import Fore
import numpy as np

def find_destination_node(user_ids_map, dest_user, source_node):
    for dest_node, users in user_ids_map.items():
        if dest_user in users and dest_node != source_node:
            return dest_node
    return None

def create_packets(router_id, user_ids_map, graph, send_rate=0.01):
    packets = []
    num_users = sum(len(users) for _, users in user_ids_map.items())
    for user_id in user_ids_map[router_id]:
        source_node = router_id
        if (
                dest_user := probabilistic_redirect(
                    source_id=user_id,
                    num_nodes=num_users,
                    activation_rate=send_rate
                )
        ) is None: continue

        if (
                destination_node := find_destination_node(
                    user_ids_map=user_ids_map,
                    dest_user=dest_user,
                    source_node=router_id
                )
        ) is None: continue

        if best_path := shortest_path_policy(graph, source_node, destination_node):
            packets.append({
                "source_node": source_node,
                "destination_node": destination_node,
                "path": best_path,
                "weight": random.randint(1, 10)
            })
        else:
            print(Fore.BLUE + f"Router {source_node} no path to Router {destination_node}")
    return packets

def demultiplex_packets(router_id, packets):
    routed_packets = {router_id: 0}
    if not packets: return routed_packets

    for packet in packets:
        if packet["destination_node"] == router_id:
            routed_packets[router_id] += 1
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