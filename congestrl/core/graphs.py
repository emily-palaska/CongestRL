import networkx as nx
import random

def ensure_connectivity(G):
    if not nx.is_connected(G):
        components = list(nx.connected_components(G))
        while len(components) > 1:
            node1 = random.choice(list(components[0]))
            node2 = random.choice(list(components[1]))
            G.add_edge(node1, node2, weight=1)
            components = list(nx.connected_components(G))
    return G

def create_random_graph(num_nodes, connection_density=0.1):
    G = nx.Graph()
    G.add_nodes_from([i for i in range(num_nodes)])
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < connection_density:
                G.add_edge(i, j, weight=1)
    ensure_connectivity(G)
    return G

def shortest_path_policy(graph, start_node, destination_node):
    try:
        path = nx.shortest_path(graph, source=start_node, target=destination_node, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None