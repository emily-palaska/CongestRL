import networkx as nx
from nodes import Router
import random, time
from colorama import Fore

class NetworkTopology:
    def __init__(self, num_users=10, num_routers=10):
        self.num_users = num_users
        self.num_routers = num_routers
        self.graph = nx.Graph()
        self.routers = None

    def initialize_routers(self):
        self._assign_users_to_router()
        self.routers = [Router(router_id,
                               self.user_ids_map,
                               self.num_users)
                        for router_id in range(self.num_routers)]

    def initialize_graph(self, connection_density=0.05):
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

    def start(self):
        # Start the router thread
        for router in self.routers:
            router.graph = self.graph
            router.start()

        start_time = time.time()
        while time.time() - start_time < 20:
            # Forward the packets from the outgoing queues
            for router in self.routers:
                if not router.outgoing_queue.empty():
                    routed_packets = router.outgoing_queue.get().items()

                    for next_router_id, packets in routed_packets:
                        try:
                            self.graph[router.router_id][next_router_id]['weight'] = len(packets)
                        except Exception as e:
                            print(Fore.RED +
                                  f'Iterating router {router.router_id} with next router {next_router_id}:: '
                                  + f'\nRouted packets: {routed_packets}'
                                  + f'\nException: {e}')

                        self.routers[next_router_id].incoming_queue.put(packets)

            for router in self.routers:
                router.graph = self.graph
            #print(Fore.BLUE + 'Graph updated for all users.')

            #total_weight = sum(data['weight'] for u, v, data in self.graph.edges(data=True))
            #print(Fore.CYAN + f"Total Graph weight: {total_weight}")

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

    print('NETWORK')
    for edge in net.graph.edges():
        print(edge)
    print('='*60)

    net.start()
    net.stop()

if __name__ == '__main__':
    main()