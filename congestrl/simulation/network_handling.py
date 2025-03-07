import networkx as nx
import numpy as np
import random
import threading
import time

GLOBAL_USERS = 10
GLOBAL_ROUTERS = 2
class User:
    def __init__(self, user_id, dist=np.random.uniform):
        self.user_id = user_id
        self.dist = dist # TODO add more distributions
        self.send_rate = 0
        self.total_lag = 0

        self.rate_thread = threading.Thread(target=self.rate_thread)
        self.stop_event = threading.Event()

    def send_packet(self):
        if self.dist(0, 1) < self.send_rate:
            return random.randint(0, GLOBAL_USERS)

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

    def rate_thread(self):
        while 1:
            if self.stop_event.is_set(): break
            self.change_send_rate()
            time.sleep(0.5)



class Router:
    def __init__(self, router_id, user_ids, connection_capacity=10):
        self.router_id = router_id
        self.stop_event = threading.Event()
        self.connection_capacity = connection_capacity

        self.users = [User(user_id) for user_id in user_ids]

        self.buffer = 0
        self.router_thread = threading.Thread(target=self.router_thread)

        self.routing_policy = None # TODO implement different strategies


    def start(self):
        self.router_thread.start()

    def stop(self):
        self.stop_event.set()
        self.router_thread.join()
        for user in self.users: user.stop()

    def router_thread(self):
        for user in self.users: user.start()
        while 1:
            if self.stop_event.is_set(): break
            destinations = [user.send_packet() for user in self.users]
            print(f'Router {self.router_id} destinations: {destinations}')
            time.sleep(1)

def main():
    numbers = list(range(GLOBAL_USERS))
    random.shuffle(numbers)

    # initialization
    routers = []
    for i in range(GLOBAL_ROUTERS):
        users = numbers[i * GLOBAL_USERS // GLOBAL_ROUTERS : (i + 1) * GLOBAL_USERS // GLOBAL_ROUTERS - 1]
        routers.append(Router(i, users))

    for router in routers: router.start()
    time.sleep(3)
    for router in routers: router.stop()

if __name__ == '__main__':
    main()
