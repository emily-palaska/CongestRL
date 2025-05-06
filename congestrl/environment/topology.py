from routing import Router
import time
from colorama import Fore
from congestrl.core import ensure_connectivity, create_random_graph
from congestrl.visualization.graphs import draw_weights_runtime, draw_congestion_graph

class NetworkTopology:
    def __init__(self, num_users=10, num_routers=10, connection_density=0.5):
        # Arguments
        self.num_users = num_users
        self.num_routers = num_routers
        self.connection_density = connection_density
        # Placeholders
        self.routers = []
        self.weights_runtime = []
        # Initialization
        self.graph = ensure_connectivity(
            create_random_graph(num_nodes=self.num_routers,
                                connection_density=connection_density)
        )
        self._initialize_routers()

    def _initialize_routers(self):
        self.routers = [Router(router_id=router_id,
                               num_routers=self.num_routers,
                               num_users=self.num_users,
                               graph=self.graph)
                        for router_id in range(self.num_routers)]
        self._update_neighbor_routers()

    def _update_neighbor_routers(self):
        for i in range(self.num_routers):
            neighbor_routers = {
                self.routers[n].router_id: self.routers[n]
                    for n in self.graph.neighbors(i)
            }
            self.routers[i].neighbor_routers = neighbor_routers

    def start(self, run_time=20):
        for router in self.routers:
            router.graph = self.graph
            router.start()

        start_time = time.time()
        while time.time() - start_time < run_time:
            total_weight = sum(data['weight'] for _, _, data in self.graph.edges(data=True))
            self.weights_runtime.append(total_weight)
            print(Fore.CYAN + f"Total Graph weight: {total_weight}")
            time.sleep(1)

    def stop(self):
        for router in self.routers:
            router.stop()

    def reset(self):
        self.stop()
        self.weights_runtime = []
        for u, v in self.graph.edges():
            self.graph[u][v]['weight'] = 1

def main():
    net = NetworkTopology(num_users=50, num_routers=10, connection_density=0.1)

    print('CONNECTED_ROUTERS')
    for router in net.routers:
        print(f'{router.router_id}: {router.neighbor_routers.keys()}')
    print('=' * 60)

    net.start(run_time=10)
    net.stop()

    congestion_times = {
        router.router_id: router.congestion_times
            for router in net.routers
    }
    draw_congestion_graph(congestion_times)

    packets_created = {
        router.router_id: router.packets_created
            for router in net.routers
    }

    packets_received = {
        router.router_id: router.packets_received
        for router in net.routers
    }

    print(f'Packets created: {packets_created} -> {sum(packets_created.values())}')
    print(f'Packets received: {packets_received} -> {sum(packets_received.values())}')
    draw_weights_runtime(net.weights_runtime)


if __name__ == '__main__':
    main()