import matplotlib.pyplot as plt

def draw_congestion_graph(congestion_times):
    plt.figure(figsize=(12, 6))

    for router_id, times in congestion_times.items():
        # Plot the congestion times as vertical lines or scatter points
        plt.plot(times, label=f"Router {router_id}")

    plt.xlabel("Time")
    plt.ylabel("Congestion")
    plt.title("Congestion Events per Router")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def draw_graph_weights(graph_weights):
    plt.figure(figsize=(12, 6))
    plt.plot(graph_weights)
    plt.xlabel("Time")
    plt.ylabel("Total Edge Weight")
    plt.title("Total Edge Weights during Runtime")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
