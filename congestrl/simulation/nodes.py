import numpy as np
import random, threading, time, queue
from utils import find_key, demultiplex_packets, shortest_path_policy
from colorama import Fore

def user_decide_destination(user_id, num_users, send_rate=0.5 , dist=np.random.uniform):
    if dist(0, 1) < send_rate:
        destination = random.randint(0, num_users - 1)
        if destination != user_id: return destination
    return None

class Router:
    def __init__(self, router_id, user_ids_map, num_users):
        self.router_id = router_id
        self.num_users = num_users
        self.stop_event = threading.Event()
        self.graph = None

        self.user_ids_map = user_ids_map
        self.my_user_ids = user_ids_map[router_id]

        self.outgoing_queue = queue.Queue()
        self.incoming_queue = queue.Queue()
        self.packet_queue = queue.Queue()
        self.router_thread = threading.Thread(target=self.router_thread)

    def start(self):
        self.router_thread.start()

    def stop(self):
        self.stop_event.set()
        self.router_thread.join()
        print(Fore.RED + f'Router {self.router_id} stopped')

    def _create_packets(self, current_graph):
        packets = []
        for user_id in self.my_user_ids:
            source_node = self.router_id
            destination_user = user_decide_destination(user_id, self.num_users)
            if destination_user is None: continue

            destination_node = find_key(self.user_ids_map, destination_user)
            if destination_node == self.router_id: continue

            best_path = shortest_path_policy(current_graph, source_node, destination_node)

            if best_path:
                packet = {
                    "source_node": source_node,
                    "destination_node": destination_node,
                    "path": best_path,
                    "dummy_data": f"Data from User {user_id} to User {destination_user}"
                }
                packets.append(packet)
            else:
                print(Fore.BLUE + f"Router {self.router_id} no path to Router {destination_node}")
        return packets

    def router_thread(self):
        while not self.stop_event.is_set():
            if self.graph is None: continue

            packets = self._create_packets(self.graph)
            if not self.incoming_queue.empty():
                packets.extend(self.incoming_queue.get())

            routed_packets = demultiplex_packets(self.router_id, packets)
            if routed_packets is not None:
                #import json
                #print(Fore.YELLOW + f'Router {self.router_id} outgoing queue: {json.dumps(routed_packets, indent=2)}')
                self.outgoing_queue.put(routed_packets)

            time.sleep(len(packets))


