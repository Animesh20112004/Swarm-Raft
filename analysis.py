import numpy as np
import matplotlib.pyplot as plt
from simulation.drone import Drone
from simulation.attacks import apply_spoofing
from simulation.bridge import SwarmRaftBridge

def run_scaling_analysis():
    results = []
    sizes = [3, 5, 7, 9, 11, 13, 15, 17]
    bridge = SwarmRaftBridge()

    for n in sizes:
        f = (n - 1) // 2 # Max tolerated faults [cite: 88, 195]
        errors = []
        for _ in range(100): # Monte Carlo trials [cite: 342]
            drones = [Drone(i, np.random.uniform(0, 100, 3)) for i in range(n)]
            dist_mat = np.zeros((n, n))
            for i in range(n):
                for j in range(n): dist_mat[i,j] = drones[i].get_noise_dist(drones[j])
            
            apply_spoofing(drones, f)
            recovered, _ = bridge.run_consensus(drones, dist_mat)
            
            mae = np.mean([np.linalg.norm(recovered[i] - drones[i].true_pos) for i in range(n)])
            errors.append(mae)
        results.append(np.mean(errors))

    plt.semilogy(sizes, results, 'o--', color='orange', label='SwarmRaft Recovery Error')
    plt.xlabel("Swarm size n")
    plt.ylabel("Mean error (m, log scale)")
    plt.grid(True, which="both", ls="-")
    plt.title("Error Scaling with Swarm Size")
    # plt.savefig("results/scaling_analysis.png")
    plt.show()

if __name__ == "__main__":
    run_scaling_analysis()