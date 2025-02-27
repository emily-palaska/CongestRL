import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image

class User:
    def __init__(self, user_id, send_rate=0.1):
        self.user_id = user_id
        self.send_rate = send_rate  # Probability of sending a message per time step
        self.data_sent = 0  # Tracks amount of data sent

    def send_data(self):
        """ Simulates sending data with a probability based on send_rate """
        if np.random.rand() < self.send_rate:
            self.data_sent += 1
            return True
        return False


class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.users = []
        self.buffer = 0  # Simulates congestion level

    def connect_user(self, user):
        self.users.append(user)

    def receive_data(self):
        """ Simulates receiving data from connected users """
        for user in self.users:
            if user.send_data():
                self.buffer += 1  # Increase congestion level if data is sent


class CongestNetwork:
    def __init__(self, num_users=10, num_routers=3):
        self.network = nx.Graph()
        self.users = [User(f"User_{i+1}", send_rate=random.uniform(0.1, 0.5)) for i in range(num_users)]
        self.routers = [Router(f"Router_{i+1}") for i in range(num_routers)]

        # Randomly assign users to routers
        for user in self.users:
            chosen_router = random.choice(self.routers)
            chosen_router.connect_user(user)
            self.network.add_edge(user.user_id, chosen_router.router_id)

        # Connect routers to form an internet-like structure
        for i in range(len(self.routers)):
            for j in range(i + 1, len(self.routers)):
                self.network.add_edge(self.routers[i].router_id, self.routers[j].router_id, weight=random.randint(1, 5))

    def simulate_traffic(self, steps=10, delay=1, save_gif=True):
        """ Simulates live network traffic over multiple steps and saves as GIF if needed """
        frames = []

        for _ in range(steps):
            for router in self.routers:
                router.receive_data()

            # Save the visualization as an image
            fig = self.visualize_network()

            # Convert figure to an image and store it
            fig.canvas.draw()
            frame = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.buffer_rgba ())
            frames.append(frame)

            plt.close(fig)  # Close the figure to prevent memory issues

        if save_gif:
            gif_path = "../../results/plots/network_simulation.gif"
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=delay * 1000, loop=0)
            print(f"GIF saved as {gif_path}")

    def visualize_network(self):
        """ Visualizes the network state dynamically and optionally saves the figure """
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
        return fig  # Return figure for GIF conversion


# Run the network simulation
if __name__ == "__main__":
    network = CongestNetwork(num_users=10, num_routers=3)
    network.simulate_traffic(steps=10, delay=1, save_gif=True)
