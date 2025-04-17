import networkx as nx
from routing import Router
import random, time
from colorama import Fore
from congestrl.visualization.congestion_graph import draw_congestion_graph

class NetworkTopology:
    def __init__(self, num_users=10, num_routers=10, connection_density=0.5):
        self.num_users = num_users
        self.num_routers = num_routers
        self.graph = nx.Graph()
        self.routers = None
        self.connection_density = connection_density

        self._initialize_graph(connection_density=connection_density)
        self._initialize_routers()

    def _initialize_routers(self):
        self._assign_users_to_router()
        self.routers = [Router(router_id,
                               self.user_ids_map,
                               self.num_users,
                               self.graph)
                        for router_id in range(self.num_routers)]
        self._assign_connected_routers()

    def _initialize_graph(self, connection_density=0.05):
        self.graph.add_nodes_from([i for i in range(self.num_routers)])
        for i in range(self.num_routers):
            for j in range(i + 1, self.num_routers):
                if random.random() < connection_density:
                    self.graph.add_edge(i, j, weight=1)

    def _assign_users_to_router(self): # TODO not equal distribution
        ids = list(range(self.num_users))
        random.shuffle(ids)

        base_size = self.num_users // self.num_routers
        remainder = self.num_users % self.num_routers

        self.user_ids_map = dict()
        start = 0
        for i in range(self.num_routers):
            if i <= remainder:
                sublist_size = base_size + 1
            else:
                sublist_size = base_size
            end = start + sublist_size
            sublist = ids[start:end]
            sublist.sort()
            self.user_ids_map[i] = sublist
            start = end

    def _assign_connected_routers(self):
        for i in range(self.num_routers):
            connected_routers = {
                self.routers[n].router_id: self.routers[n]
                    for n in self.graph.neighbors(i)
            }
            self.routers[i].connected_routers = connected_routers

    def start(self):
        for router in self.routers:
            router.graph = self.graph
            router.start()

        start_time = time.time()
        while time.time() - start_time < 20:
            total_weight = sum(w for _, w in self.graph.edges())
            print(Fore.CYAN + f"\nTotal Graph weight: {total_weight}")
            time.sleep(1)

    def stop(self):
        for router in self.routers:
            router.stop()

def main():
    net = NetworkTopology(num_users=500, num_routers=50, connection_density=0.5)

    print('USERS MAP')
    print(net.user_ids_map)
    print('='*60)

    """
    print('NETWORK')
    for edge in net.graph.edges():
        print(edge)
    print('='*60)
    """

    net.start()
    net.stop()

    congestion_times = {
        router.router_id: router.congestion_times
            for router in net.routers
    }
    draw_congestion_graph(congestion_times)

if __name__ == '__main__':
    main()