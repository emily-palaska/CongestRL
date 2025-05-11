import time, threading
from colorama import Fore
from congestrl.network.routing import Router
from congestrl.core import ensure_connectivity, create_random_graph
from congestrl.visualization.graphs import draw_weights_runtime

class CongestNetwork:
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

    def start(self, run_time=20, verbose=False):
        start_time = time.time()
        self.freeze_event.clear()
        self.start_event.set()
        while time.time() - start_time < run_time:
            time.sleep(0.5)
            if verbose:
                congestion = sum(data['weight'] for _, _, data in self.graph.edges(data=True))
                print(Fore.CYAN + f'congestion: {congestion}, delay: {self.sample_delay()}')
        self.start_event.clear()
        self.freeze_event.set()

    def stop(self):
        self.stop_event.set()
        for router in self.routers: router.router_thread.join()

    def reset(self):
        self.weights_runtime = []
        self.graph = ensure_connectivity(
            create_random_graph(num_nodes=self.num_routers,
                                connection_density=self.connection_density)
        )
        self._initialize_routers()

    def get_info(self, rate=1000):
        congestion = sum(data['weight'] for _, _, data in self.graph.edges(data=True))
        delay = sum(router.sample_delay(rate=rate) for router in self.routers) / self.num_routers
        return {'congestion': congestion, 'delay': delay}

def main():
    net = CongestNetwork(num_users=50, num_routers=10, connection_density=0.1)

    print('CONNECTED_ROUTERS')
    for router in net.routers:
        print(f'{router.router_id}: {list(router.neighbor_routers.keys())}')
    print('=' * 60)

    net.start(run_time=20, verbose=True)
    print(Fore.BLUE + 'FROZEN')
    #ime.sleep(2)
    net.start(run_time=5, verbose=True)
    net.stop()

    packets_created = {
        router.router_id: router.packets_created
        for router in net.routers
    }
    packets_received = {
        router.router_id: router.packets_received
        for router in net.routers
    }

    print(f'Packets created: {sum(packets_created.values())}')
    print(f'Packets received: {sum(packets_received.values())}')
    #print('Delay times:')
    #for router in net.routers: print(router.delay_times)
    #draw_weights_runtime(net.weights_runtime)


if __name__ == '__main__':
    main()
