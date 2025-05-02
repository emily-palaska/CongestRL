import threading, time, queue
from utils import demultiplex_packets, create_packets
from colorama import Fore

class Router:
    def __init__(self, router_id, user_ids_map, num_users, graph):
        self.router_id = router_id
        self.num_users = num_users
        self.stop_event = threading.Event()
        self.graph = graph

        self.user_ids_map = user_ids_map
        self.connected_routers = None

        self.incoming_queue = queue.Queue()
        self.router_thread = threading.Thread(target=self.router_thread)
        self.congestion_times = []

        self.packets_created = 0
        self.packets_received = 0

    def start(self):
        self.router_thread.start()

    def stop(self):
        self.stop_event.set()
        self.router_thread.join()
        print(Fore.YELLOW + f'Router {self.router_id} stopped')

    def _forward_packets(self, routed_packets):
        sleep_time = 0
        for next_router_id, packets in routed_packets.items():
            if next_router_id == self.router_id: continue
            new_weight = sum(packet["weight"] for packet in packets)
            sleep_time += new_weight
            self.graph[self.router_id][next_router_id]['weight'] = new_weight
            self.connected_routers[next_router_id].incoming_queue.put(packets)
        return sleep_time

    def router_thread(self):
        while not self.stop_event.is_set():
            if self.graph is None: continue

            packets = create_packets(self.router_id, self.user_ids_map, self.graph)
            self.packets_created += len(packets)
            if not self.incoming_queue.empty():
                packets.extend(self.incoming_queue.get())

            routed_packets = demultiplex_packets(self.router_id, packets)
            self.packets_received += routed_packets[self.router_id]
            sleep_time = self._forward_packets(routed_packets) if len(routed_packets) > 1 else 0
            self.congestion_times.append(sleep_time)
            time.sleep(sleep_time / 10)
