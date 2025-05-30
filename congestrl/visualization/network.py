from simulation.network import CongestNetwork
import networkx as nx
import matplotlib.pyplot as plt


def main():
    net = CongestNetwork(num_users=50, num_routers=10, connection_density=0.5)
    custom_labels = {node: f"r{node}" for node in net.graph.nodes()}
    node_color, edge_color = '#56517E', 'slategrey'


    plt.figure()
    pos = nx.spring_layout(net.graph)

    nx.draw(net.graph, pos,
            labels=custom_labels,
            node_color=node_color,
            edge_color=edge_color,
            font_color='white',
            width=1.5,
            node_size=800,
            font_size=10)

    legend_texts = [
        f'num_routers = {net.num_routers}',
        f'connection_density = {net.connection_density}'
    ]

    legend_elements = [
        plt.Line2D([0], [0],
                   marker='o',
                   color=node_color,
                   label=legend_texts[0],
                   markersize=10,
                   linestyle='None'),

        plt.Line2D([0], [0],
                   color=edge_color,
                   label=legend_texts[1],
                   linewidth=2)
    ]

    legend = plt.legend(handles=legend_elements,
                        loc='best',
                        title='Network Info',
                        fontsize=10)
    legend.get_title().set_fontsize('12')

    plt.savefig(f'../../results/plots/network_{net.connection_density}.png',
                bbox_inches='tight',
                dpi=300)
    net.stop()

if __name__ == '__main__':
    main()