import networkx as nx
import matplotlib.pyplot as plt

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