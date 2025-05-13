import os
import matplotlib.pyplot as plt
from congestrl.core import ResultManager

def plot_result_manager(result_manager: ResultManager, path: str,
                        congestion=True, rewards=True, delays=True):
    assert len(result_manager) != 0, "Empty result manager"
    if not (congestion or rewards or delays): return

    full_path = os.path.join(path, result_manager.filename)
    plot_items = {
        'rewards': rewards,
        'congestions': congestion,
        'delays': delays
    }

    for key, should_plot in plot_items.items():
        if should_plot:
            data = result_manager.get_data(key)
            if not data:
                continue  # Skip empty data
            plt.figure(figsize=(10, 5))
            plt.plot(data, marker='o')
            plt.title(f"Episode {key.capitalize()}")
            plt.xlabel("Episode")
            plt.ylabel(key.capitalize())
            plt.grid(True)
            plt.savefig(f"{key}_{full_path}")
            plt.close()
