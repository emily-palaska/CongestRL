"""
def visualize_network(self):
    pos = nx.spring_layout(self.network)

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(self.network, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=1200,
            font_size=10)

    # Get router and user positions
    router_positions = {router.router_id: pos[router.router_id] for router in self.routers}
    user_positions = {user.user_id: pos[user.user_id] for user in self.users}

    # Offset labels above routers (buffer levels)
    buffer_labels = {router.router_id: f"Buf: {router.buffer}" for router in self.routers}
    buffer_positions = {k: (v[0], v[1] + 0.08) for k, v in router_positions.items()}

    # Offset labels above users (send rates)
    send_rate_labels = {user.user_id: f"Rate: {user.send_rate:.2f}" for user in self.users}
    send_rate_positions = {k: (v[0], v[1] + 0.08) for k, v in user_positions.items()}

    nx.draw_networkx_labels(self.network, buffer_positions, labels=buffer_labels, font_color="red", font_size=10)
    nx.draw_networkx_labels(self.network, send_rate_positions, labels=send_rate_labels, font_color="blue",
                            font_size=9)

    plt.title("Live Network Visualization")
    return fig
"""
"""
class CongestNetwork:
    def __init__(self, num_routers=3):
        self.network = nx.Graph()

        self.routers = [Router(i) for i in range(num_routers)]

    def simulate_traffic(self, steps=10):
        frames = []

        for _ in range(steps):
            for router in self.routers:
                router.receive_data()
            frames.append(self.screenshot())
        return frames

    def screenshot(self):
        return self.network

"""