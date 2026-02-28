import numpy as np
import matplotlib.pyplot as plt
from simulation.world import SwarmWorld
from simulation.attacks import Adversary
from simulation.bridge import SwarmRaftBridge

def main():
    # 1. Configuration (matches Phase 1 results)
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
    bridge = SwarmRaftBridge()

    world.generate_step(k=1)
    reports = world.get_all_reports()
    dist_matrix = world.get_full_distance_matrix()

    faulty_indices, attacked_dist_matrix = adversary.apply_attacks(world.drones, dist_matrix)

    recovered_positions, flags = bridge.run_swarmraft(reports, attacked_dist_matrix, threshold=5.0)

    plt.figure(figsize=(12, 8))
    
    true_x = [d.true_pos[0] for d in world.drones]
    true_y = [d.true_pos[1] for d in world.drones]
    rep_x = [d.gnss_pos[0] for d in world.drones]
    rep_y = [d.gnss_pos[1] for d in world.drones]
    rec_x = recovered_positions[:, 0]
    rec_y = recovered_positions[:, 1]

    plt.scatter(true_x, true_y, marker='x', color='green', s=100, label='True Position')
    plt.scatter(rep_x, rep_y, marker='^', color='red', s=80, label='Spoofed/Noisy Report')
    plt.scatter(rec_x, rec_y, marker='*', color='gold', s=150, edgecolors='black', label='SwarmRaft Recovered')

    # Draw lines from spoofed to recovered to show correction
    for i in range(config['n']):
        plt.arrow(rep_x[i], rep_y[i], rec_x[i]-rep_x[i], rec_y[i]-rep_y[i], 
                  color='gray', linestyle=':', head_width=0.5, alpha=0.5)

    plt.title(f"SwarmRaft Final Result (n={config['n']}, f={config['f']})")
    plt.xlabel("Projected X (m)")
    plt.ylabel("Projected Y (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()