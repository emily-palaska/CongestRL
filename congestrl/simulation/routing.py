import threading, queue
from congestrl.core import demultiplex_packets, create_packets, distributed_partition

class Router:
    def __init__(self, router_id, num_routers, num_users, graph, events, active_periods):
        # Arguments
        self.router_id, self.num_routers, self.graph = router_id, num_routers, graph
        self.local_users = distributed_partition(num_users, num_routers, router_id)
        self.active_periods = active_periods
        # Threading initialization
        self.start_event, self.stop_event, self.freeze_event = events
        self.incoming_queue, self.buffer = queue.Queue(), queue.Queue()
        self.router_thread = threading.Thread(target=self.router_thread)
        # Placeholders
        self.neighbor_routers = None
        self.forwarded_packets, self.delay_times = [], []
        self.packets_created, self.packets_received = 0, 0
        self.send_rate, self.max_send_rate = 10000, 10000

    def start(self):
        self.router_thread.start()

    def sample_delay(self, rate=1000):
        if rate < len(self.delay_times):
            return sum(self.delay_times[-rate:]) / rate
        return sum(self.delay_times) / (len(self.delay_times) + 1.0e-12)

    def _forward_packets(self, routed_packets):
        sleep_time = 0
        for next_router_id, packets in routed_packets.items():
            if next_router_id == self.router_id: continue
            new_weight = sum(packet["weight"] for packet in packets)
            sleep_time += new_weight
            self.graph[self.router_id][next_router_id]['weight'] = new_weight
            self.neighbor_routers[next_router_id].incoming_queue.put(packets)
        return sleep_time

    def _add_to_buffer(self, packets):
        for packet in packets:
            self.buffer.put(packet)

    def _get_from_buffer(self):
        num_packets = min(self.send_rate, self.buffer.qsize())
        return [self.buffer.get() for _ in range(num_packets)]

    def router_thread(self):
        self.start_event.wait()
        while True:
            if self.stop_event.is_set(): break
            if self.freeze_event.is_set(): self.start_event.wait()
            if self.graph is None: continue

            created_packets = create_packets(self.router_id, self.local_users, self.num_routers, self.graph)
            self.packets_created += len(created_packets)
            self._add_to_buffer(created_packets)
            if incoming_packets := self.incoming_queue.qsize():
                for _ in range(incoming_packets): self._add_to_buffer(self.incoming_queue.get())

            routed_packets = demultiplex_packets(router_id=self.router_id, packets=self._get_from_buffer(),
                                                 active_periods=self.active_periods)
            self.packets_received += len(routed_packets[self.router_id])
            self.delay_times.extend(routed_packets[self.router_id])

            num_packets = self._forward_packets(routed_packets) if len(routed_packets) > 1 else 0
            self.forwarded_packets.append(num_packets)
