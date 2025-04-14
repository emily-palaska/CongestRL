import networkx as nx
import matplotlib.pyplot as plt
from colorama import Fore

def find_key(my_dict, element):
    for key, values in my_dict.items():
        if element in values:
            return key
    return None

def draw_topology(graph, layout=nx.circular_layout):
    if not layout in [nx.circular_layout,
                      nx.spring_layout,
                      nx.kamada_kawai_layout,
                      nx.spectral_layout,
                      nx.random_layout]:
        raise TypeError
    pos = layout(graph)
    nx.draw(graph, pos, node_color='lightblue', node_size=5)
    plt.show()

def demultiplex_packets(router_id, packets):
    routed_packets = {}
    for packet in packets:
        if packet["destination_node"] == router_id:
            print(Fore.GREEN + f"Router {router_id} received packet with path {packet["path"]}.")
            continue
        path = packet["path"]
        current_index = path.index(router_id)
        next_router_id = path[current_index + 1]
        try:
            routed_packets[next_router_id].append(packet)
        except KeyError:
            routed_packets[next_router_id] = [packet]
    return routed_packets

def shortest_path_policy(graph, start_node, destination_node):
    try:
        path = nx.shortest_path(graph, source=start_node, target=destination_node, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None
