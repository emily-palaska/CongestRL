import networkx as nx
from nodes import Router
import random, queue, time
from colorama import Fore

class NetworkTopology:
    def __init__(self, num_users=10, num_routers=10):
        self.num_users = num_users
        self.num_routers = num_routers
        self.graph = nx.Graph()
        self.network_queue = queue.Queue()
        self.routers = None

    def initialize_routers(self):
        self._assign_users_to_router()
        self.routers = [Router(router_id,
                               self.user_ids_map,
                               self.network_queue,
                               self.num_users)
                        for router_id in range(self.num_routers)]

    def initialize_graph(self, connection_density=0.05):
        self.graph.add_nodes_from([i for i in range(self.num_routers)])
        for i in range(self.num_routers):
            for j in range(i + 1, self.num_routers):
                if random.random() < connection_density:
                    self.graph.add_edge(i, j)

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

    def start(self):
        # Start the router thread
        for router in self.routers:
            router.start()
            router.update_graph(self.graph)

        start_time = time.time()
        while time.time() - start_time < 10:
            # Forward the packets from the outgoing queues
            for router in self.routers:
                if not router.outgoing_queue.empty():
                    for dest_id, packets in router.outgoing_queue.get().items():
                        self.routers[int(dest_id)].incoming_queue.put(packets)

            #for router in self.routers:
                #router.update_graph(self.graph)

    def stop(self):
        for router in self.routers:
            router.stop()

def main():
    net = NetworkTopology()
    net.initialize_routers()
    net.initialize_graph(connection_density=0.5)

    print('USERS MAP')
    print(net.user_ids_map)
    print('='*60)

    net.start()
    net.stop()

if __name__ == '__main__':
    main()