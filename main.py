import numpy as np
import matplotlib.pyplot as plt
from simulation.world import SwarmWorld
from simulation.attacks import Adversary

def main():
    config = {
        'n': 6,
        'f': 2,
        'R_GNSS': 0.5,
        'R_INS': 0.1,
        'sigma_d': 0.05,
        'dt': 1.0,
        'spoof_bias': np.array([15.0, 15.0, 0.0])
    }

    world = SwarmWorld(config)
    adversary = Adversary(config)

    world.generate_step(k=1)
    
    reports = world.get_all_reports()
    dist_matrix = world.get_full_distance_matrix()

    faulty_indices, attacked_dist_matrix = adversary.apply_attacks(world.drones, dist_matrix)

    plt.figure(figsize=(10, 7))
    
    true_x = [d.true_pos[0] for d in world.drones]
    true_y = [d.true_pos[1] for d in world.drones]
    plt.scatter(true_x, true_y, marker='x', color='green', label='True Position [cite: 290]')

    rep_x = [d.gnss_pos[0] for d in world.drones]
    rep_y = [d.gnss_pos[1] for d in world.drones]
    plt.scatter(rep_x, rep_y, marker='^', color='red', label='Reported (Noisy/Spoofed) [cite: 290]')

    for i in range(config['n']):
        plt.plot([true_x[i], rep_x[i]], [true_y[i], rep_y[i]], 'k--', alpha=0.3)

    plt.title(f"Phase 1 Test: Swarm size n={config['n']}, Faulty f={config['f']}")
    plt.xlabel("Projected X (m)")
    plt.ylabel("Projected Y (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Faulty Drones indices: {faulty_indices}")

if __name__ == "__main__":
    main()