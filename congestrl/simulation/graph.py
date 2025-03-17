import matplotlib.pyplot as plt
import networkx as nx
from nodes import Router
import random
from env import *

class NetworkTopology:
    def __init__(self, num_users=GLOBAL_USERS, num_routers=GLOBAL_ROUTERS):
        self.num_users = num_users
        self.num_routers = num_routers

        self.graph = nx.Graph()
        self._assign_users_to_router()

        self.routers = [Router(router_id, self.user_router_map[router_id]) for router_id in range(num_routers)]
        self.graph.add_nodes_from([f'r{i}' for i in range(self.num_routers)])

    def connect_routers(self, connection_density=0.05):
        for i in range(self.num_routers):
            for j in range(i + 1, self.num_routers):
                if random.random() < connection_density:
                    self.graph.add_edge(f'r{i}', f'r{j}')

    def _assign_users_to_router(self): # TODO not equal distribution
        ids = list(range(self.num_users))
        random.shuffle(ids)
        self.user_router_map = []
        for i in range(GLOBAL_ROUTERS):
            start = i * self.num_users // self.num_routers
            end = (i + 1) * self.num_users // self.num_routers - 1
            self.user_router_map.append(ids[start:end])

    def start(self):
        for router in self.routers:
            router.start()

    def stop(self):
        for router in self.routers:
            router.stop()

    def draw_topology(self, layout=nx.circular_layout):
        if not layout in [nx.circular_layout,
                          nx.spring_layout,
                          nx.kamada_kawai_layout,
                          nx.spectral_layout,
                          nx.random_layout]:
            raise TypeError
        pos = layout(self.graph)
        nx.draw(self.graph, pos, node_color='lightblue', node_size=5)
        plt.show()

def main():
    net = NetworkTopology()
    net.draw_topology()

if __name__ == '__main__':
    main()