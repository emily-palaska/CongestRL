import numpy as np
import networkx as nx
import random, threading, time, queue, json
from env import GLOBAL_USERS, router_user_map

class User:
    def __init__(self, user_id, assigned_router_id, dist=np.random.uniform):
        self.user_id = user_id
        self.dist = dist # TODO add more distributions
        self.assigned_router_id = assigned_router_id
        self.send_rate = 0
        self.total_lag = 0

        self.rate_thread = threading.Thread(target=self.send_rate_thread)
        self.stop_event = threading.Event()

    def send_packet(self):
        if self.dist(0, 1) < self.send_rate:
            destination = random.randint(0, GLOBAL_USERS - 1)
            if destination != self.user_id: return destination
        return None

    def change_send_rate(self, rate = None):
        if rate: self.send_rate = rate
        else: self.send_rate = random.randint(0, 10) / 10

    def announce(self, dest):
        print(f'\tUser {self.user_id} wants to send to user {dest}')

    def start(self):
        self.rate_thread.start()

    def stop(self):
        self.stop_event.set()
        self.rate_thread.join()

    def send_rate_thread(self):
        while 1:
            if self.stop_event.is_set(): break
            self.change_send_rate()
            time.sleep(0.5)


class Router:
    def __init__(self, router_id, user_ids, connection_capacity=10):
        self.router_id = router_id
        self.stop_event = threading.Event()
        self.connection_capacity = connection_capacity

        self.users = [User(user_id, router_id) for user_id in user_ids]

        self.buffer = 0
        self.graph_queue = queue.Queue()  # Queue to hold dynamic graphs
        self.router_thread = threading.Thread(target=self.router_thread)

        self.routing_policy = self.shortest_path_policy  # Default routing policy

    def start(self):
        self.router_thread.start()

    def stop(self):
        self.stop_event.set()
        self.router_thread.join()
        for user in self.users:
            user.stop()

    def update_graph(self, graph):
        self.graph_queue.put(graph)

    def shortest_path_policy(self, graph, start_node, destination_node):
        try:
            path = nx.shortest_path(graph, source=start_node, target=destination_node, weight='weight')
            return path
        except nx.NetworkXNoPath:
            return None  # No path exists

    def router_thread(self):
        for user in self.users:
            user.start()

        current_graph = None

        while not self.stop_event.is_set():
            if not self.graph_queue.empty():
                current_graph = self.graph_queue.get()
                print(f"Router {self.router_id} updated graph: {current_graph}")

            if current_graph is None: continue

            for user in self.users:
                start_node = self.router_id
                destination_user = user.send_packet()
                if destination_user is None: continue

                destination_node = router_user_map[destination_user]
                if destination_node == self.router_id: continue

                best_path = self.routing_policy(current_graph, start_node, destination_node)

                if best_path:
                    packet = {
                        "start_node": start_node,
                        "destination_node": destination_node,
                        "path": best_path,
                        "dummy_data": f"Data from User {user.user_id} to User {destination_user}"
                    }
                    print(f"Router {self.router_id} sending packet: {json.dumps(packet, indent=2)}")
                else:
                    print(f"Router {self.router_id} no path to Router {destination_node}")

            time.sleep(1)

# Example usage
if __name__ == "__main__":
    router1 = Router(router_id=1, user_ids=[0, 1, 2])
    router2 = Router(router_id=2, user_ids=[3, 4, 5])
    router3 = Router(router_id=3, user_ids=[6, 7, 8, 9])
    GLOBAL_ROUTERS = 3
    GLOBAL_USERS = 10
    router_user_map = [1, 1, 1, 2, 2, 2, 3, 3, 3, 3]

    router1.start()
    router2.start()
    router3.start()

    # Simulate dynamic graph updates
    for i in range(5):
        demo_graph = nx.Graph()
        demo_graph.add_weighted_edges_from([
            (1, 2, random.randint(1, 10)),
            (1, 3, random.randint(1, 10)),
            (3, 2, random.randint(1, 10))
        ])
        router1.update_graph(demo_graph)
        router2.update_graph(demo_graph)
        router3.update_graph(demo_graph)
        time.sleep(2)

    router1.stop()
    router2.stop()
    router3.stop()