import networkx as nx

a = [1, 2, 3, 4]
graph = nx.Graph()
graph.add_edge(1, 2, weight=1)
graph[1][2]['weight'] = 4
