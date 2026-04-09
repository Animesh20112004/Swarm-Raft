import numpy as np
import matplotlib.pyplot as plt
from simulation.drone import Drone
from simulation.attacks import apply_spoofing
from simulation.bridge import SwarmRaftBridge

def run_single_test(n=11, f=5):
    drones = [Drone(i, np.random.uniform(0, 100, 3)) for i in range(n)]
    dist_mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_mat[i,j] = drones[i].get_noise_dist(drones[j])

    apply_spoofing(drones, f)
    bridge = SwarmRaftBridge()
    recovered_pos, flags = bridge.run_consensus(drones, dist_mat)

    # Visualization [cite: 270]
    plt.figure(figsize=(8,6))
    for i, d in enumerate(drones):
        plt.scatter(d.true_pos[0], d.true_pos[1], c='g', marker='x', label='True' if i==0 else "")
        plt.scatter(d.reported_pos[0], d.reported_pos[1], c='r', marker='^', label='Spoofed' if i==0 else "")
        plt.scatter(recovered_pos[i][0], recovered_pos[i][1], c='y', marker='*', label='Recovered' if i==0 else "")
        plt.arrow(d.true_pos[0], d.true_pos[1], d.reported_pos[0]-d.true_pos[0], 
                  d.reported_pos[1]-d.true_pos[1], color='gray', alpha=0.3)

    plt.title(f"SwarmRaft Verification (n={n}, f={f})")
    plt.legend()
    # plt.savefig("results/single_test.png")
    plt.show()

if __name__ == "__main__":
    run_single_test()