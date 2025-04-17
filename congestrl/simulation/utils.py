import networkx as nx
from colorama import Fore
import random
import numpy as np

def create_packets(router_id, user_ids_map, graph):
    packets = []
    num_users = sum(len(users) for _, users in user_ids_map.items())
    for user_id in user_ids_map[router_id]:
        source_node = router_id
        destination_user = user_decide_destination(user_id, num_users)
        if destination_user is None: continue

        destination_node = find_key(user_ids_map, destination_user)
        if destination_node == router_id: continue
        best_path = shortest_path_policy(graph, source_node, destination_node)

        if best_path:
            packet = {
                "source_node": source_node,
                "destination_node": destination_node,
                "path": best_path,
                "weight": random.randint(1, 10)
            }
            packets.append(packet)
        else:
            print(Fore.BLUE + f"Router {source_node} no path to Router {destination_node}")
    return packets

def demultiplex_packets(router_id, packets):
    if not packets: return None
    routed_packets = {}

    for packet in packets:
        if packet["destination_node"] == router_id:
            #print(Fore.GREEN + f"\nRouter {router_id} received packet with path {packet["path"]}.")
            continue

        # todo change the path dynamically
        path = packet["path"]
        current_index = path.index(router_id)
        next_router_id = path[current_index + 1]

        try:
            routed_packets[next_router_id].append(packet)
        except KeyError:
            routed_packets[next_router_id] = [packet]
    return routed_packets if not routed_packets == {} else None

def user_decide_destination(user_id, num_users, send_rate=0.5 , dist=np.random.normal):
    number = dist(0, 1)
    if send_rate > number > - send_rate:
        destination = random.randint(0, num_users - 1)
        if destination != user_id: return destination
    return None

def find_key(my_dict, element):
    for key, values in my_dict.items():
        if element in values:
            return key
    return None

def shortest_path_policy(graph, start_node, destination_node):
    try:
        path = nx.shortest_path(graph, source=start_node, target=destination_node, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None
