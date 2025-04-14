import numpy as np
import random, threading, time, queue, json
from utils import find_key, demultiplex_packets, shortest_path_policy
from colorama import Fore

class User:
    def __init__(self, user_id, assigned_router_id, num_users, dist=np.random.uniform):
        self.user_id = user_id
        self.dist = dist # TODO add more distributions
        self.num_users = num_users
        self.assigned_router_id = assigned_router_id
        self.send_rate = 0
        self.total_lag = 0

        self.rate_thread = threading.Thread(target=self.send_rate_thread)
        self.stop_event = threading.Event()

    def send_packet(self):
        if self.dist(0, 1) < self.send_rate:
            destination = random.randint(0, self.num_users - 1)
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
    def __init__(self, router_id, user_ids_map, network_queue, num_users, connection_capacity=10):
        self.router_id = router_id
        self.num_users = num_users
        self.stop_event = threading.Event()
        self.connection_capacity = connection_capacity

        self.user_ids_map = user_ids_map
        self.users = [User(user_id, router_id, num_users) for user_id in user_ids_map[router_id]]

        self.network_queue = network_queue
        self.packet_queue = queue.Queue()
        self.graph_queue = queue.Queue()
        self.router_thread = threading.Thread(target=self.router_thread)

    def start(self):
        self.router_thread.start()

    def stop(self):
        self.stop_event.set()
        self.router_thread.join()
        for user in self.users:
            user.stop()
        print(Fore.RED + f'Router {self.router_id} stopped')

    def update_graph(self, graph):
        self.graph_queue.put(graph)


    def _create_packets(self, current_graph):
        packets = []
        for user in self.users:
            start_node = self.router_id
            destination_user = user.send_packet()
            if destination_user is None: continue

            destination_node = find_key(self.user_ids_map, destination_user)
            if destination_node == self.router_id: continue

            best_path = shortest_path_policy(current_graph, start_node, destination_node)

            if best_path:
                packet = {
                    "start_node": start_node,
                    "destination_node": destination_node,
                    "path": best_path,
                    "dummy_data": f"Data from User {user.user_id} to User {destination_user}"
                }
                packets.append(packet)
                print(Fore.GREEN + f"Router {self.router_id} sending packet: {json.dumps(packet, indent=2)}")
            else:
                print(Fore.BLUE + f"Router {self.router_id} no path to Router {destination_node}")
        return packets

    def router_thread(self):
        for user in self.users:
            user.start()

        current_graph = None

        while not self.stop_event.is_set():
            if not self.graph_queue.empty():
                current_graph = self.graph_queue.get()
                print(Fore.YELLOW + "Router {self.router_id} updated graph: {current_graph}")

            if current_graph is None: continue
            routed_packets = demultiplex_packets(self.router_id, self._create_packets(current_graph))
            self.network_queue.put(routed_packets)

            time.sleep(random.randint(1, 3))
