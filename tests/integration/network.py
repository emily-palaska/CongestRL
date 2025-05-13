from simulation.network import CongestNetwork
from colorama import Fore
import time

def main():
    net = CongestNetwork(num_users=50, num_routers=10, connection_density=0.1)

    print('CONNECTED_ROUTERS')
    for router in net.routers:
        print(f'{router.router_id}: {list(router.neighbor_routers.keys())}')
    print('=' * 60)

    net.start(run_time=2, verbose=True)
    print(Fore.BLUE + 'FROZEN')
    time.sleep(2)
    net.start(run_time=2, verbose=True)
    net.stop()

    packets_created = {
        router.router_id: router.packets_created
        for router in net.routers
    }
    packets_received = {
        router.router_id: router.packets_received
        for router in net.routers
    }

    print(Fore.GREEN + f'Packets created: {sum(packets_created.values())}')
    print(f'Packets received: {sum(packets_received.values())}')
    print('Delay times:')
    for router in net.routers: print(router.delay_times)


if __name__ == '__main__':
    main()
