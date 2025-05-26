import time, threading
from colorama import Fore
from congestrl.simulation.routing import Router
from congestrl.core import ensure_connectivity, create_random_graph

class CongestNetwork:
    def __init__(self, num_users=10, num_routers=10, connection_density=0.5):
        # Arguments
        self.num_users = num_users
        self.num_routers = num_routers
        self.connection_density = connection_density
        # Placeholders
        self.routers, self.active_periods, self.congestions = [], [], []
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
                               active_periods=self.active_periods,
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
            time.sleep(0.1)
            self.congestions.append(self.sample_congestion())
            delay = sum(d for d in self.get_delays().values()) / self.num_routers
            if verbose: print(Fore.CYAN + f'congestion: {self.congestions[-1]}, delay: {delay}')

        end_time = time.time()
        if len(self.active_periods) >= 100: self.active_periods.pop(0)
        self.active_periods.append((start_time, end_time))
        self.start_event.clear()
        self.freeze_event.set()

    def stop(self):
        self.stop_event.set()
        self.freeze_event.set()
        self.start_event.set()
        for router in self.routers:
            router.router_thread.join(timeout=0.1)

    def reset(self):
        self.congestions = []
        self.graph = ensure_connectivity(
            create_random_graph(num_nodes=self.num_routers,
                                connection_density=self.connection_density)
        )
        self._initialize_routers()

    def sample_congestion(self):
        return sum(data['weight'] for _, _, data in self.graph.edges(data=True))

    def get_congestions(self, cong_samples=25):
        if len(self.congestions) < cong_samples:
            padding = [0] * (cong_samples - len(self.congestions))
            return padding + self.congestions
        else:
            return self.congestions[-cong_samples:]

    def get_delays(self, delay_samples=1000):
        return {router.router_id: router.sample_delay(rate=delay_samples) for router in self.routers}

    def get_send_rates(self):
        return {router.router_id: router.send_rate for router in self.routers}

