from routing import Router
import time
from colorama import Fore
from congestrl.core import ensure_connectivity, create_random_graph
from congestrl.visualization.graphs import draw_weights_runtime
import threading

class NetworkTopology:
    def __init__(self, num_users=10, num_routers=10, connection_density=0.5):
        # Arguments
        self.num_users = num_users
        self.num_routers = num_routers
        self.connection_density = connection_density
        # Placeholders
        self.routers = []
        self.weights_runtime = []
        self.start_event, self.stop_event, self.freeze_event = threading.Event(), threading.Event(), threading.Event()
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
                               graph=self.graph,
                               events=(self.start_event, self.stop_event, self.freeze_event))
                        for router_id in range(self.num_routers)]
        self._update_neighbor_routers()
        for router in self.routers:
            router.graph = self.graph
            router.start()

    def _update_neighbor_routers(self):
        for i in range(self.num_routers):
            neighbor_routers = {
                self.routers[n].router_id: self.routers[n]
                    for n in self.graph.neighbors(i)
            }
            self.routers[i].neighbor_routers = neighbor_routers

    def start(self, run_time=20):
        start_time = time.time()
        self.freeze_event.clear()
        self.start_event.set()
        while time.time() - start_time < run_time:
            time.sleep(1)
            global_congestion = sum(data['weight'] for _, _, data in self.graph.edges(data=True))
            self.weights_runtime.append(global_congestion)
            print(Fore.CYAN + f"Total Graph weight: {global_congestion}")
        self.start_event.clear()
        self.freeze_event.set()

    def stop(self):
        self.stop_event.set()
        for router in self.routers: router.router_thread.join()

    def reset(self):
        self.stop()
        self.weights_runtime = []
        self.graph = ensure_connectivity(
            create_random_graph(num_nodes=self.num_routers,
                                connection_density=self.connection_density)
        )
        self._initialize_routers()

    def sample_delay(self, rate=1000):
        delay = sum(router.delay_times[-rate] for router in self.routers)
        return delay / self.num_routers

def main():
    net = NetworkTopology(num_users=50, num_routers=10, connection_density=0.1)

    print('CONNECTED_ROUTERS')
    for router in net.routers:
        print(f'{router.router_id}: {list(router.neighbor_routers.keys())}')
    print('=' * 60)

    net.start(run_time=10)
    print(Fore.BLUE + 'FROZEN')
    time.sleep(2)
    net.start(run_time=10)
    net.stop()

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
    print('Delay times:')
    for router in net.routers: print(router.delay_times)
    draw_weights_runtime(net.weights_runtime)


if __name__ == '__main__':
    main()